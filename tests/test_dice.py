import random

from engine.dice import reroll_lowest, roll


class TestRoll:
    def test_returns_correct_count(self):
        result = roll(3)
        assert len(result) == 3

    def test_returns_empty_for_zero(self):
        assert roll(0) == []

    def test_returns_empty_for_negative(self):
        assert roll(-1) == []

    def test_values_within_range_d6(self):
        rng = random.Random(42)
        for _ in range(100):
            result = roll(3, die_size=6, rng=rng)
            for val in result:
                assert 1 <= val <= 6

    def test_values_within_range_d10(self):
        rng = random.Random(42)
        for _ in range(100):
            result = roll(2, die_size=10, rng=rng)
            for val in result:
                assert 1 <= val <= 10

    def test_sorted_descending(self):
        rng = random.Random(42)
        for _ in range(50):
            result = roll(3, rng=rng)
            assert result == sorted(result, reverse=True)

    def test_deterministic_with_seed(self):
        rng1 = random.Random(99)
        rng2 = random.Random(99)
        assert roll(3, rng=rng1) == roll(3, rng=rng2)


class TestRerollLowest:
    def test_empty_list(self):
        assert reroll_lowest([]) == []

    def test_single_die(self):
        rng = random.Random(42)
        result = reroll_lowest([3], die_size=6, rng=rng)
        assert len(result) == 1
        assert 1 <= result[0] <= 6

    def test_result_sorted_descending(self):
        rng = random.Random(42)
        for _ in range(50):
            result = reroll_lowest([5, 3, 1], die_size=6, rng=rng)
            assert result == sorted(result, reverse=True)

    def test_preserves_length(self):
        rng = random.Random(42)
        result = reroll_lowest([6, 4, 2], die_size=6, rng=rng)
        assert len(result) == 3
