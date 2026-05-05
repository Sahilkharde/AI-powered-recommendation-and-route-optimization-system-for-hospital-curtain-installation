"""Tests for the track-to-curtain matching engine."""

import unittest

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
    UnitLookup,
)
from app.engine.match import MatchError, match_curtains_for_track

_test_engine = create_engine("sqlite:///:memory:")
_TestSession = sessionmaker(bind=_test_engine)


class TestMatchCurtains(unittest.TestCase):
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
        ct_standard = CurtType(Curt_TypeID=1, Name="Standard", Enabled=True)
        ct_snap = CurtType(Curt_TypeID=2, Name="Snap", Enabled=True)
        db.add_all([ct_standard, ct_snap])

        ul_icu = UnitLookup(UnitId=1, Name="ICU", Enabled=True)
        db.add(ul_icu)
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

        b = HospBuilding(HID=10, Name="Main", TotalFloor=2, Enabled=True)
        db.add(b)
        db.flush()

        u = HospUnit(BID=b.BID, UnitID=1, Floor=1, Style=1, Enabled=True)
        db.add(u)
        db.flush()

        r = HospBuildingRoom(HUID=u.HUID, RoomNumber="Room 101", Enabled=True)
        db.add(r)
        db.flush()

        cls.track = HospTrack(
            HUID=u.HUID, RoomId=r.RoomID, TrackBarCode="9999-T0001",
            Length="72", Height="84", Curt_TypeId=1,
            NumberOfCurtain=2, NumberOfSpares=1, NumberOfDisposables=1, Enabled=True,
        )
        db.add(cls.track)
        db.flush()

        db.add_all([
            HospCurtain(
                HID=10, Hosp_CurtID=1, CurtBarCode=99990001,
                Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
            ),
            HospCurtain(
                HID=10, Hosp_CurtID=2, CurtBarCode=99990002,
                Curt_TypeID=2, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
            ),
            HospCurtain(
                HID=1001, Hosp_CurtID=3, CurtBarCode=10010001,
                Curt_TypeID=1, UnitStyle=1, WidthId=71, HeightId=84, Enabled=True,
            ),
        ])
        db.commit()

    def test_returns_matches(self):
        resp = match_curtains_for_track(self.db, "9999-T0001")
        self.assertGreater(len(resp.matches), 0)

    def test_best_match_flagged(self):
        resp = match_curtains_for_track(self.db, "9999-T0001")
        best = [m for m in resp.matches if m.is_best_match]
        self.assertEqual(len(best), 1)

    def test_spare_curtains_included(self):
        resp = match_curtains_for_track(self.db, "9999-T0001")
        barcodes = [m.curtain_barcode for m in resp.matches]
        self.assertIn("10010001", barcodes)

    def test_type_mismatch_produces_warning(self):
        resp = match_curtains_for_track(self.db, "9999-T0001")
        snap_matches = [m for m in resp.matches if m.curtain_type == "Snap"]
        for m in snap_matches:
            self.assertTrue(any("mismatch" in w.lower() for w in m.warnings))

    def test_sorted_by_score(self):
        resp = match_curtains_for_track(self.db, "9999-T0001")
        scores = [m.score for m in resp.matches]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_unknown_track_raises(self):
        with self.assertRaises(MatchError):
            match_curtains_for_track(self.db, "NONEXIST")


if __name__ == "__main__":
    unittest.main()
