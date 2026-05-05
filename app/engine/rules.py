"""
AI Automation Hospital Business Rules (R1-R12).

These are hard constraints that the recommendation engine must respect.
Every recommendation is filtered and annotated through these rules before
being returned to the caller.
"""

from app.config import (
    MAX_CURTAINS_PER_BAG,
    SPECIAL_HOSPITAL_DISPOSABLE,
    SPECIAL_HOSPITAL_SPARE,
)
from app.models import HospCurtain, HospTrack, HospUnit, Hospital


def is_special_hospital(hospital: Hospital) -> bool:
    return hospital.HID in (SPECIAL_HOSPITAL_DISPOSABLE, SPECIAL_HOSPITAL_SPARE)


def is_disposable_curtain(curtain: HospCurtain) -> bool:
    return curtain.HID == SPECIAL_HOSPITAL_DISPOSABLE


def is_spare_curtain(curtain: HospCurtain) -> bool:
    return curtain.HID == SPECIAL_HOSPITAL_SPARE


# ── R1: Hospital curtains stay in their own hospital ─────────────────────────
def can_install_in_hospital(curtain: HospCurtain, target_hospital_id: int) -> bool:
    """
    Regular curtains can only go to their own hospital.
    Hospital 99 (disposable) and 1001 (spare) curtains can go anywhere.
    """
    if curtain.HID in (SPECIAL_HOSPITAL_DISPOSABLE, SPECIAL_HOSPITAL_SPARE):
        return True
    return curtain.HID == target_hospital_id


# ── R2: Only packable curtains can be installed ──────────────────────────────
def is_packable_status(cur_status_id: int | None, packable_ids: set[int]) -> bool:
    """Check if the curtain's current status ID is in the packable set."""
    if not packable_ids:
        return True
    if cur_status_id is None:
        return True
    return cur_status_id in packable_ids


# ── R4: Max 15 curtains per bag ──────────────────────────────────────────────
def bag_has_capacity(current_count: int) -> bool:
    return current_count < MAX_CURTAINS_PER_BAG


# ── R6: Track barcode starts with hospital account number ────────────────────
def track_belongs_to_hospital(track_barcode: str, account_number: int | None) -> bool:
    if account_number is None:
        return False
    return track_barcode.startswith(str(account_number))


# ── R7: Style mismatch → warning, not block ──────────────────────────────────
def check_style_match(curtain: HospCurtain, unit: HospUnit) -> str | None:
    """Compare curtain UnitStyle to unit Style (both int IDs)."""
    if curtain.UnitStyle is not None and unit.Style is not None:
        if curtain.UnitStyle != unit.Style:
            return (
                f"Style mismatch: curtain style ID {curtain.UnitStyle} "
                f"but unit '{unit.unit_name}' style ID {unit.Style}. "
                "Installation allowed but confirm with installer."
            )
    return None


# ── R8: Curtain type mismatch on track → warning, not block ─────────────────
def check_type_match(curtain: HospCurtain, track: HospTrack) -> str | None:
    """Compare Curt_TypeID between curtain and track."""
    if curtain.Curt_TypeID is not None and track.Curt_TypeId is not None:
        if curtain.Curt_TypeID != track.Curt_TypeId:
            curt_name = ""
            track_name = ""
            if curtain.curtain_type_ref:
                curt_name = curtain.curtain_type_ref.Name or ""
            if track.curtain_type_ref:
                track_name = track.curtain_type_ref.Name or ""
            return (
                f"Type mismatch: curtain is '{curt_name}' "
                f"but track expects '{track_name}'. "
                "Installation allowed but confirm with installer."
            )
    return None


# ── R9: Disposable curtains need no bag ──────────────────────────────────────
def needs_bag(curtain: HospCurtain) -> bool:
    return not is_disposable_curtain(curtain)


# ── R10: Hospital isTempStorage → Allow Team Storage ─────────────────────────
def is_temp_storage_hospital(hospital: Hospital) -> bool:
    return hospital.isTempStorage


# ── Track capacity ───────────────────────────────────────────────────────────
def track_has_capacity(
    track: HospTrack,
    current_installed: int,
    curtain: HospCurtain,
) -> bool:
    max_regular = track.NumberOfCurtain or 0
    max_spare = track.NumberOfSpares or 0
    max_disposable = track.NumberOfDisposables or 0

    if is_disposable_curtain(curtain):
        return current_installed < max_disposable + max_regular
    if is_spare_curtain(curtain):
        return current_installed < max_spare + max_regular
    return current_installed < max_regular


def size_compatible(curtain_width: float | None, track_length: float | None, tolerance: float = 2.0) -> bool:
    """Width must be within tolerance inches of the track length."""
    if curtain_width is None or track_length is None:
        return True
    return abs(curtain_width - track_length) <= tolerance
