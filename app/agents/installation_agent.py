"""
AI Automation Hospital Installation Agent.

Powered by Snowflake Cortex AI. When an installer scans a curtain barcode,
this agent:
  1. Looks up the curtain (type, style, status, hospital)
  2. Fetches its installation history (where has it gone before?)
  3. Runs the scored recommendation engine
  4. Calls Cortex COMPLETE to produce an installer-friendly explanation

The deterministic scoring engine (engine/recommender.py) does the heavy
lifting. Cortex AI adds contextual reasoning and produces clear explanations.

When Snowflake is not configured (local SQLite dev), the agent returns the
raw recommendation data without an LLM explanation.
"""

import json
import logging
from collections import Counter

from sqlalchemy.orm import Session

from app.config import CORTEX_MODEL, IS_SNOWFLAKE, SPECIAL_HOSPITAL_DISPOSABLE, SPECIAL_HOSPITAL_SPARE
from app.engine.recommender import RecommenderError, suggest_location
from app.models import (
    HospBuilding,
    HospBuildingRoom,
    HospCurtain,
    HospTrack,
    HospUnit,
    Hospital,
    TrackCurtainService,
)

logger = logging.getLogger(__name__)

# ── Prompt template ──────────────────────────────────────────────────────────

AGENT_PROMPT_TEMPLATE = """\
You are an AI installation assistant for AI Automation Hospital, a curtain installation \
management system serving hospitals.

An installer just scanned curtain barcode: {barcode}

Below is all the data gathered from the system. Use it to tell the installer \
EXACTLY where to install this curtain.

## Curtain Details
{curtain_json}

## Installation History
{history_json}

## Scored Recommendations (ranked by confidence)
{recommendations_json}

## Business Rules
- Regular hospital curtains -> ONLY install in their own hospital (Rule R1)
- Hospital 99 curtains (disposable) -> install ANYWHERE, no bag needed (Rule R9)
- Hospital 1001 curtains (spare) -> install ANYWHERE
- Style mismatch -> WARN the installer but DO NOT block (Rule R7)
- Type mismatch (snap vs standard) -> WARN but DO NOT block (Rule R8)

Based on the above data, give the installer a short, actionable answer. Use this format:

INSTALL HERE:
  Building : <name>
  Floor    : <number>
  Unit     : <ward/unit name>
  Room     : <room name>
  Track    : <track barcode>
  Confidence: <score>/100

WHY: <1-2 sentences explaining the recommendation>

WARNINGS: <list any style/type mismatches, or "None">

If recommendations is empty or an error occurred, clearly explain what the \
problem is (e.g. curtain not found, wrong status).
"""


# ── Agent entry point ─────────────────────────────────────────────────────────


def run_agent(db: Session, curtain_barcode: str) -> dict:
    curtain_data = _tool_lookup_curtain(db, curtain_barcode)
    if "error" in curtain_data:
        return {
            "curtain_barcode": curtain_barcode,
            "recommendation": None,
            "agent_explanation": curtain_data["error"],
        }

    barcode_int = curtain_data.get("barcode")
    history_data = _tool_get_install_history(db, barcode_int) if barcode_int else {}
    recommendation_data = _tool_get_recommendations(db, curtain_barcode)

    agent_explanation = _call_cortex(
        curtain_barcode, curtain_data, history_data, recommendation_data
    )

    return {
        "curtain_barcode": curtain_barcode,
        "recommendation": recommendation_data,
        "agent_explanation": agent_explanation,
    }


def _call_cortex(
    barcode: str,
    curtain_data: dict,
    history_data: dict,
    recommendation_data: dict,
) -> str:
    prompt = AGENT_PROMPT_TEMPLATE.format(
        barcode=barcode,
        curtain_json=json.dumps(curtain_data, indent=2, default=str),
        history_json=json.dumps(history_data, indent=2, default=str),
        recommendations_json=json.dumps(recommendation_data, indent=2, default=str),
    )

    if not IS_SNOWFLAKE:
        return _fallback_explanation(recommendation_data)

    try:
        from snowflake.cortex import complete

        from app.database import get_snowflake_session

        session = get_snowflake_session()
        if session is None:
            logger.warning("Could not create Snowpark session, using fallback explanation")
            return _fallback_explanation(recommendation_data)

        try:
            result = complete(CORTEX_MODEL, prompt, session=session)
            return result if isinstance(result, str) else str(result)
        finally:
            session.close()

    except ImportError:
        logger.warning("snowflake-ml-python not installed, using fallback explanation")
        return _fallback_explanation(recommendation_data)
    except Exception as exc:
        logger.warning("Cortex COMPLETE failed: %s, using fallback", exc)
        return _fallback_explanation(recommendation_data)


