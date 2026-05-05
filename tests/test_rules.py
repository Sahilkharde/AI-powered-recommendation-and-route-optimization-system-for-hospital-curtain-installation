"""Tests for all AI Automation Hospital business rules (R1-R12)."""

import unittest

from app.engine.rules import (
    bag_has_capacity,
    can_install_in_hospital,
    check_style_match,
    check_type_match,
    is_disposable_curtain,
    is_packable_status,
    is_spare_curtain,
    is_temp_storage_hospital,
    needs_bag,
    size_compatible,
    track_belongs_to_hospital,
    track_has_capacity,
)
from app.models import HospCurtain, HospTrack, HospUnit, Hospital


def _curtain(**kw) -> HospCurtain:
    defaults = dict(
        CID=1, HID=1002, Hosp_CurtID=1001,
        CurtBarCode=1001, Curt_TypeID=1,
        UnitStyle=1, WidthId=4, HeightId=2,
        Enabled=True,
    )
    defaults.update(kw)
    return HospCurtain(**defaults)


def _hospital(**kw) -> Hospital:
    defaults = dict(
        HID=1002, Name="Test Hospital", AccountNumber=1576,
        isTempStorage=False, HasDisposable=False,
        Enabled=True,
    )
    defaults.update(kw)
    return Hospital(**defaults)


def _track(**kw) -> HospTrack:
    defaults = dict(
        HospTrackId=1, HUID=1, RoomId=1,
        TrackBarCode="1576-T0001",
        Length="72", Height="84", Curt_TypeId=1,
        NumberOfCurtain=2, NumberOfSpares=1, NumberOfDisposables=1,
        Enabled=True,
    )
    defaults.update(kw)
    return HospTrack(**defaults)


def _unit(**kw) -> HospUnit:
    defaults = dict(
        HUID=1, BID=1, UnitID=1, Floor=1,
        Style=1, CellingHeight="10",
        Enabled=True,
    )
    defaults.update(kw)
    return HospUnit(**defaults)


class TestR1_HospitalBound(unittest.TestCase):
    def test_regular_curtain_own_hospital(self):
        c = _curtain(HID=1002)
        self.assertTrue(can_install_in_hospital(c, 1002))

    def test_regular_curtain_wrong_hospital(self):
        c = _curtain(HID=1002)
        self.assertFalse(can_install_in_hospital(c, 1003))

    def test_disposable_curtain_any_hospital(self):
        c = _curtain(HID=99)
        self.assertTrue(can_install_in_hospital(c, 1002))
        self.assertTrue(can_install_in_hospital(c, 1003))
        self.assertTrue(can_install_in_hospital(c, 9999))

    def test_spare_curtain_any_hospital(self):
        c = _curtain(HID=1001)
        self.assertTrue(can_install_in_hospital(c, 1002))
        self.assertTrue(can_install_in_hospital(c, 1003))


class TestR2_PackableStatus(unittest.TestCase):
    def test_packable_status_ids(self):
        self.assertTrue(is_packable_status(1, {1, 2}))
        self.assertTrue(is_packable_status(2, {1, 2}))

    def test_non_packable_status(self):
        self.assertFalse(is_packable_status(4, {1, 2}))

    def test_empty_packable_set_allows_all(self):
        self.assertTrue(is_packable_status(99, set()))

    def test_none_status_allowed(self):
        self.assertTrue(is_packable_status(None, {1, 2}))


class TestR4_BagCapacity(unittest.TestCase):
    def test_under_limit(self):
        self.assertTrue(bag_has_capacity(14))

    def test_at_limit(self):
        self.assertFalse(bag_has_capacity(15))

    def test_over_limit(self):
        self.assertFalse(bag_has_capacity(20))

    def test_empty(self):
        self.assertTrue(bag_has_capacity(0))


