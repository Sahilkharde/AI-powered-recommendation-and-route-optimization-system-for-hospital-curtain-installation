"""
Track-to-Curtain Matching Engine.

Given a scanned track barcode, finds all curtains that could be installed
on it, ranked by compatibility score.
"""

from sqlalchemy.orm import Session

from app.config import SPECIAL_HOSPITAL_DISPOSABLE, SPECIAL_HOSPITAL_SPARE
from app.engine.rules import (
    check_style_match,
    check_type_match,
    size_compatible,
)
from app.engine.scoring import ScoringInput, build_reason, compute_score
from app.models import (
    HospBuilding,
    HospBuildingRoom,
    HospCurtain,
    HospTrack,
    HospUnit,
    Hospital,
)
from app.schemas import (
    CurtainMatch,
    MatchCurtainsResponse,
)


class MatchError(Exception):
    pass


def match_curtains_for_track(db: Session, track_barcode: str) -> MatchCurtainsResponse:
    track = db.query(HospTrack).filter(HospTrack.TrackBarCode == track_barcode).first()
    if track is None:
        raise MatchError(f"Track with barcode '{track_barcode}' not found.")

    room = db.query(HospBuildingRoom).filter(HospBuildingRoom.RoomID == track.RoomId).first()
    unit = db.query(HospUnit).filter(HospUnit.HUID == track.HUID).first()
    building = db.query(HospBuilding).filter(HospBuilding.BID == unit.BID).first() if unit else None
    hospital = db.query(Hospital).filter(Hospital.HID == building.HID).first() if building else None

    if not all([room, unit, building, hospital]):
        raise MatchError(f"Could not resolve location hierarchy for track '{track_barcode}'.")

    candidates = _get_candidate_curtains(db, hospital.HID)

    track_length = track.length_value
    track_height = track.height_value
    type_name = ""
    if track.curtain_type_ref:
        type_name = track.curtain_type_ref.Name or ""

    if not candidates:
        return MatchCurtainsResponse(
            track_barcode=track_barcode,
            track_type=type_name,
            track_length=track_length or 0,
            track_height=track_height or 0,
            hospital_name=hospital.Name or "",
            building_name=building.Name or "",
            floor=unit.Floor or 0,
            room_name=room.RoomNumber or "",
            matches=[],
            total_candidates=0,
            message="No available curtains found for this track.",
        )

    matches: list[CurtainMatch] = []

    for curtain in candidates:
        curtain_width = float(curtain.WidthId) if curtain.WidthId else None
        curtain_height = float(curtain.HeightId) if curtain.HeightId else None

        size_delta = abs(curtain_width - track_length) if curtain_width and track_length else 0
        s_compat = size_compatible(curtain_width, track_length)
        type_match = curtain.Curt_TypeID == track.Curt_TypeId
        style_match = (curtain.UnitStyle is not None and unit.Style is not None
                       and curtain.UnitStyle == unit.Style)

        scoring_input = ScoringInput(
            history_count=0,
            max_history=1,
            size_delta=size_delta,
            size_tolerance=2.0,
            type_match=type_match,
            style_match=style_match,
            days_since_last_install=None,
            has_capacity=True,
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
        if not s_compat and curtain_width and track_length:
            warnings.append(
                f"Size mismatch: curtain width {curtain_width} vs track length {track_length} "
                f"(delta {size_delta:.1f})."
            )

        curt_type_name = ""
        if curtain.curtain_type_ref:
            curt_type_name = curtain.curtain_type_ref.Name or ""

        category = "hospital"
        if curtain.IsManufecturing:
            category = "manufacturing"
        elif curtain.Mesh:
            category = "regular_mesh"

        matches.append(CurtainMatch(
            curtain_barcode=curtain.barcode_str,
            curtain_id=curtain.CID,
            curtain_category=category,
            curtain_type=curt_type_name,
            width=curtain_width or 0,
            height=curtain_height or 0,
            status="available",
            score=score,
            is_best_match=False,
            reason=reason,
            warnings=warnings,
        ))

    matches.sort(key=lambda m: m.score, reverse=True)
    if matches:
        matches[0].is_best_match = True

    top_n = matches[:15]

    best = top_n[0] if top_n else None
    msg = (
        f"Best match: curtain {best.curtain_barcode} "
        f"(score {best.score}/100, {best.curtain_type}, {best.width} wide)."
    ) if best else "No matching curtains available."

    return MatchCurtainsResponse(
        track_barcode=track_barcode,
        track_type=type_name,
        track_length=track_length or 0,
        track_height=track_height or 0,
        hospital_name=hospital.Name or "",
        building_name=building.Name or "",
        floor=unit.Floor or 0,
        room_name=room.RoomNumber or "",
        matches=top_n,
        total_candidates=len(matches),
        message=msg,
    )


def _get_candidate_curtains(db: Session, hospital_id: int) -> list[HospCurtain]:
    return (
        db.query(HospCurtain)
        .filter(
            HospCurtain.HID.in_([
                hospital_id,
                SPECIAL_HOSPITAL_DISPOSABLE,
                SPECIAL_HOSPITAL_SPARE,
            ])
        )
        .filter(HospCurtain.Enabled == True)  # noqa: E712
        .all()
    )
