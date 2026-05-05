"""
Seed the local SQLite database with sample AI Automation Hospital data.

Creates hospitals, buildings, units, rooms, tracks, curtains, and
Track_Curtain_Services records so the AI agent can be tested locally.

NOTE: When connected to the real SQL Server (UATAI Automation Hospital), seeding is
not needed — the production data is already present.
"""

import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal, init_db
from app.models import (
    CurtGrommets,
    CurtHeight,
    CurtStatus,
    CurtType,
    CurtWidth,
    HospBuilding,
    HospBuildingRoom,
    HospCurtain,
    HospTrack,
    HospUnit,
    Hospital,
    TrackCurtainService,
    TrackType,
    UnitLookup,
)


def seed():
    init_db()
    db = SessionLocal()

    if db.query(Hospital).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    try:
        _seed_data(db)
        db.commit()
        print("Database seeded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def _seed_data(db: Session):
    # ── Lookup tables ─────────────────────────────────────────────────────
    curt_types = [
        CurtType(Curt_TypeID=1, Name="Standard", SortIndex=1, Enabled=True),
        CurtType(Curt_TypeID=2, Name="Snap", SortIndex=2, Enabled=True),
        CurtType(Curt_TypeID=3, Name="Psyc", SortIndex=3, Enabled=True),
    ]
    db.add_all(curt_types)

    track_types = [
        TrackType(TrackTypeId=1, Name="Straight", SortIndex=1, Enabled=True),
        TrackType(TrackTypeId=2, Name="L-Shape", SortIndex=2, Enabled=True),
        TrackType(TrackTypeId=3, Name="U-Shape", SortIndex=3, Enabled=True),
    ]
    db.add_all(track_types)

    widths = [
        CurtWidth(WidthID=1, Description="36", SortIndex=1, Enabled=True),
        CurtWidth(WidthID=2, Description="48", SortIndex=2, Enabled=True),
        CurtWidth(WidthID=3, Description="60", SortIndex=3, Enabled=True),
        CurtWidth(WidthID=4, Description="72", SortIndex=4, Enabled=True),
        CurtWidth(WidthID=5, Description="84", SortIndex=5, Enabled=True),
        CurtWidth(WidthID=6, Description="96", SortIndex=6, Enabled=True),
    ]
    db.add_all(widths)

    heights = [
        CurtHeight(HeightID=1, Description="72", SortIndex=1, Enabled=True),
        CurtHeight(HeightID=2, Description="84", SortIndex=2, Enabled=True),
        CurtHeight(HeightID=3, Description="96", SortIndex=3, Enabled=True),
        CurtHeight(HeightID=4, Description="108", SortIndex=4, Enabled=True),
    ]
    db.add_all(heights)

    statuses = [
        CurtStatus(StatusID=1, Description="Curtain Setup", SortIndex=1, Enabled=True),
        CurtStatus(StatusID=2, Description="Clean", SortIndex=2, Enabled=True),
        CurtStatus(StatusID=3, Description="Soiled", SortIndex=3, Enabled=True),
        CurtStatus(StatusID=4, Description="Installed", SortIndex=4, Enabled=True),
        CurtStatus(StatusID=5, Description="Delivered", SortIndex=5, Enabled=True),
    ]
    db.add_all(statuses)

    grommets = [
        CurtGrommets(GoormateID=1, Description="Standard", SortIndex=1, Enabled=True),
        CurtGrommets(GoormateID=2, Description="Snap", SortIndex=2, Enabled=True),
    ]
    db.add_all(grommets)

    unit_lookups = [
        UnitLookup(UnitId=1, Name="ICU", SortIndex=1, Enabled=True),
        UnitLookup(UnitId=2, Name="General Ward", SortIndex=2, Enabled=True),
        UnitLookup(UnitId=3, Name="Surgical Ward", SortIndex=3, Enabled=True),
        UnitLookup(UnitId=4, Name="Recovery Wing", SortIndex=4, Enabled=True),
        UnitLookup(UnitId=5, Name="Emergency", SortIndex=5, Enabled=True),
        UnitLookup(UnitId=6, Name="Pediatrics", SortIndex=6, Enabled=True),
        UnitLookup(UnitId=7, Name="Cardiology", SortIndex=7, Enabled=True),
        UnitLookup(UnitId=8, Name="Maternity", SortIndex=8, Enabled=True),
        UnitLookup(UnitId=9, Name="Orthopedics", SortIndex=9, Enabled=True),
    ]
    db.add_all(unit_lookups)
    db.flush()

    # ── Special hospitals ─────────────────────────────────────────────────
    h99 = Hospital(
        HID=99, Name="AI Automation Hospital Disposable",
        HasDisposable=True, Enabled=True,
    )
    h1001 = Hospital(
        HID=1001, Name="AI Automation Hospital Spare Curtains",
        HasAIAutomationHospitalSpares=True, Enabled=True,
    )
    db.add_all([h99, h1001])

    # ── Regular hospitals ─────────────────────────────────────────────────
    hospitals_data = [
        (1001 + 1, "Florida General Hospital", 1576, False, True),
        (1001 + 2, "Orlando Regional Medical", 2301, True, True),
        (1001 + 3, "Tampa Bay Community Hospital", 3042, False, False),
    ]

    hospitals: list[Hospital] = []
    for hid, name, acct, temp_storage, has_disp in hospitals_data:
        h = Hospital(
            HID=hid, Name=name, AccountNumber=acct,
            isTempStorage=temp_storage, HasDisposable=has_disp,
            Enabled=True,
        )
        db.add(h)
        hospitals.append(h)

    db.flush()

    # ── Buildings / Units / Rooms / Tracks ────────────────────────────────
    buildings_spec = {
        1002: [
            ("Cancer Care Block", 4, [
                (1, 1, 1, [("101", 1), ("102", 1), ("103", 2)]),
                (2, 2, 1, [("201", 1), ("202", 1)]),
                (3, 3, 2, [("301", 2), ("302", 2)]),
                (4, 4, 1, [("401", 1)]),
            ]),
            ("Bone Block", 2, [
                (9, 1, 1, [("101", 1), ("102", 1)]),
                (4, 2, 2, [("201", 2)]),
            ]),
        ],
        1003: [
            ("Main Building", 5, [
                (5, 1, 1, [("101", 1), ("102", 1), ("103", 1)]),
                (6, 2, 1, [("201", 1), ("202", 2)]),
                (7, 3, 2, [("301", 2), ("302", 2), ("303", 2)]),
            ]),
        ],
        1004: [
            ("West Wing", 3, [
                (8, 1, 1, [("101", 1), ("102", 1)]),
                (2, 2, 2, [("201", 2), ("202", 2)]),
                (2, 3, 1, [("301", 1)]),
            ]),
        ],
    }

    all_tracks: list[HospTrack] = []
    track_counter = 0

    for hosp in hospitals:
        if hosp.HID not in buildings_spec:
            continue
        for bname, floors, units_data in buildings_spec[hosp.HID]:
            building = HospBuilding(
                HID=hosp.HID, Name=bname, TotalFloor=floors, Enabled=True
            )
            db.add(building)
            db.flush()

            for unit_id, floor, style, rooms_data in units_data:
                unit = HospUnit(
                    BID=building.BID, UnitID=unit_id, Floor=floor,
                    Style=style,
                    CellingHeight=str(round(random.uniform(8, 12), 1)),
                    Enabled=True,
                )
                db.add(unit)
                db.flush()

                for room_num, curt_type_id in rooms_data:
                    room = HospBuildingRoom(
                        HUID=unit.HUID, RoomNumber=room_num, Enabled=True
                    )
                    db.add(room)
                    db.flush()

                    track_counter += 1
                    acct = hosp.AccountNumber or hosp.HID
                    barcode = f"{acct}-T{track_counter:04d}"
                    length = round(random.uniform(36, 96), 1)
                    height = round(random.uniform(72, 108), 1)

                    track = HospTrack(
                        HUID=unit.HUID,
                        RoomId=room.RoomID,
                        TrackBarCode=barcode,
                        TrackTypeID=1,
                        Length=str(length),
                        Height=str(height),
                        Curt_TypeId=curt_type_id,
                        NumberOfCurtain=random.randint(1, 3),
                        NumberOfSpares=1,
                        NumberOfDisposables=1,
                        Enabled=True,
                    )
                    db.add(track)
                    db.flush()
                    all_tracks.append(track)

    # ── Curtains ──────────────────────────────────────────────────────────
    all_curtains: list[HospCurtain] = []
    curtain_counter = 1000

    for hosp in hospitals:
        hosp_tracks = [t for t in all_tracks if t.TrackBarCode and
                       t.TrackBarCode.startswith(str(hosp.AccountNumber or hosp.HID))]
        num_curtains = len(hosp_tracks) * 3

        for i in range(num_curtains):
            curtain_counter += 1
            ref_track = random.choice(hosp_tracks) if hosp_tracks else None
            c_type = ref_track.Curt_TypeId if ref_track else 1
            width_id = random.randint(1, 6)
            height_id = random.randint(1, 4)

            curtain = HospCurtain(
                HID=hosp.HID,
                Hosp_CurtID=curtain_counter,
                CurtBarCode=curtain_counter,
                PatternID=1,
                Curt_TypeID=c_type,
                GrommetID=1,
                WidthId=width_id,
                HeightId=height_id,
                UnitStyle=random.choice([1, 1, 1, 2]),
                Enabled=True,
            )
            db.add(curtain)
            db.flush()
            all_curtains.append(curtain)

    # ── Spare curtains (Hospital 1001) ────────────────────────────────────
    for i in range(20):
        curtain_counter += 1
        curtain = HospCurtain(
            HID=1001,
            Hosp_CurtID=curtain_counter,
            CurtBarCode=curtain_counter,
            PatternID=1,
            Curt_TypeID=random.choice([1, 2]),
            GrommetID=1,
            WidthId=random.randint(1, 6),
            HeightId=random.randint(1, 4),
            UnitStyle=1,
            Enabled=True,
        )
        db.add(curtain)
        db.flush()
        all_curtains.append(curtain)

    # ── Disposable curtains (Hospital 99) ─────────────────────────────────
    for i in range(15):
        curtain_counter += 1
        curtain = HospCurtain(
            HID=99,
            Hosp_CurtID=curtain_counter,
            CurtBarCode=curtain_counter,
            PatternID=1,
            Curt_TypeID=random.choice([1, 2]),
            GrommetID=1,
            WidthId=random.randint(1, 6),
            HeightId=random.randint(1, 4),
            UnitStyle=1,
            Enabled=True,
        )
        db.add(curtain)
        db.flush()
        all_curtains.append(curtain)

    # ── Track_Curtain_Services (installation history) ─────────────────────
    hospital_curtains: dict[int, list[HospCurtain]] = {}
    for c in all_curtains:
        hospital_curtains.setdefault(c.HID, []).append(c)

    now = datetime.utcnow()

    for hosp in hospitals:
        hosp_tracks = [t for t in all_tracks if t.TrackBarCode and
                       t.TrackBarCode.startswith(str(hosp.AccountNumber or hosp.HID))]
        hosp_curtains = hospital_curtains.get(hosp.HID, [])
        if not hosp_tracks or not hosp_curtains:
            continue

        for curtain in hosp_curtains:
            primary_track = random.choice(hosp_tracks)
            secondary = random.choice(hosp_tracks) if len(hosp_tracks) > 1 else primary_track

            num_installs = random.randint(2, 8)
            for j in range(num_installs):
                track = primary_track if random.random() < 0.7 else secondary
                days_ago = random.randint(1, 180)

                tcs = TrackCurtainService(
                    CurBarCode=curtain.CurtBarCode,
                    TrackBarCode=track.TrackBarCode,
                    CurStatusID=4,
                    HID=hosp.HID,
                    Installed_By=str(random.randint(1, 5)),
                    Installed_Date=now - timedelta(days=days_ago, hours=random.randint(0, 8)),
                    Date_Created=now - timedelta(days=days_ago),
                    Created_By="seed",
                    ServiceType="Maintenance",
                )
                db.add(tcs)

    db.flush()

    total_curtains = db.query(HospCurtain).count()
    total_tracks = db.query(HospTrack).count()
    total_history = db.query(TrackCurtainService).count()
    print(f"Seeded: {len(hospitals)+2} hospitals, {total_tracks} tracks, "
          f"{total_curtains} curtains, {total_history} service records.")


if __name__ == "__main__":
    seed()
