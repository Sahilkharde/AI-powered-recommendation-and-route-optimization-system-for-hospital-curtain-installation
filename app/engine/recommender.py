"""
Curtain Installation Recommender.

Given a scanned curtain barcode, determines which building / floor / room / track
the curtain should be installed on, ranked by confidence score.
"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.config import HISTORY_WINDOW_SIZE, SPECIAL_HOSPITAL_DISPOSABLE, SPECIAL_HOSPITAL_SPARE
from app.engine.rules import (
    can_install_in_hospital,
    check_style_match,
    check_type_match,
    is_disposable_curtain,
    is_spare_curtain,
    size_compatible,
    track_has_capacity,
)
from app.engine.scoring import ScoringInput, build_reason, compute_score
from app.models import (
    HospBuilding,
    HospBuildingRoom,
    HospCurtain,
    HospTrack,
    HospUnit,
    Hospital,
    TrackCurtainService,
)
from app.schemas import (
    LocationDetail,
    SuggestLocationResponse,
    TrackRecommendation,
)


class RecommenderError(Exception):
    pass


def _resolve_curtain_width(curtain: HospCurtain) -> float | None:
    """
    Resolve the curtain's width. WidthId references Curt_Width lookup;
    for now we use it as an approximate numeric value if no relationship loaded.
    """
    if curtain.WidthId is not None:
        return float(curtain.WidthId)
    return None


def suggest_location(db: Session, curtain_barcode: str) -> SuggestLocationResponse:
    barcode_int: int | None = None
    try:
        barcode_int = int(curtain_barcode)
    except (ValueError, TypeError):
        pass

    curtain: HospCurtain | None = None
    if barcode_int is not None:
        curtain = (
            db.query(HospCurtain)
            .options(joinedload(HospCurtain.hospital))
            .filter(HospCurtain.CurtBarCode == barcode_int)
            .first()
        )

    if curtain is None:
        raise RecommenderError(f"Curtain with barcode '{curtain_barcode}' not found.")

    hospital = curtain.hospital
    is_disp = is_disposable_curtain(curtain)
    is_spr = is_spare_curtain(curtain)

    candidate_tracks = _get_candidate_tracks(db, curtain, hospital)
    if not candidate_tracks:
        return SuggestLocationResponse(
            curtain_barcode=curtain_barcode,
            curtain_status="unknown",
            curtain_category=_curtain_category(curtain),
            hospital_name=hospital.Name or "",
            is_disposable=is_disp,
            is_spare=is_spr,
            recommendations=[],
            total_candidates=0,
            message="No eligible tracks found for this curtain.",
        )

    history_map = _get_history_map(db, curtain.CurtBarCode)
    max_history = max(history_map.values()) if history_map else 1
    last_install_map = _get_last_install_dates(db, curtain.CurtBarCode)

    track_ids = [t.HospTrack.HospTrackId for t in candidate_tracks]
    installed_counts = _get_installed_counts(db, track_ids)

    curtain_width = _resolve_curtain_width(curtain)

    recommendations: list[TrackRecommendation] = []

    for track_row in candidate_tracks:
        track: HospTrack = track_row.HospTrack
        room: HospBuildingRoom = track_row.HospBuildingRoom
        unit: HospUnit = track_row.HospUnit
        building: HospBuilding = track_row.HospBuilding
        target_hospital: Hospital = track_row.Hospital

        current_installed = installed_counts.get(track.HospTrackId, 0)
        has_cap = track_has_capacity(track, current_installed, curtain)

        track_length = track.length_value
        size_delta = abs(curtain_width - track_length) if curtain_width and track_length else 0
        s_compat = size_compatible(curtain_width, track_length)

        type_match = curtain.Curt_TypeID == track.Curt_TypeId
        style_match = (curtain.UnitStyle is not None and unit.Style is not None
                       and curtain.UnitStyle == unit.Style)

        barcode_key = track.TrackBarCode or str(track.HospTrackId)
        days_since = None
        if barcode_key in last_install_map:
            delta = datetime.utcnow() - last_install_map[barcode_key]
            days_since = delta.days

        scoring_input = ScoringInput(
            history_count=history_map.get(barcode_key, 0),
            max_history=max_history,
            size_delta=size_delta,
            size_tolerance=2.0,
            type_match=type_match,
            style_match=style_match,
            days_since_last_install=days_since,
            has_capacity=has_cap,
        )
        score = compute_score(scoring_input)
        reason = build_reason(scoring_input, score)

        warnings: list[str] = []
        style_warn = check_style_match(curtain, unit)
        if style_warn:
            warnings.append(style_warn)
        type_warn = check_type_match(curtain, track)
        if type_warn:
            warnings.append(type_warn)
        if not has_cap:
            warnings.append(
                f"Track {track.TrackBarCode} is at max capacity ({current_installed} installed)."
            )
        if not s_compat and curtain_width and track_length:
            warnings.append(
                f"Size mismatch: curtain width {curtain_width} vs track length {track_length} "
                f"(delta {size_delta:.1f})."
            )

        recommendations.append(TrackRecommendation(
            rank=0,
            location=LocationDetail(
                hospital_name=target_hospital.Name or "",
                hospital_id=target_hospital.HID,
                building_name=building.Name or "",
                building_id=building.BID,
                floor=unit.Floor or 0,
                unit_name=unit.unit_name,
                unit_id=unit.HUID,
                room_name=room.RoomNumber or "",
                room_id=room.RoomID,
                track_barcode=track.TrackBarCode or "",
                track_id=track.HospTrackId,
            ),
            score=score,
            reason=reason,
            type_match=type_match,
            style_match=style_match,
            size_match=s_compat,
            has_capacity=has_cap,
            warnings=warnings,
        ))

    recommendations.sort(key=lambda r: r.score, reverse=True)
    for idx, rec in enumerate(recommendations, start=1):
        rec.rank = idx

    top_n = recommendations[:10]

    best = top_n[0].location if top_n else None
    msg = (
        f"Top recommendation: install in {best.building_name}, "
        f"Floor {best.floor}, {best.room_name}, Track {best.track_barcode} "
        f"(score {top_n[0].score}/100)."
    ) if best else "No recommendations available."

    return SuggestLocationResponse(
        curtain_barcode=curtain_barcode,
        curtain_status="available",
        curtain_category=_curtain_category(curtain),
        hospital_name=hospital.Name or "",
        is_disposable=is_disp,
        is_spare=is_spr,
        recommendations=top_n,
        total_candidates=len(recommendations),
        message=msg,
    )


def _curtain_category(curtain: HospCurtain) -> str:
    if curtain.IsManufecturing:
        return "manufacturing"
    if curtain.Mesh:
        return "regular_mesh"
    return "hospital"


def _get_candidate_tracks(db: Session, curtain: HospCurtain, hospital: Hospital):
    query = (
        db.query(
            HospTrack,
            HospBuildingRoom,
            HospUnit,
            HospBuilding,
            Hospital,
        )
        .join(HospBuildingRoom, HospTrack.RoomId == HospBuildingRoom.RoomID)
        .join(HospUnit, HospTrack.HUID == HospUnit.HUID)
        .join(HospBuilding, HospUnit.BID == HospBuilding.BID)
        .join(Hospital, HospBuilding.HID == Hospital.HID)
        .filter(HospTrack.Enabled == True)  # noqa: E712
        .filter(HospUnit.Enabled == True)   # noqa: E712
    )

    if curtain.HID not in (SPECIAL_HOSPITAL_DISPOSABLE, SPECIAL_HOSPITAL_SPARE):
        query = query.filter(Hospital.HID == hospital.HID)

    return query.all()


def _get_history_map(db: Session, curt_barcode: int | None) -> dict[str, int]:
    """TrackBarCode → install count for this curtain barcode."""
    if curt_barcode is None:
        return {}
    rows = (
        db.query(
            TrackCurtainService.TrackBarCode,
            func.count(TrackCurtainService.ID).label("cnt"),
        )
        .filter(TrackCurtainService.CurBarCode == curt_barcode)
        .filter(TrackCurtainService.TrackBarCode.isnot(None))
        .group_by(TrackCurtainService.TrackBarCode)
        .order_by(func.count(TrackCurtainService.ID).desc())
        .limit(HISTORY_WINDOW_SIZE)
        .all()
    )
    return {row.TrackBarCode: row.cnt for row in rows}


def _get_last_install_dates(db: Session, curt_barcode: int | None) -> dict[str, datetime]:
    """TrackBarCode → most recent installation date for this curtain."""
    if curt_barcode is None:
        return {}
    rows = (
        db.query(
            TrackCurtainService.TrackBarCode,
            func.max(TrackCurtainService.Installed_Date).label("latest"),
        )
        .filter(TrackCurtainService.CurBarCode == curt_barcode)
        .filter(TrackCurtainService.TrackBarCode.isnot(None))
        .filter(TrackCurtainService.Installed_Date.isnot(None))
        .group_by(TrackCurtainService.TrackBarCode)
        .all()
    )
    return {row.TrackBarCode: row.latest for row in rows if row.latest}


def _get_installed_counts(db: Session, track_ids: list[int]) -> dict[int, int]:
    """HospTrackId → current number of curtains installed (via TrackBarCode join)."""
    if not track_ids:
        return {}

    track_barcodes_sub = (
        db.query(HospTrack.TrackBarCode)
        .filter(HospTrack.HospTrackId.in_(track_ids))
        .filter(HospTrack.TrackBarCode.isnot(None))
        .subquery()
    )

    rows = (
        db.query(
            TrackCurtainService.TrackBarCode,
            func.count(TrackCurtainService.ID).label("cnt"),
        )
        .filter(TrackCurtainService.TrackBarCode.in_(
            db.query(track_barcodes_sub.c.TrackBarCode)
        ))
        .group_by(TrackCurtainService.TrackBarCode)
        .all()
    )

    barcode_to_count = {row.TrackBarCode: row.cnt for row in rows}

    barcode_to_id = {}
    for t_row in db.query(HospTrack.HospTrackId, HospTrack.TrackBarCode).filter(
        HospTrack.HospTrackId.in_(track_ids)
    ).all():
        barcode_to_id[t_row.TrackBarCode] = t_row.HospTrackId

    result: dict[int, int] = {}
    for barcode, cnt in barcode_to_count.items():
        if barcode in barcode_to_id:
            result[barcode_to_id[barcode]] = cnt
    return result
