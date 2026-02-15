from __future__ import annotations

import random as _random
from typing import Any


def roll(num_dice: int, die_size: int = 6, rng: Any = _random) -> list[int]:
    """Roll num_dice of the given size, return sorted descending."""
    if num_dice <= 0:
        return []
    return sorted([rng.randint(1, die_size) for _ in range(num_dice)], reverse=True)


def reroll_lowest(rolls: list[int], die_size: int = 6, rng: Any = _random) -> list[int]:
    """Reroll the lowest die in the list, return sorted descending."""
    if not rolls:
        return rolls
    result = list(rolls)
    result[-1] = rng.randint(1, die_size)
    return sorted(result, reverse=True)
