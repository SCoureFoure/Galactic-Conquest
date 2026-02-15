from engine.combat import resolve_single_round
from engine.models import Army
from engine.tuning import CombatTuning


class ConstantRng:
    def randint(self, a, b):  # noqa: ARG002
        return 3


class TestCombatTuning:
    def test_default_is_vanilla(self):
        tuning = CombatTuning()
        assert tuning.attacker_total_bonus() == 0
        assert tuning.defender_total_bonus() == 0

    def test_upgrade_levels_are_clamped(self):
        tuning = CombatTuning(
            hero_upgrade_level=99,
            planet_upgrade_level=-5,
            hero_value_per_upgrade=2,
            planet_value_per_upgrade=2,
            max_hero_upgrade_level=3,
            max_planet_upgrade_level=3,
        )
        assert tuning.clamped_hero_upgrade_level() == 3
        assert tuning.clamped_planet_upgrade_level() == 0
        assert tuning.attacker_total_bonus() == 6
        assert tuning.defender_total_bonus() == 0


class TestTunedRoundResolution:
    def test_attacker_ability_bonus_can_break_ties(self):
        attacker = Army(units=5)
        defender = Army(units=5)
        tuning = CombatTuning(attacker_ability=1)
        result = resolve_single_round(attacker, defender, rng=ConstantRng(), tuning=tuning)
        assert result.attacker_losses == 0
        assert result.defender_losses == 2

    def test_equal_bonuses_preserve_tie_advantage_for_defender(self):
        attacker = Army(units=5)
        defender = Army(units=5)
        tuning = CombatTuning(attacker_ability=1, defender_ability=1)
        result = resolve_single_round(attacker, defender, rng=ConstantRng(), tuning=tuning)
        assert result.attacker_losses == 2
        assert result.defender_losses == 0

    def test_symmetric_upgrade_levels_remain_symmetric(self):
        attacker = Army(units=5)
        defender = Army(units=5)
        tuning = CombatTuning(
            hero_upgrade_level=3,
            planet_upgrade_level=3,
            hero_value_per_upgrade=2,
            planet_value_per_upgrade=2,
        )
        result = resolve_single_round(attacker, defender, rng=ConstantRng(), tuning=tuning)
        assert result.attacker_losses == 2
        assert result.defender_losses == 0
