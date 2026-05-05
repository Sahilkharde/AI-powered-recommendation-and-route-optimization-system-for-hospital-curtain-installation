from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.agents.installation_agent import run_agent
from app.cache import (
    RECOMMEND_TTL,
    match_curtains_key,
    recommendation_key,
    route_key,
)
from app.database import get_db
from app.engine.match import match_curtains_for_track, MatchError
from app.engine.recommender import RecommenderError, suggest_location
from app.engine.route import build_installer_route
from app.schemas import (
    CacheStatsResponse,
    HealthResponse,
    InstallerRouteResponse,
    MatchCurtainsResponse,
    ScanRequest,
    SuggestLocationResponse,
    TrackScanRequest,
)

router = APIRouter()


def _get_cache(request: Request):
    return getattr(request.app.state, "cache", None)


@router.post(
    "/agent/scan-curtain",
    summary="AI Agent: scan a curtain barcode -> get installation guidance",
    response_description=(
        "Structured top-5 recommendations (building/floor/unit/room/track) "
        "plus a plain-language installer explanation from Claude."
    ),
)
def agent_scan_curtain(req: ScanRequest, db: Session = Depends(get_db)):
    try:
        return run_agent(db, req.curtain_barcode)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post(
    "/suggest-location",
    response_model=SuggestLocationResponse,
    summary="Scan a curtain -> get installation location recommendations",
    description=(
        "Given a curtain barcode, the AI agent returns ranked recommendations "
        "for which building, floor, room, and track the curtain should be installed on. "
        "Business rules R1-R12 are enforced automatically."
    ),
)
def api_suggest_location(
    req: ScanRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    cache = _get_cache(request)
    cache_k = recommendation_key(req.curtain_barcode)

    if cache:
        cached = cache.get(cache_k)
        if cached is not None:
            return SuggestLocationResponse(**cached)

    try:
        result = suggest_location(db, req.curtain_barcode)
    except RecommenderError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if cache:
        cache.set(cache_k, result.model_dump(), ttl=RECOMMEND_TTL)

    return result


@router.post(
    "/match-curtains",
    response_model=MatchCurtainsResponse,
    summary="Scan a track -> get matching curtains",
    description=(
        "Given a track barcode, returns a ranked list of curtains that "
        "are compatible in size, type, and style. Filters by availability."
    ),
)
def api_match_curtains(
    req: TrackScanRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    cache = _get_cache(request)
    cache_k = match_curtains_key(req.track_barcode)

    if cache:
        cached = cache.get(cache_k)
        if cached is not None:
            return MatchCurtainsResponse(**cached)

    try:
        result = match_curtains_for_track(db, req.track_barcode)
    except MatchError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if cache:
        cache.set(cache_k, result.model_dump(), ttl=RECOMMEND_TTL)

    return result


@router.get(
    "/installer/{installer_id}/route",
    response_model=InstallerRouteResponse,
    summary="Get optimized installation route for an installer",
    description=(
        "Returns an ordered list of stops (hospital/building/floor/room/track) "
        "optimized to minimize back-and-forth during the installation day."
    ),
)
def api_installer_route(
    installer_id: int,
    route_date: date | None = None,
    request: Request = None,
    db: Session = Depends(get_db),
):
    cache = _get_cache(request) if request else None
    date_str = (route_date or date.today()).isoformat()
    cache_k = route_key(installer_id, date_str)

    if cache:
        cached = cache.get(cache_k)
        if cached is not None:
            return InstallerRouteResponse(**cached)

    result = build_installer_route(db, installer_id, route_date)

    response = InstallerRouteResponse(
        installer_id=result.installer_id,
        route_date=result.route_date,
        total_stops=result.total_stops,
        total_hospitals=result.total_hospitals,
        segments=[
            {
                "hospital_name": seg.hospital_name,
                "hospital_id": seg.hospital_id,
                "stops": [
                    {
                        "order": s.order,
                        "hospital_name": s.hospital_name,
                        "hospital_id": s.hospital_id,
                        "building_name": s.building_name,
                        "building_id": s.building_id,
                        "floor": s.floor,
                        "unit_name": s.unit_name,
                        "room_name": s.room_name,
                        "track_barcode": s.track_barcode,
                        "track_id": s.track_id,
                        "pending_curtains": s.pending_curtains,
                    }
                    for s in seg.stops
                ],
                "total_tracks": seg.total_tracks,
            }
            for seg in result.segments
        ],
        message=result.message,
    )

    if cache:
        cache.set(cache_k, response.model_dump(), ttl=RECOMMEND_TTL)

    return response


@router.get(
    "/cache/stats",
    response_model=CacheStatsResponse,
    summary="Cache statistics",
)
def cache_stats(request: Request):
    cache = _get_cache(request)
    if cache is None:
        return CacheStatsResponse(total_keys=0, backend="none")
    stats = cache.stats()
    return CacheStatsResponse(
        total_keys=stats.get("total_keys", 0),
        backend=stats.get("backend", "in-memory"),
    )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Service health check",
)
def health(request: Request, db: Session = Depends(get_db)):
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    cache = _get_cache(request)
    cache_ok = cache is not None

    return HealthResponse(
        status="ok" if (db_ok and cache_ok) else "degraded",
        version="0.4.0",
        db_ok=db_ok,
        cache_ok=cache_ok,
        timestamp=datetime.utcnow(),
    )
