import random

from engine.heroes import get_die_size, roll_with_hero
from engine.models import Hero


class TestGetDieSize:
    def test_no_hero(self):
        assert get_die_size(None) == 6

    def test_captain(self):
        assert get_die_size(Hero("Captain", 8)) == 8

    def test_admiral(self):
        assert get_die_size(Hero("Admiral", 12)) == 12


class TestRollWithHero:
    def test_returns_correct_count(self):
        result = roll_with_hero(3, None)
        assert len(result) == 3

    def test_empty_for_zero(self):
        assert roll_with_hero(0, None) == []

    def test_no_hero_all_d6(self):
        rng = random.Random(42)
        for _ in range(100):
            result = roll_with_hero(3, None, rng)
            for val in result:
                assert 1 <= val <= 6

    def test_hero_can_exceed_d6(self):
        """A d10 hero should eventually roll a 7+ (impossible on d6)."""
        rng = random.Random(42)
        hero = Hero("General", 10)
        max_val = 0
        for _ in range(200):
            result = roll_with_hero(1, hero, rng)
            max_val = max(max_val, result[0])
        assert max_val > 6, "d10 hero never rolled above 6 in 200 attempts"

    def test_sorted_descending(self):
        rng = random.Random(42)
        hero = Hero("Captain", 8)
        for _ in range(50):
            result = roll_with_hero(3, hero, rng)
            assert result == sorted(result, reverse=True)
