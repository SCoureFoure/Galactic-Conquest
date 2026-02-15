import random

from engine.combat import resolve_battle, resolve_single_round
from engine.models import Army, Hero, Structure
from engine.structures import STRUCTURES


class TestResolveSingleRound:
    def test_attacker_must_leave_one_unit(self):
        """Attacker with 2 units should only roll 1 die (keeps 1 behind)."""
        rng = random.Random(42)
        attacker = Army(units=2)
        defender = Army(units=2)
        result = resolve_single_round(attacker, defender, rng)
        assert len(result.attacker_rolls) == 1

    def test_attacker_max_three_dice(self):
        rng = random.Random(42)
        attacker = Army(units=10)
        defender = Army(units=5)
        result = resolve_single_round(attacker, defender, rng)
        assert len(result.attacker_rolls) == 3

    def test_defender_max_two_dice(self):
        rng = random.Random(42)
        attacker = Army(units=10)
        defender = Army(units=5)
        result = resolve_single_round(attacker, defender, rng)
        assert len(result.defender_rolls) == 2

    def test_losses_sum_to_pairs_without_structures(self):
        """Without structures, total losses per round equal pairs compared."""
        rng = random.Random(42)
        attacker = Army(units=10)
        defender = Army(units=5)
        result = resolve_single_round(attacker, defender, rng)
        pairs = min(len(result.attacker_rolls), len(result.defender_rolls))
        assert result.attacker_losses + result.defender_losses == pairs

    def test_defender_wins_ties_by_default(self):
        """When both roll the same, defender should win (attacker loses)."""
        class ConstantRng:
            def randint(self, a, b):
                return 3

        attacker = Army(units=5)
        defender = Army(units=5)
        result = resolve_single_round(attacker, defender, ConstantRng())
        # All pairs tie -> all losses go to attacker
        assert result.defender_losses == 0
        assert result.attacker_losses == 2  # min(3, 2) = 2 pairs

    def test_fortress_absorbs_damage(self):
        """Fortress should absorb 1 defender loss per round."""
        class ConstantRng:
            """Attacker always rolls 6, defender always rolls 1."""
            def __init__(self):
                self._call = 0
            def randint(self, a, b):
                self._call += 1
                # First 3 calls are attacker dice, next 2 are defender dice
                return b if self._call <= 3 else a

        fortress = STRUCTURES["fortress"]
        attacker = Army(units=5)
        defender = Army(units=5, structures=[fortress])
        result = resolve_single_round(attacker, defender, ConstantRng())
        # Attacker wins both pairs, but fortress absorbs 1
        assert result.defender_losses == 1  # 2 - 1 absorbed
        assert result.attacker_losses == 0

    def test_stacked_absorb_caps_at_losses(self):
        """Absorption can't reduce defender losses below 0."""
        shield = STRUCTURES["shield_generator"]
        fortress = STRUCTURES["fortress"]
        # 2 absorb structures but only 1 defender loss possible
        class OneWinRng:
            """Attacker wins first pair, defender wins second."""
            def __init__(self):
                self._calls = iter([6, 1, 1, 1, 6])
            def randint(self, a, b):
                return next(self._calls)

        attacker = Army(units=5)
        defender = Army(units=5, structures=[shield, fortress])
        result = resolve_single_round(attacker, defender, OneWinRng())
        # 1 def loss from dice, 2 absorb available, but can't go below 0
        assert result.defender_losses == 0

    def test_orbital_battery_extra_die(self):
        """Orbital Battery should give defender an extra die."""
        rng = random.Random(42)
        battery = STRUCTURES["orbital_battery"]
        attacker = Army(units=10)
        defender = Army(units=5, structures=[battery])
        result = resolve_single_round(attacker, defender, rng)
        assert len(result.defender_rolls) == 3  # 2 base + 1 bonus

    def test_units_updated_after_round(self):
        rng = random.Random(42)
        attacker = Army(units=10)
        defender = Army(units=5)
        result = resolve_single_round(attacker, defender, rng)
        assert attacker.units == result.attacker_remaining
        assert defender.units == result.defender_remaining

    def test_hero_noted_in_round(self):
        rng = random.Random(42)
        hero = Hero("General", 10)
        attacker = Army(units=10, hero=hero)
        defender = Army(units=5)
        result = resolve_single_round(attacker, defender, rng)
        assert any("General" in n for n in result.notes)


class TestResolveBattle:
    def test_battle_terminates(self):
        """An auto-resolved battle should always terminate."""
        rng = random.Random(42)
        attacker = Army(units=10)
        defender = Army(units=5)
        result = resolve_battle(attacker, defender, auto_resolve=True, rng=rng)
        assert result.winner in ("attacker", "defender")
        assert len(result.rounds) > 0

    def test_attacker_wins_when_defender_eliminated(self):
        rng = random.Random(42)
        attacker = Army(units=20)
        defender = Army(units=2)
        result = resolve_battle(attacker, defender, auto_resolve=True, rng=rng)
        assert result.defender_remaining == 0
        assert result.winner == "attacker"

    def test_single_round_mode(self):
        rng = random.Random(42)
        attacker = Army(units=10)
        defender = Army(units=5)
        result = resolve_battle(attacker, defender, auto_resolve=False, rng=rng)
        assert len(result.rounds) == 1

    def test_attacker_stops_at_one_unit(self):
        """Attacker can't attack with only 1 unit remaining."""
        rng = random.Random(42)
        attacker = Army(units=3)
        defender = Army(units=20)
        result = resolve_battle(attacker, defender, auto_resolve=True, rng=rng)
        assert result.attacker_remaining >= 1
        assert result.winner == "defender"

    def test_battle_with_attacker_hero(self):
        """Heroes are attacker-only — they upgrade attack dice."""
        rng = random.Random(42)
        attacker = Army(units=10, hero=Hero("Admiral", 12))
        defender = Army(units=10)
        result = resolve_battle(attacker, defender, auto_resolve=True, rng=rng)
        assert result.winner in ("attacker", "defender")
        assert len(result.rounds) > 0
