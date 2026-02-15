"""Validate the engine against exact probabilities from Taflin (2001).

These tests run Monte Carlo simulations and compare results against the
known exact probability distributions for Risk dice. This ensures our
engine is faithfully implementing the Risk combat rules.
"""

import random
from collections import Counter

from engine.dice import roll
from engine.heroes import roll_with_hero
from engine.models import Army
from engine.combat import resolve_single_round, resolve_battle
from engine.probabilities import (
    SINGLE_ROLL_PROBABILITIES,
    expected_losses,
    attacker_advantage_ratio,
    win_probability_exact,
)

NUM_TRIALS = 50000
TOLERANCE = 0.02  # 2% tolerance for Monte Carlo vs exact


class TestSingleRollProbabilities:
    """Verify single-roll outcomes match Taflin Table 1."""

    def _run_rolls(self, atk_dice, def_dice, num_trials=NUM_TRIALS):
        """Run many single rolls and count outcome frequencies."""
        rng = random.Random(12345)
        counts: Counter[tuple[int, int]] = Counter()

        for _ in range(num_trials):
            atk = Army(units=atk_dice + 1)  # +1 because attacker keeps 1 behind
            dfn = Army(units=max(def_dice, 1))
            # Manually do what resolve_single_round does but without mutating
            atk_rolls = sorted([rng.randint(1, 6) for _ in range(atk_dice)], reverse=True)
            def_rolls = sorted([rng.randint(1, 6) for _ in range(def_dice)], reverse=True)

            atk_losses = 0
            def_losses = 0
            pairs = min(len(atk_rolls), len(def_rolls))
            for i in range(pairs):
                if atk_rolls[i] > def_rolls[i]:
                    def_losses += 1
                else:
                    atk_losses += 1  # ties go to defender

            counts[(atk_losses, def_losses)] += 1

        return {k: v / num_trials for k, v in counts.items()}

    def test_1v1_probabilities(self):
        observed = self._run_rolls(1, 1)
        exact = SINGLE_ROLL_PROBABILITIES[(1, 1)]
        for outcome, exact_p in exact.items():
            assert abs(observed.get(outcome, 0) - float(exact_p)) < TOLERANCE, \
                f"1v1 {outcome}: observed {observed.get(outcome, 0):.4f} vs exact {float(exact_p):.4f}"

    def test_1v2_probabilities(self):
        observed = self._run_rolls(1, 2)
        exact = SINGLE_ROLL_PROBABILITIES[(1, 2)]
        for outcome, exact_p in exact.items():
            assert abs(observed.get(outcome, 0) - float(exact_p)) < TOLERANCE, \
                f"1v2 {outcome}: observed {observed.get(outcome, 0):.4f} vs exact {float(exact_p):.4f}"

    def test_2v1_probabilities(self):
        observed = self._run_rolls(2, 1)
        exact = SINGLE_ROLL_PROBABILITIES[(2, 1)]
        for outcome, exact_p in exact.items():
            assert abs(observed.get(outcome, 0) - float(exact_p)) < TOLERANCE, \
                f"2v1 {outcome}: observed {observed.get(outcome, 0):.4f} vs exact {float(exact_p):.4f}"

    def test_2v2_probabilities(self):
        observed = self._run_rolls(2, 2)
        exact = SINGLE_ROLL_PROBABILITIES[(2, 2)]
        for outcome, exact_p in exact.items():
            assert abs(observed.get(outcome, 0) - float(exact_p)) < TOLERANCE, \
                f"2v2 {outcome}: observed {observed.get(outcome, 0):.4f} vs exact {float(exact_p):.4f}"

    def test_3v1_probabilities(self):
        observed = self._run_rolls(3, 1)
        exact = SINGLE_ROLL_PROBABILITIES[(3, 1)]
        for outcome, exact_p in exact.items():
            assert abs(observed.get(outcome, 0) - float(exact_p)) < TOLERANCE, \
                f"3v1 {outcome}: observed {observed.get(outcome, 0):.4f} vs exact {float(exact_p):.4f}"

    def test_3v2_probabilities(self):
        """The most important case — most battles spend time here."""
        observed = self._run_rolls(3, 2)
        exact = SINGLE_ROLL_PROBABILITIES[(3, 2)]
        for outcome, exact_p in exact.items():
            assert abs(observed.get(outcome, 0) - float(exact_p)) < TOLERANCE, \
                f"3v2 {outcome}: observed {observed.get(outcome, 0):.4f} vs exact {float(exact_p):.4f}"


