from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Hero:
    name: str
    die_size: int = 6  # d6, d8, d10, d12

    def __str__(self) -> str:
        return f"{self.name} (d{self.die_size})"


@dataclass
class Structure:
    name: str
    effect: str  # "reroll_lowest", "extra_defender_die", "ties_favor_attacker"
    description: str = ""

    def __str__(self) -> str:
        return self.name


@dataclass
class Army:
    units: int
    hero: Hero | None = None
    structures: list[Structure] = field(default_factory=list)


@dataclass
class RoundResult:
    attacker_rolls: list[int]
    defender_rolls: list[int]
    attacker_losses: int
    defender_losses: int
    attacker_remaining: int
    defender_remaining: int
    notes: list[str] = field(default_factory=list)


@dataclass
class BattleResult:
    rounds: list[RoundResult]
    attacker_remaining: int
    defender_remaining: int
    attacker_retreated: bool
    winner: str  # "attacker" or "defender"
