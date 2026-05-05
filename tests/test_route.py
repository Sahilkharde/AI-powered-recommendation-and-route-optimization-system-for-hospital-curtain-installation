"""Tests for the route optimization engine."""

import unittest
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    CurtType,
    HospBuilding,
    HospBuildingRoom,
    HospCurtain,
    HospTrack,
    HospUnit,
    Hospital,
    TrackCurtainService,
    UnitLookup,
)
from app.engine.route import build_installer_route

_test_engine = create_engine("sqlite:///:memory:")
_TestSession = sessionmaker(bind=_test_engine)


class TestRouteOptimizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=_test_engine)
        cls.db = _TestSession()
        cls._seed(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=_test_engine)

    @classmethod
    def _seed(cls, db):
        ct = CurtType(Curt_TypeID=1, Name="Standard", Enabled=True)
        db.add(ct)
        ul1 = UnitLookup(UnitId=1, Name="ICU", Enabled=True)
        ul2 = UnitLookup(UnitId=2, Name="Surgery", Enabled=True)
        ul3 = UnitLookup(UnitId=3, Name="Pediatrics", Enabled=True)
        ul4 = UnitLookup(UnitId=4, Name="General", Enabled=True)
        db.add_all([ul1, ul2, ul3, ul4])
        db.flush()

        h1 = Hospital(HID=10, Name="Hospital A", AccountNumber=1000, Enabled=True)
        h2 = Hospital(HID=20, Name="Hospital B", AccountNumber=2000, Enabled=True)
        db.add_all([h1, h2])
        db.flush()

        b1 = HospBuilding(HID=10, Name="West Wing", TotalFloor=3, Enabled=True)
        b2 = HospBuilding(HID=10, Name="East Wing", TotalFloor=2, Enabled=True)
        b3 = HospBuilding(HID=20, Name="Main Building", TotalFloor=2, Enabled=True)
        db.add_all([b1, b2, b3])
        db.flush()

        u1 = HospUnit(BID=b1.BID, UnitID=1, Floor=1, Style=1, Enabled=True)
        u2 = HospUnit(BID=b1.BID, UnitID=2, Floor=2, Style=1, Enabled=True)
        u3 = HospUnit(BID=b2.BID, UnitID=3, Floor=1, Style=1, Enabled=True)
        u4 = HospUnit(BID=b3.BID, UnitID=4, Floor=1, Style=1, Enabled=True)
        db.add_all([u1, u2, u3, u4])
        db.flush()

        track_barcodes = []
        for idx, (unit, rname) in enumerate([
            (u1, "Room 101"), (u1, "Room 102"),
            (u2, "Room 201"),
            (u3, "Room 101"),
            (u4, "Room 101"), (u4, "Room 102"),
        ], start=1):
            r = HospBuildingRoom(HUID=unit.HUID, RoomNumber=rname, Enabled=True)
            db.add(r)
            db.flush()
            barcode = f"T{idx:04d}"
            t = HospTrack(
                HUID=unit.HUID, RoomId=r.RoomID, TrackBarCode=barcode,
                Length="72", Height="84", Curt_TypeId=1,
                NumberOfCurtain=2, Enabled=True,
            )
            db.add(t)
            db.flush()
            track_barcodes.append(barcode)

        now = datetime.utcnow()
        for bc in track_barcodes:
            db.add(TrackCurtainService(
                CurBarCode=10000 + int(bc[1:]),
                TrackBarCode=bc,
                Installed_By="1",
                Installed_Date=now - timedelta(days=1),
            ))
        db.commit()
        cls.track_barcodes = track_barcodes

    def test_route_has_stops(self):
        route = build_installer_route(self.db, installer_id=1)
        self.assertGreater(route.total_stops, 0)

    def test_route_covers_both_hospitals(self):
        route = build_installer_route(self.db, installer_id=1)
        self.assertEqual(route.total_hospitals, 2)

    def test_stops_are_ordered(self):
        route = build_installer_route(self.db, installer_id=1)
        orders = []
        for seg in route.segments:
            for stop in seg.stops:
                orders.append(stop.order)
        self.assertEqual(orders, sorted(orders))

    def test_unknown_installer_empty_route(self):
        route = build_installer_route(self.db, installer_id=999)
        self.assertEqual(route.total_stops, 0)
        self.assertEqual(len(route.segments), 0)

    def test_within_hospital_sorted_by_building_floor(self):
        route = build_installer_route(self.db, installer_id=1)
        hosp_a_seg = [s for s in route.segments if s.hospital_id == 10]
        if hosp_a_seg:
            stops = hosp_a_seg[0].stops
            building_floors = [(s.building_name, s.floor) for s in stops]
            self.assertEqual(building_floors, sorted(building_floors))

    def test_message_contains_hospital_names(self):
        route = build_installer_route(self.db, installer_id=1)
        self.assertIn("Hospital A", route.message)
        self.assertIn("Hospital B", route.message)


if __name__ == "__main__":
    unittest.main()
