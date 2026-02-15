from __future__ import annotations

import copy
import random as _random
from dataclasses import dataclass, field
from typing import Any

from engine.combat import resolve_battle
from engine.models import Army, Hero, Structure
from engine.tuning import CombatTuning


@dataclass
class SimulationConfig:
    attacker_units: int = 10
    defender_units: int = 5
    attacker_hero: Hero | None = None
    defender_structures: list[Structure] = field(default_factory=list)
    tuning: CombatTuning = field(default_factory=CombatTuning)
    num_battles: int = 10000


@dataclass
class SimulationResult:
    num_battles: int
    attacker_wins: int
    defender_wins: int
    attacker_win_pct: float
    defender_win_pct: float
    avg_rounds: float
    avg_attacker_remaining: float
    avg_defender_remaining: float
    avg_attacker_losses: float
    avg_defender_losses: float
    # Breakdown: when attacker wins, what do the numbers look like?
    atk_win_avg_remaining: float
    atk_win_avg_rounds: float
    # Breakdown: when defender wins, what do the numbers look like?
    def_win_avg_remaining: float
    def_win_avg_rounds: float


def run_simulation(
    config: SimulationConfig,
    rng: Any = _random,
) -> SimulationResult:
    """Run many battles and collect statistics."""
    attacker_wins = 0
    total_rounds = 0
    total_atk_remaining = 0
    total_def_remaining = 0

    # Attacker-win stats
    atk_win_remaining_sum = 0
    atk_win_rounds_sum = 0

    # Defender-win stats
    def_win_remaining_sum = 0
    def_win_rounds_sum = 0

    for _ in range(config.num_battles):
        attacker = Army(
            units=config.attacker_units,
            hero=copy.deepcopy(config.attacker_hero),
            structures=[],
        )
        defender = Army(
            units=config.defender_units,
            structures=list(config.defender_structures),
        )

        result = resolve_battle(
            attacker,
            defender,
            auto_resolve=True,
            rng=rng,
            tuning=config.tuning,
        )
        num_rounds = len(result.rounds)
        total_rounds += num_rounds
        total_atk_remaining += result.attacker_remaining
        total_def_remaining += result.defender_remaining

        if result.winner == "attacker":
            attacker_wins += 1
            atk_win_remaining_sum += result.attacker_remaining
            atk_win_rounds_sum += num_rounds
        else:
            def_win_remaining_sum += result.defender_remaining
            def_win_rounds_sum += num_rounds

    n = config.num_battles
    defender_wins = n - attacker_wins

    return SimulationResult(
        num_battles=n,
        attacker_wins=attacker_wins,
        defender_wins=defender_wins,
        attacker_win_pct=round(attacker_wins / n * 100, 1),
        defender_win_pct=round(defender_wins / n * 100, 1),
        avg_rounds=round(total_rounds / n, 1),
        avg_attacker_remaining=round(total_atk_remaining / n, 1),
        avg_defender_remaining=round(total_def_remaining / n, 1),
        avg_attacker_losses=round(config.attacker_units - total_atk_remaining / n, 1),
        avg_defender_losses=round(config.defender_units - total_def_remaining / n, 1),
        atk_win_avg_remaining=round(atk_win_remaining_sum / attacker_wins, 1) if attacker_wins else 0,
        atk_win_avg_rounds=round(atk_win_rounds_sum / attacker_wins, 1) if attacker_wins else 0,
        def_win_avg_remaining=round(def_win_remaining_sum / defender_wins, 1) if defender_wins else 0,
        def_win_avg_rounds=round(def_win_rounds_sum / defender_wins, 1) if defender_wins else 0,
    )