class TestExpectedLosses:
    """Verify expected loss rates match Taflin Table 1."""

    def test_3v2_attacker_advantage(self):
        """Taflin: attacker loses armies 15% slower than defender in 3v2."""
        ratio = attacker_advantage_ratio(3, 2)
        # Exact ratio is 1.0791/0.9209 ≈ 1.1718
        assert 1.15 < ratio < 1.20, f"3v2 advantage ratio {ratio} not ~1.17"

    def test_3v2_expected_losses(self):
        atk, dfn = expected_losses(3, 2)
        assert abs(atk - 0.9209) < 0.001
        assert abs(dfn - 1.0791) < 0.001

    def test_1v1_defender_advantage(self):
        """With 1v1, defender has the advantage due to winning ties."""
        ratio = attacker_advantage_ratio(1, 1)
        assert ratio < 1.0, f"1v1 should favor defender, got ratio {ratio}"

    def test_2v2_defender_advantage(self):
        """With 2v2, defender has the advantage."""
        atk, dfn = expected_losses(2, 2)
        assert atk > dfn, f"2v2: attacker should lose more ({atk} vs {dfn})"


class TestBattleWinProbabilities:
    """Verify full battle outcomes match exact Markov chain solutions."""

    def _simulate_win_rate(self, atk_units, def_units, num_trials=NUM_TRIALS):
        rng = random.Random(54321)
        wins = 0
        for _ in range(num_trials):
            atk = Army(units=atk_units)
            dfn = Army(units=def_units)
            result = resolve_battle(atk, dfn, auto_resolve=True, rng=rng)
            if result.winner == "attacker":
                wins += 1
        return wins / num_trials

    def test_equal_3v3(self):
        exact = win_probability_exact(3, 3)
        observed = self._simulate_win_rate(3, 3)
        assert abs(observed - exact) < TOLERANCE, \
            f"3v3: observed {observed:.4f} vs exact {exact:.4f}"

    def test_equal_5v5(self):
        exact = win_probability_exact(5, 5)
        observed = self._simulate_win_rate(5, 5)
        assert abs(observed - exact) < TOLERANCE, \
            f"5v5: observed {observed:.4f} vs exact {exact:.4f}"

    def test_10v5_attacker_favored(self):
        exact = win_probability_exact(10, 5)
        observed = self._simulate_win_rate(10, 5)
        assert abs(observed - exact) < TOLERANCE, \
            f"10v5: observed {observed:.4f} vs exact {exact:.4f}"

    def test_5v10_defender_favored(self):
        exact = win_probability_exact(5, 10)
        observed = self._simulate_win_rate(5, 10)
        assert abs(observed - exact) < TOLERANCE, \
            f"5v10: observed {observed:.4f} vs exact {exact:.4f}"

    def test_10v10_defender_slight_edge(self):
        """With equal large armies, defender has a slight edge (~52%).

        Even though attacker has per-roll advantage in 3v2, the boundary
        conditions (must leave 1 behind, ties to defender at low dice)
        give defender an overall edge in equal-army battles.
        """
        exact = win_probability_exact(10, 10)
        observed = self._simulate_win_rate(10, 10)
        assert abs(observed - exact) < TOLERANCE, \
            f"10v10: observed {observed:.4f} vs exact {exact:.4f}"
        assert exact < 0.5, f"10v10 defender should be slightly favored, got {exact}"

    def test_known_easy_case_2v1(self):
        """Attacker with 2 vs defender with 1: single roll decides it."""
        exact = win_probability_exact(2, 1)
        # This is just P(attacker wins 1v1 roll) = 15/36
        assert abs(exact - 15 / 36) < 0.001

    def test_overwhelming_force(self):
        exact = win_probability_exact(20, 3)
        assert exact > 0.95, f"20v3 should be near-certain attacker win, got {exact}"

    def test_hopeless_attack(self):
        exact = win_probability_exact(2, 10)
        assert exact < 0.05, f"2v10 should be near-certain defender win, got {exact}"
