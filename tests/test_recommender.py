"""Integration tests for the recommender engine against a seeded database."""

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
from app.engine.recommender import RecommenderError, suggest_location

_test_engine = create_engine("sqlite:///:memory:")
_TestSession = sessionmaker(bind=_test_engine)


class TestRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=_test_engine)
        cls.db = _TestSession()
        cls._seed_test_data(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        Base.metadata.drop_all(bind=_test_engine)

    @classmethod
    def _seed_test_data(cls, db):
        ct_standard = CurtType(Curt_TypeID=1, Name="Standard", Enabled=True)
        ct_snap = CurtType(Curt_TypeID=2, Name="Snap", Enabled=True)
        db.add_all([ct_standard, ct_snap])

        ul_icu = UnitLookup(UnitId=1, Name="ICU", Enabled=True)
        ul_surgery = UnitLookup(UnitId=2, Name="Surgery", Enabled=True)
        db.add_all([ul_icu, ul_surgery])
        db.flush()

        h1 = Hospital(HID=10, Name="Test Hospital", AccountNumber=9999, Enabled=True)
        h99 = Hospital(
            HID=99, Name="AI Automation Hospital Disposable", AccountNumber=99,
            HasDisposable=True, Enabled=True,
        )
        h1001 = Hospital(
            HID=1001, Name="AI Automation Hospital Spare", AccountNumber=1001, Enabled=True,
        )
        db.add_all([h1, h99, h1001])
        db.flush()

        b1 = HospBuilding(HID=10, Name="Main Building", TotalFloor=3, Enabled=True)
        db.add(b1)
        db.flush()

        u1 = HospUnit(BID=b1.BID, UnitID=1, Floor=1, Style=1, Enabled=True)
        u2 = HospUnit(BID=b1.BID, UnitID=2, Floor=2, Style=2, Enabled=True)
        db.add_all([u1, u2])
        db.flush()

        r1 = HospBuildingRoom(HUID=u1.HUID, RoomNumber="Room 101", Enabled=True)
        r2 = HospBuildingRoom(HUID=u1.HUID, RoomNumber="Room 102", Enabled=True)
        r3 = HospBuildingRoom(HUID=u2.HUID, RoomNumber="Room 201", Enabled=True)
        db.add_all([r1, r2, r3])
        db.flush()

        t1 = HospTrack(
            HUID=u1.HUID, RoomId=r1.RoomID, TrackBarCode="9999-T0001",
            Length="72", Height="84", Curt_TypeId=1,
            NumberOfCurtain=2, NumberOfSpares=1, NumberOfDisposables=1, Enabled=True,
        )
        t2 = HospTrack(
            HUID=u1.HUID, RoomId=r2.RoomID, TrackBarCode="9999-T0002",
            Length="72", Height="84", Curt_TypeId=1,
            NumberOfCurtain=2, NumberOfSpares=1, NumberOfDisposables=1, Enabled=True,
        )
        t3 = HospTrack(
            HUID=u2.HUID, RoomId=r3.RoomID, TrackBarCode="9999-T0003",
            Length="48", Height="96", Curt_TypeId=2,
            NumberOfCurtain=1, NumberOfSpares=1, NumberOfDisposables=1, Enabled=True,
        )
        db.add_all([t1, t2, t3])
        db.flush()

        cls.curtain_regular = HospCurtain(
            HID=10, Hosp_CurtID=1, CurtBarCode=99990001,
            Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
        )
        cls.curtain_spare = HospCurtain(
            HID=1001, Hosp_CurtID=2, CurtBarCode=10010001,
            Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
        )
        cls.curtain_disposable = HospCurtain(
            HID=99, Hosp_CurtID=3, CurtBarCode=990001,
            Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
        )
        db.add_all([
            cls.curtain_regular, cls.curtain_spare, cls.curtain_disposable,
        ])
        db.flush()

        now = datetime.utcnow()
        for i in range(5):
            db.add(TrackCurtainService(
                CurBarCode=cls.curtain_regular.CurtBarCode,
                TrackBarCode="9999-T0001",
                Installed_Date=now - timedelta(days=i * 10),
                Installed_By="installer1",
            ))
        for i in range(2):
            db.add(TrackCurtainService(
                CurBarCode=cls.curtain_regular.CurtBarCode,
                TrackBarCode="9999-T0002",
                Installed_Date=now - timedelta(days=i * 30 + 5),
                Installed_By="installer1",
            ))
        db.commit()

        cls.t1 = t1
        cls.t2 = t2
        cls.t3 = t3

    def test_regular_curtain_gets_recommendations(self):
        resp = suggest_location(self.db, "99990001")
        self.assertGreater(len(resp.recommendations), 0)
        self.assertEqual(resp.curtain_barcode, "99990001")
        self.assertFalse(resp.is_disposable)
        self.assertFalse(resp.is_spare)

    def test_top_recommendation_is_most_frequent_track(self):
        resp = suggest_location(self.db, "99990001")
        top = resp.recommendations[0]
        self.assertEqual(top.location.track_barcode, "9999-T0001")

    def test_regular_curtain_only_own_hospital(self):
        resp = suggest_location(self.db, "99990001")
        for rec in resp.recommendations:
            self.assertEqual(rec.location.hospital_id, 10)

    def test_spare_curtain_can_cross_hospitals(self):
        resp = suggest_location(self.db, "10010001")
        self.assertGreater(len(resp.recommendations), 0)

    def test_disposable_curtain_can_cross_hospitals(self):
        resp = suggest_location(self.db, "990001")
        self.assertGreater(len(resp.recommendations), 0)

    def test_unknown_barcode_rejected(self):
        with self.assertRaises(RecommenderError):
            suggest_location(self.db, "DOESNOTEXIST")

    def test_recommendations_sorted_by_score(self):
        resp = suggest_location(self.db, "99990001")
        scores = [r.score for r in resp.recommendations]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_style_mismatch_produces_warning(self):
        resp = suggest_location(self.db, "99990001")
        mismatched = [r for r in resp.recommendations if not r.style_match]
        for rec in mismatched:
            self.assertTrue(any("mismatch" in w.lower() for w in rec.warnings))


if __name__ == "__main__":
    unittest.main()
