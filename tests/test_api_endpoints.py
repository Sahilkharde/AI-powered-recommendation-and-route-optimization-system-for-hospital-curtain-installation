"""API endpoint tests for the FastAPI routes shown in /docs."""

import unittest
from datetime import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.cache import TTLCache
from app.database import Base, get_db
from app.main import app
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


class _BrokenDbSession:
    def execute(self, _query):
        raise RuntimeError("db unavailable")


class TestApiEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        cls.SessionLocal = sessionmaker(bind=cls.engine, autocommit=False, autoflush=False)
        Base.metadata.create_all(bind=cls.engine)
        cls._seed()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine)

    @classmethod
    def _seed(cls):
        db = cls.SessionLocal()
        try:
            ct = CurtType(Curt_TypeID=1, Name="Standard", Enabled=True)
            db.add(ct)
            ul = UnitLookup(UnitId=1, Name="ICU", Enabled=True)
            db.add(ul)
            db.flush()

            h10 = Hospital(HID=10, Name="Test Hospital", AccountNumber=9999, Enabled=True)
            h99 = Hospital(
                HID=99, Name="AI Automation Hospital Disposable", AccountNumber=99,
                HasDisposable=True, Enabled=True,
            )
            h1001 = Hospital(
                HID=1001, Name="AI Automation Hospital Spare", AccountNumber=1001, Enabled=True,
            )
            db.add_all([h10, h99, h1001])
            db.flush()

            building = HospBuilding(HID=h10.HID, Name="Main Building", TotalFloor=2, Enabled=True)
            db.add(building)
            db.flush()

            unit = HospUnit(BID=building.BID, UnitID=1, Floor=1, Style=1, Enabled=True)
            db.add(unit)
            db.flush()

            room = HospBuildingRoom(HUID=unit.HUID, RoomNumber="Room 101", Enabled=True)
            db.add(room)
            db.flush()

            track = HospTrack(
                HUID=unit.HUID, RoomId=room.RoomID, TrackBarCode="9999-T0001",
                Length="72", Height="84", Curt_TypeId=1,
                NumberOfCurtain=2, NumberOfSpares=1, NumberOfDisposables=1, Enabled=True,
            )
            db.add(track)
            db.flush()

            curtain_regular = HospCurtain(
                HID=h10.HID, Hosp_CurtID=1, CurtBarCode=99990001,
                Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
            )
            curtain_spare = HospCurtain(
                HID=h1001.HID, Hosp_CurtID=2, CurtBarCode=10010001,
                Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
            )
            curtain_disposable = HospCurtain(
                HID=h99.HID, Hosp_CurtID=3, CurtBarCode=990001,
                Curt_TypeID=1, UnitStyle=1, WidthId=72, HeightId=84, Enabled=True,
            )
            db.add_all([curtain_regular, curtain_spare, curtain_disposable])
            db.flush()

            db.add(TrackCurtainService(
                CurBarCode=curtain_regular.CurtBarCode,
                TrackBarCode=track.TrackBarCode,
                Installed_By="7",
                Installed_Date=datetime.utcnow(),
            ))
            db.commit()
        finally:
            db.close()

    def setUp(self):
        def _override_db():
            db = self.SessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = _override_db
        self.client = TestClient(app)
        app.state.cache = TTLCache(default_ttl=60)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        app.state.cache = None

    def test_suggest_location_success_contract(self):
        response = self.client.post("/api/v1/suggest-location", json={"curtain_barcode": "99990001"})
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["curtain_barcode"], "99990001")
        self.assertIn("recommendations", payload)
        self.assertGreaterEqual(len(payload["recommendations"]), 1)
        self.assertIn("total_candidates", payload)
        self.assertIn("message", payload)

    def test_suggest_location_validation_error(self):
        response = self.client.post("/api/v1/suggest-location", json={})
        self.assertEqual(response.status_code, 422)

    def test_suggest_location_domain_error(self):
        response = self.client.post("/api/v1/suggest-location", json={"curtain_barcode": "DOESNOTEXIST"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", response.json()["detail"].lower())

    def test_match_curtains_success_contract(self):
        response = self.client.post("/api/v1/match-curtains", json={"track_barcode": "9999-T0001"})
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["track_barcode"], "9999-T0001")
        self.assertIn("matches", payload)
        self.assertGreaterEqual(len(payload["matches"]), 1)
        best = [m for m in payload["matches"] if m["is_best_match"]]
        self.assertEqual(len(best), 1)

    def test_match_curtains_validation_error(self):
        response = self.client.post("/api/v1/match-curtains", json={})
        self.assertEqual(response.status_code, 422)

    def test_match_curtains_domain_error(self):
        response = self.client.post("/api/v1/match-curtains", json={"track_barcode": "NONEXISTENT"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("not found", response.json()["detail"].lower())

    def test_route_endpoint_success(self):
        response = self.client.get("/api/v1/installer/7/route")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["installer_id"], 7)
        self.assertGreater(payload["total_stops"], 0)

    def test_route_endpoint_invalid_date(self):
        response = self.client.get("/api/v1/installer/7/route?route_date=not-a-date")
        self.assertEqual(response.status_code, 422)

    def test_cache_stats_reflect_api_cache_usage(self):
        initial = self.client.get("/api/v1/cache/stats").json()
        initial_keys = initial["total_keys"]

        self.client.post("/api/v1/suggest-location", json={"curtain_barcode": "99990001"})
        self.client.post("/api/v1/suggest-location", json={"curtain_barcode": "99990001"})

        after = self.client.get("/api/v1/cache/stats")
        self.assertEqual(after.status_code, 200)
        self.assertGreaterEqual(after.json()["total_keys"], initial_keys + 1)
        self.assertIn(after.json()["backend"], ["in-memory", "redis", "none"])

    def test_health_ok(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn(payload["status"], ["ok", "degraded"])
        self.assertTrue(payload["db_ok"])
        self.assertTrue(payload["cache_ok"])

    def test_health_degraded_when_db_and_cache_unavailable(self):
        def _broken_db_override():
            yield _BrokenDbSession()

        app.dependency_overrides[get_db] = _broken_db_override
        app.state.cache = None

        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "degraded")
        self.assertFalse(payload["db_ok"])
        self.assertFalse(payload["cache_ok"])

    def test_agent_scan_success_and_failure(self):
        with patch("app.api.routes.run_agent", return_value={"ok": True, "recommendation": {}, "agent_explanation": "x"}):
            ok_response = self.client.post("/api/v1/agent/scan-curtain", json={"curtain_barcode": "99990001"})
            self.assertEqual(ok_response.status_code, 200)
            self.assertTrue(ok_response.json()["ok"])

        with patch("app.api.routes.run_agent", side_effect=RuntimeError("anthropic unavailable")):
            fail_response = self.client.post("/api/v1/agent/scan-curtain", json={"curtain_barcode": "99990001"})
            self.assertEqual(fail_response.status_code, 500)
            self.assertIn("anthropic unavailable", fail_response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
