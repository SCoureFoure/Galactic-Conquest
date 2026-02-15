"""Exact probability matrices for Risk dice from Taflin (2001).

'The Probability Distribution of Risk Battles' by Daniel C. Taflin
provides exact probabilities for every attacker/defender dice combination.

Each entry maps (atk_dice, def_dice) to a dict of outcomes:
  (atk_losses, def_losses) -> exact probability as a fraction.
"""

from __future__ import annotations

from fractions import Fraction


# Table 1 from the Taflin paper — exact probabilities for a single roll.
# Key: (attacker_dice, defender_dice)
# Value: dict of {(attacker_losses, defender_losses): Fraction}
SINGLE_ROLL_PROBABILITIES: dict[tuple[int, int], dict[tuple[int, int], Fraction]] = {
    (1, 1): {
        (0, 1): Fraction(15, 36),
        (1, 0): Fraction(21, 36),
    },
    (1, 2): {
        (0, 1): Fraction(55, 216),
        (1, 0): Fraction(161, 216),
    },
    (2, 1): {
        (0, 1): Fraction(125, 216),
        (1, 0): Fraction(91, 216),
    },
    (2, 2): {
        (0, 2): Fraction(295, 1296),
        (1, 1): Fraction(420, 1296),
        (2, 0): Fraction(581, 1296),
    },
    (3, 1): {
        (0, 1): Fraction(855, 1296),
        (1, 0): Fraction(441, 1296),
    },
    (3, 2): {
        (0, 2): Fraction(2890, 7776),
        (1, 1): Fraction(2611, 7776),
        (2, 0): Fraction(2275, 7776),
    },
}


def expected_losses(atk_dice: int, def_dice: int) -> tuple[float, float]:
    """Return (expected_attacker_losses, expected_defender_losses) per roll."""
    probs = SINGLE_ROLL_PROBABILITIES.get((atk_dice, def_dice))
    if probs is None:
        raise ValueError(f"No probability data for ({atk_dice}, {def_dice})")
    atk_loss = sum(al * float(p) for (al, dl), p in probs.items())
    def_loss = sum(dl * float(p) for (al, dl), p in probs.items())
    return (round(atk_loss, 4), round(def_loss, 4))


def attacker_advantage_ratio(atk_dice: int, def_dice: int) -> float:
    """Return the ratio of defender losses to attacker losses.

    Values > 1 mean the attacker has the advantage.
    For 3v2: this is ~1.17 (attacker loses 15% slower than defender).
    """
    atk, dfn = expected_losses(atk_dice, def_dice)
    if atk == 0:
        return float("inf")
    return round(dfn / atk, 4)


def win_probability_exact(atk_armies: int, def_armies: int) -> float:
    """Calculate exact attacker win probability using Markov chain approach.

    This implements the random walk through (A, D) space described in the
    Taflin paper. We compute Q(a, d) = probability attacker wins from
    state (a, d) for all reachable states using dynamic programming.

    Boundary conditions:
      Q(1, d) = 0 for all d >= 1  (attacker can't attack with 1 unit)
      Q(a, 0) = 1 for all a >= 1  (defender eliminated)
    """
    if atk_armies <= 1:
        return 0.0
    if def_armies <= 0:
        return 1.0

    # Build DP table: q[a][d] = probability attacker wins from (a, d)
    max_a = atk_armies + 1
    max_d = def_armies + 1

    q: list[list[float]] = [[0.0] * max_d for _ in range(max_a)]

    # Base cases: defender at 0 means attacker won
    for a in range(max_a):
        q[a][0] = 1.0

    # Fill in from small states upward
    for a in range(2, max_a):
        for d in range(1, max_d):
            atk_dice = min(3, a - 1)
            def_dice = min(2, d)
            probs = SINGLE_ROLL_PROBABILITIES[(atk_dice, def_dice)]

            val = 0.0
            for (al, dl), p in probs.items():
                new_a = a - al
                new_d = d - dl
                if new_a < 1:
                    new_a = 1
                if new_d < 0:
                    new_d = 0
                val += float(p) * q[new_a][new_d]
            q[a][d] = val

    return round(q[atk_armies][def_armies], 6)
