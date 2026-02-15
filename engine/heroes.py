from __future__ import annotations

import random as _random
from typing import Any

from engine.models import Hero


HERO_TIERS: dict[str, int] = {
    "captain": 8,
    "general": 10,
    "admiral": 12,
}


def get_die_size(hero: Hero | None) -> int:
    """Return the die size for a hero, or 6 (standard d6) if no hero."""
    if hero is None:
        return 6
    return hero.die_size


def roll_with_hero(num_dice: int, hero: Hero | None, rng: Any = _random) -> list[int]:
    """Roll dice where the hero upgrades one die to a larger size.

    The hero's die replaces one of the standard d6s. All other dice remain d6.
    """
    if num_dice <= 0:
        return []
    hero_size = get_die_size(hero)
    hero_roll = [rng.randint(1, hero_size)]
    normal_rolls = [rng.randint(1, 6) for _ in range(num_dice - 1)]
    return sorted(hero_roll + normal_rolls, reverse=True)
