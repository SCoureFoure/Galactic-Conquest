from __future__ import annotations

from dataclasses import dataclass


def _clamp(value: int, minimum: int, maximum: int) -> int:
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


@dataclass(frozen=True)
class CombatTuning:
    """Numeric knobs used to tune combat balance without changing core rules.

    Vanilla Risk behavior is preserved when all values remain at defaults.
    """

    attacker_ability: int = 0
    defender_ability: int = 0
    hero_upgrade_level: int = 0
    planet_upgrade_level: int = 0
    hero_value_per_upgrade: int = 1
    planet_value_per_upgrade: int = 1
    max_hero_upgrade_level: int = 3
    max_planet_upgrade_level: int = 3

    def clamped_hero_upgrade_level(self) -> int:
        return _clamp(self.hero_upgrade_level, 0, max(0, self.max_hero_upgrade_level))

    def clamped_planet_upgrade_level(self) -> int:
        return _clamp(self.planet_upgrade_level, 0, max(0, self.max_planet_upgrade_level))

    def hero_upgrade_bonus(self) -> int:
        return self.clamped_hero_upgrade_level() * self.hero_value_per_upgrade

    def planet_upgrade_bonus(self) -> int:
        return self.clamped_planet_upgrade_level() * self.planet_value_per_upgrade

    def attacker_total_bonus(self) -> int:
        return self.attacker_ability + self.hero_upgrade_bonus()

    def defender_total_bonus(self) -> int:
        return self.defender_ability + self.planet_upgrade_bonus()
