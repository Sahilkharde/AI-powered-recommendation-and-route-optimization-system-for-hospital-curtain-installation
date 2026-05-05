"""
Installation Route Optimizer.

Given an installer's assigned visits for a day, produces an optimized
visit order that minimizes back-and-forth between buildings and floors.

Strategy (nearest-neighbor heuristic):
  1. Group all tracks to visit by hospital → building → floor
  2. Order hospitals by total work (most tracks first)
  3. Within each hospital, visit buildings top-to-bottom by floor
  4. Within each floor, visit rooms in sequence
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import (
    HospBuilding,
    HospBuildingRoom,
    HospTrack,
    HospUnit,
    Hospital,
    TrackCurtainService,
)


@dataclass
class RouteStop:
    order: int
    hospital_name: str
    hospital_id: int
    building_name: str
    building_id: int
    floor: int
    unit_name: str
    room_name: str
    track_barcode: str
    track_id: int
    pending_curtains: int


@dataclass
class RouteSegment:
    hospital_name: str
    hospital_id: int
    stops: list[RouteStop] = field(default_factory=list)
    total_tracks: int = 0


@dataclass
class InstallerRoute:
    installer_id: int
    route_date: str
    total_stops: int
    total_hospitals: int
    segments: list[RouteSegment]
    message: str


def build_installer_route(
    db: Session,
    installer_id: int,
    route_date: date | None = None,
) -> InstallerRoute:
    target_date = route_date or date.today()

    track_rows = _get_installer_tracks(db, installer_id, target_date)

    if not track_rows:
        return InstallerRoute(
            installer_id=installer_id,
            route_date=target_date.isoformat(),
            total_stops=0,
            total_hospitals=0,
            segments=[],
            message=f"No assigned visits found for installer {installer_id} on {target_date}.",
        )

    by_hospital: dict[int, list] = defaultdict(list)
    for row in track_rows:
        by_hospital[row.Hospital.HID].append(row)

    segments: list[RouteSegment] = []
    global_order = 0

    sorted_hospitals = sorted(
        by_hospital.items(),
        key=lambda item: len(item[1]),
        reverse=True,
    )

    for hospital_id, rows in sorted_hospitals:
        hospital = rows[0].Hospital
        segment = RouteSegment(
            hospital_name=hospital.Name or "",
            hospital_id=hospital.HID,
        )

        sorted_rows = sorted(
            rows,
            key=lambda r: (r.HospBuilding.Name or "", r.HospUnit.Floor or 0, r.HospBuildingRoom.RoomNumber or ""),
        )

        for row in sorted_rows:
            global_order += 1
            pending = _count_pending_for_track(db, row.HospTrack.TrackBarCode)
            segment.stops.append(RouteStop(
                order=global_order,
                hospital_name=hospital.Name or "",
                hospital_id=hospital.HID,
                building_name=row.HospBuilding.Name or "",
                building_id=row.HospBuilding.BID,
                floor=row.HospUnit.Floor or 0,
                unit_name=row.HospUnit.unit_name,
                room_name=row.HospBuildingRoom.RoomNumber or "",
                track_barcode=row.HospTrack.TrackBarCode or "",
                track_id=row.HospTrack.HospTrackId,
                pending_curtains=pending,
            ))

        segment.total_tracks = len(segment.stops)
        segments.append(segment)

    total_stops = sum(s.total_tracks for s in segments)

    msg_parts = []
    for seg in segments:
        msg_parts.append(f"{seg.hospital_name} ({seg.total_tracks} tracks)")
    route_summary = " -> ".join(msg_parts)

    return InstallerRoute(
        installer_id=installer_id,
        route_date=target_date.isoformat(),
        total_stops=total_stops,
        total_hospitals=len(segments),
        segments=segments,
        message=f"Route: {route_summary}. {total_stops} total stops.",
    )


def _get_installer_tracks(db: Session, installer_id: int, target_date: date):
    """
    Find all tracks the installer needs to visit.
    Uses Track_Curtain_Services.Installed_By to match installer.
    """
    installer_str = str(installer_id)

    track_barcodes_sub = (
        db.query(TrackCurtainService.TrackBarCode)
        .filter(TrackCurtainService.Installed_By == installer_str)
        .filter(TrackCurtainService.TrackBarCode.isnot(None))
        .distinct()
        .subquery()
    )

    rows = (
        db.query(HospTrack, HospBuildingRoom, HospUnit, HospBuilding, Hospital)
        .join(HospBuildingRoom, HospTrack.RoomId == HospBuildingRoom.RoomID)
        .join(HospUnit, HospTrack.HUID == HospUnit.HUID)
        .join(HospBuilding, HospUnit.BID == HospBuilding.BID)
        .join(Hospital, HospBuilding.HID == Hospital.HID)
        .filter(HospTrack.TrackBarCode.in_(
            db.query(track_barcodes_sub.c.TrackBarCode)
        ))
        .filter(HospTrack.Enabled == True)   # noqa: E712
        .filter(HospUnit.Enabled == True)    # noqa: E712
        .all()
    )
    return rows


def _count_pending_for_track(db: Session, track_barcode: str | None) -> int:
    if not track_barcode:
        return 0
    result = (
        db.query(func.count(TrackCurtainService.ID))
        .filter(TrackCurtainService.TrackBarCode == track_barcode)
        .scalar()
    )
    return result or 0
