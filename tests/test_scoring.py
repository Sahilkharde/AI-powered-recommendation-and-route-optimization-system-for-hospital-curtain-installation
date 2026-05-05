"""Tests for the scoring engine."""

import unittest

from app.engine.scoring import ScoringInput, build_reason, compute_score


class TestScoring(unittest.TestCase):
    def test_perfect_match(self):
        inp = ScoringInput(
            history_count=10, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=3, has_capacity=True,
        )
        score = compute_score(inp)
        self.assertGreaterEqual(score, 90.0)

    def test_no_history_reduces_score(self):
        perfect = ScoringInput(
            history_count=10, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=3, has_capacity=True,
        )
        no_history = ScoringInput(
            history_count=0, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=3, has_capacity=True,
        )
        self.assertGreater(compute_score(perfect), compute_score(no_history))

    def test_size_mismatch_reduces_score(self):
        good_size = ScoringInput(
            history_count=5, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=10, has_capacity=True,
        )
        bad_size = ScoringInput(
            history_count=5, max_history=10,
            size_delta=1.8, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=10, has_capacity=True,
        )
        self.assertGreater(compute_score(good_size), compute_score(bad_size))

    def test_no_capacity_penalized(self):
        with_cap = ScoringInput(
            history_count=5, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=10, has_capacity=True,
        )
        no_cap = ScoringInput(
            history_count=5, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=10, has_capacity=False,
        )
        self.assertGreater(compute_score(with_cap), compute_score(no_cap))

    def test_type_mismatch_reduces_score(self):
        matched = ScoringInput(
            history_count=5, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=10, has_capacity=True,
        )
        mismatched = ScoringInput(
            history_count=5, max_history=10,
            size_delta=0, size_tolerance=2.0,
            type_match=False, style_match=True,
            days_since_last_install=10, has_capacity=True,
        )
        self.assertGreater(compute_score(matched), compute_score(mismatched))

    def test_score_bounds(self):
        worst = ScoringInput(
            history_count=0, max_history=10,
            size_delta=10, size_tolerance=2.0,
            type_match=False, style_match=False,
            days_since_last_install=365, has_capacity=False,
        )
        score = compute_score(worst)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_reason_includes_history(self):
        inp = ScoringInput(
            history_count=3, max_history=5,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=5, has_capacity=True,
        )
        reason = build_reason(inp, 85.0)
        self.assertIn("3 time(s) before", reason)

    def test_reason_warns_on_no_capacity(self):
        inp = ScoringInput(
            history_count=1, max_history=5,
            size_delta=0, size_tolerance=2.0,
            type_match=True, style_match=True,
            days_since_last_install=5, has_capacity=False,
        )
        reason = build_reason(inp, 50.0)
        self.assertIn("WARNING", reason)


if __name__ == "__main__":
    unittest.main()