def _fallback_explanation(recommendation_data: dict) -> str:
    """Generate a structured explanation without an LLM (for local dev or fallback)."""
    if "error" in recommendation_data:
        return recommendation_data["error"]

    recs = recommendation_data.get("recommendations", [])
    if not recs:
        return "No eligible tracks found for this curtain."

    top = recs[0]
    lines = [
        "INSTALL HERE:",
        f"  Building : {top['building']}",
        f"  Floor    : {top['floor']}",
        f"  Unit     : {top['unit']}",
        f"  Room     : {top['room']}",
        f"  Track    : {top['track_barcode']}",
        f"  Confidence: {top['score']}/100",
        "",
        f"WHY: {top['reason']}",
        "",
    ]

    warnings = top.get("warnings", [])
    if warnings:
        lines.append("WARNINGS:")
        for w in warnings:
            lines.append(f"  - {w}")
    else:
        lines.append("WARNINGS: None")

    return "\n".join(lines)


# ── Data gathering (unchanged from original) ─────────────────────────────────


def _tool_lookup_curtain(db: Session, barcode: str) -> dict:
    barcode_int: int | None = None
    try:
        barcode_int = int(barcode)
    except (ValueError, TypeError):
        pass

    curtain: HospCurtain | None = None
    if barcode_int is not None:
        curtain = db.query(HospCurtain).filter(HospCurtain.CurtBarCode == barcode_int).first()

    if curtain is None:
        return {"error": f"Curtain '{barcode}' not found in the system."}

    hospital = db.query(Hospital).filter(Hospital.HID == curtain.HID).first()

    type_name = ""
    if curtain.curtain_type_ref:
        type_name = curtain.curtain_type_ref.Name or ""

    return {
        "curtain_id": curtain.CID,
        "barcode": curtain.CurtBarCode,
        "curt_type_id": curtain.Curt_TypeID,
        "curt_type_name": type_name,
        "unit_style": curtain.UnitStyle,
        "width_id": curtain.WidthId,
        "height_id": curtain.HeightId,
        "weight": curtain.Weight,
        "hospital_id": curtain.HID,
        "hospital_name": hospital.Name if hospital else "Unknown",
        "is_disposable": curtain.HID == SPECIAL_HOSPITAL_DISPOSABLE,
        "is_spare": curtain.HID == SPECIAL_HOSPITAL_SPARE,
        "is_mesh": curtain.Mesh or False,
        "is_manufacturing": curtain.IsManufecturing or False,
        "enabled": curtain.Enabled,
    }


def _tool_get_install_history(db: Session, curt_barcode: int) -> dict:
    rows = (
        db.query(TrackCurtainService, HospTrack, HospBuildingRoom, HospUnit, HospBuilding, Hospital)
        .join(HospTrack, TrackCurtainService.TrackBarCode == HospTrack.TrackBarCode)
        .join(HospBuildingRoom, HospTrack.RoomId == HospBuildingRoom.RoomID)
        .join(HospUnit, HospTrack.HUID == HospUnit.HUID)
        .join(HospBuilding, HospUnit.BID == HospBuilding.BID)
        .join(Hospital, HospBuilding.HID == Hospital.HID)
        .filter(TrackCurtainService.CurBarCode == curt_barcode)
        .order_by(TrackCurtainService.Installed_Date.desc())
        .limit(20)
        .all()
    )

    if not rows:
        return {
            "curtain_barcode": curt_barcode,
            "total_installs": 0,
            "history": [],
            "note": "No installation history found.",
        }

    history = [
        {
            "installed_at": tcs.Installed_Date.isoformat() if tcs.Installed_Date else None,
            "track_barcode": track.TrackBarCode,
            "room": room.RoomNumber,
            "unit": unit.unit_name,
            "floor": unit.Floor,
            "building": building.Name,
            "hospital": hospital.Name,
        }
        for tcs, track, room, unit, building, hospital in rows
    ]

    track_counts = Counter(h["track_barcode"] for h in history)
    most_common = [{"track": t, "times": c} for t, c in track_counts.most_common(3)]

    return {
        "curtain_barcode": curt_barcode,
        "total_installs": len(rows),
        "most_frequently_installed_on": most_common,
        "recent_history": history[:10],
    }


def _tool_get_recommendations(db: Session, curtain_barcode: str) -> dict:
    try:
        result = suggest_location(db, curtain_barcode)

        recommendations = [
            {
                "rank": r.rank,
                "score": r.score,
                "hospital": r.location.hospital_name,
                "building": r.location.building_name,
                "floor": r.location.floor,
                "unit": r.location.unit_name,
                "room": r.location.room_name,
                "track_barcode": r.location.track_barcode,
                "type_match": r.type_match,
                "style_match": r.style_match,
                "size_match": r.size_match,
                "has_capacity": r.has_capacity,
                "warnings": r.warnings,
                "reason": r.reason,
            }
            for r in result.recommendations[:5]
        ]

        return {
            "curtain_barcode": curtain_barcode,
            "curtain_status": result.curtain_status,
            "curtain_category": result.curtain_category,
            "hospital": result.hospital_name,
            "is_disposable": result.is_disposable,
            "is_spare": result.is_spare,
            "total_candidates_evaluated": result.total_candidates,
            "recommendations": recommendations,
            "top_recommendation_summary": result.message,
        }

    except RecommenderError as e:
        return {"error": str(e), "curtain_barcode": curtain_barcode}
