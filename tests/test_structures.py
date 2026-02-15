from engine.models import Structure
from engine.structures import (
    STRUCTURES,
    damage_absorbed,
    extra_defender_dice,
    has_effect,
)


class TestHasEffect:
    def test_finds_matching_effect(self):
        structs = [Structure("Test", "absorb")]
        assert has_effect(structs, "absorb") is True

    def test_no_match(self):
        structs = [Structure("Test", "absorb")]
        assert has_effect(structs, "extra_defender_die") is False

    def test_empty_list(self):
        assert has_effect([], "absorb") is False


class TestDamageAbsorbed:
    def test_no_structures(self):
        assert damage_absorbed([]) == 0

    def test_single_absorb(self):
        shield = STRUCTURES["shield_generator"]
        assert damage_absorbed([shield]) == 1

    def test_stacked_absorb(self):
        shield = STRUCTURES["shield_generator"]
        fortress = STRUCTURES["fortress"]
        assert damage_absorbed([shield, fortress]) == 2

    def test_non_absorb_structure(self):
        battery = STRUCTURES["orbital_battery"]
        assert damage_absorbed([battery]) == 0


class TestExtraDefenderDice:
    def test_no_structures(self):
        assert extra_defender_dice([]) == 0

    def test_orbital_battery(self):
        battery = STRUCTURES["orbital_battery"]
        assert extra_defender_dice([battery]) == 1

    def test_non_dice_structure(self):
        shield = STRUCTURES["shield_generator"]
        assert extra_defender_dice([shield]) == 0