class TestR6_TrackBarcode(unittest.TestCase):
    def test_matching_account_number(self):
        self.assertTrue(track_belongs_to_hospital("1576-T0001", 1576))

    def test_non_matching_account_number(self):
        self.assertFalse(track_belongs_to_hospital("2301-T0001", 1576))

    def test_none_account_number(self):
        self.assertFalse(track_belongs_to_hospital("2301-T0001", None))


class TestR7_StyleMismatch(unittest.TestCase):
    def test_matching_style(self):
        c = _curtain(UnitStyle=1)
        u = _unit(Style=1)
        self.assertIsNone(check_style_match(c, u))

    def test_mismatched_style_returns_warning(self):
        c = _curtain(UnitStyle=1)
        u = _unit(Style=2)
        warning = check_style_match(c, u)
        self.assertIsNotNone(warning)
        self.assertIn("mismatch", warning.lower())

    def test_none_style_no_warning(self):
        c = _curtain(UnitStyle=None)
        u = _unit(Style=1)
        self.assertIsNone(check_style_match(c, u))


class TestR8_TypeMismatch(unittest.TestCase):
    def test_matching_type(self):
        c = _curtain(Curt_TypeID=1)
        t = _track(Curt_TypeId=1)
        self.assertIsNone(check_type_match(c, t))

    def test_mismatched_type_returns_warning(self):
        c = _curtain(Curt_TypeID=2)
        t = _track(Curt_TypeId=1)
        warning = check_type_match(c, t)
        self.assertIsNotNone(warning)
        self.assertIn("mismatch", warning.lower())

    def test_none_type_no_warning(self):
        c = _curtain(Curt_TypeID=None)
        t = _track(Curt_TypeId=1)
        self.assertIsNone(check_type_match(c, t))


class TestR9_DisposableNoBag(unittest.TestCase):
    def test_disposable_no_bag(self):
        c = _curtain(HID=99)
        self.assertFalse(needs_bag(c))

    def test_regular_needs_bag(self):
        c = _curtain(HID=1002)
        self.assertTrue(needs_bag(c))

    def test_spare_needs_bag(self):
        c = _curtain(HID=1001)
        self.assertTrue(needs_bag(c))


class TestR10_TempStorage(unittest.TestCase):
    def test_temp_storage_hospital(self):
        h = _hospital(isTempStorage=True)
        self.assertTrue(is_temp_storage_hospital(h))

    def test_regular_hospital(self):
        h = _hospital(isTempStorage=False)
        self.assertFalse(is_temp_storage_hospital(h))


class TestTrackCapacity(unittest.TestCase):
    def test_regular_under_capacity(self):
        t = _track(NumberOfCurtain=2)
        c = _curtain(HID=1002)
        self.assertTrue(track_has_capacity(t, 1, c))

    def test_regular_at_capacity(self):
        t = _track(NumberOfCurtain=2)
        c = _curtain(HID=1002)
        self.assertFalse(track_has_capacity(t, 2, c))

    def test_disposable_uses_combined_capacity(self):
        t = _track(NumberOfCurtain=2, NumberOfDisposables=1)
        c = _curtain(HID=99)
        self.assertTrue(track_has_capacity(t, 2, c))
        self.assertFalse(track_has_capacity(t, 3, c))


class TestSizeCompatibility(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(size_compatible(72.0, 72.0))

    def test_within_tolerance(self):
        self.assertTrue(size_compatible(73.5, 72.0))

    def test_outside_tolerance(self):
        self.assertFalse(size_compatible(75.0, 72.0))

    def test_none_values_compatible(self):
        self.assertTrue(size_compatible(None, 72.0))
        self.assertTrue(size_compatible(72.0, None))


class TestSpecialHospitalFlags(unittest.TestCase):
    def test_disposable_curtain(self):
        self.assertTrue(is_disposable_curtain(_curtain(HID=99)))
        self.assertFalse(is_disposable_curtain(_curtain(HID=1002)))

    def test_spare_curtain(self):
        self.assertTrue(is_spare_curtain(_curtain(HID=1001)))
        self.assertFalse(is_spare_curtain(_curtain(HID=1002)))


if __name__ == "__main__":
    unittest.main()
