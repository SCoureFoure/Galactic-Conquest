from __future__ import annotations

import random as _random
from typing import Any

from engine.heroes import roll_with_hero
from engine.models import Army, BattleResult, RoundResult
from engine.structures import damage_absorbed, extra_defender_dice
from engine.tuning import CombatTuning


def resolve_single_round(
    attacker: Army,
    defender: Army,
    rng: Any = _random,
    tuning: CombatTuning | None = None,
) -> RoundResult:
    """Resolve one round of combat between attacker and defender.

    Risk rules:
    - Attacker rolls up to 3 dice, must leave at least 1 unit behind
    - Defender rolls up to 2 dice (+ bonus from structures)
    - Compare highest pairs, defender wins ties
    - Structures absorb defender losses (damage reduction)
    """
    notes: list[str] = []
    active_tuning = tuning or CombatTuning()

    # Determine dice counts
    atk_dice = min(3, attacker.units - 1)
    base_def_dice = min(2, defender.units)
    bonus_dice = extra_defender_dice(defender.structures)
    def_dice = base_def_dice + bonus_dice
    if bonus_dice > 0:
        notes.append(f"Orbital Battery grants +{bonus_dice} defender die")

    # Roll dice. Heroes upgrade attacker dice only.
    atk_rolls = roll_with_hero(atk_dice, attacker.hero, rng)
    def_rolls = roll_with_hero(def_dice, None, rng)

    if attacker.hero and attacker.hero.die_size > 6:
        notes.append(f"{attacker.hero.name} upgrades one attack die to d{attacker.hero.die_size}")

    hero_upgrade_bonus = active_tuning.hero_upgrade_bonus()
    planet_upgrade_bonus = active_tuning.planet_upgrade_bonus()
    atk_bonus = active_tuning.attacker_total_bonus()
    def_bonus = active_tuning.defender_total_bonus()

    if hero_upgrade_bonus > 0:
        notes.append(f"Hero upgrades add +{hero_upgrade_bonus} attacker ability")
    if planet_upgrade_bonus > 0:
        notes.append(f"Planet upgrades add +{planet_upgrade_bonus} defender ability")
    if active_tuning.attacker_ability != 0:
        notes.append(f"Attacker base ability modifier: {active_tuning.attacker_ability:+d}")
    if active_tuning.defender_ability != 0:
        notes.append(f"Defender base ability modifier: {active_tuning.defender_ability:+d}")

    # Compare sorted pairs. Defender wins ties (standard Risk).
    atk_losses = 0
    def_losses = 0
    pairs = min(len(atk_rolls), len(def_rolls))

    for i in range(pairs):
        if atk_rolls[i] + atk_bonus > def_rolls[i] + def_bonus:
            def_losses += 1
        else:  # defender wins ties
            atk_losses += 1

    # Apply damage absorption from structures
    absorbed = min(def_losses, damage_absorbed(defender.structures))
    if absorbed > 0:
        def_losses -= absorbed
        notes.append(f"Structures absorb {absorbed} defender loss{'es' if absorbed > 1 else ''}")

    # Apply losses
    attacker.units -= atk_losses
    defender.units -= def_losses

    return RoundResult(
        attacker_rolls=atk_rolls,
        defender_rolls=def_rolls,
        attacker_losses=atk_losses,
        defender_losses=def_losses,
        attacker_remaining=attacker.units,
        defender_remaining=defender.units,
        notes=notes,
    )


def resolve_battle(
    attacker: Army,
    defender: Army,
    auto_resolve: bool = True,
    rng: Any = _random,
    tuning: CombatTuning | None = None,
) -> BattleResult:
    """Resolve a full battle (potentially multiple rounds).

    If auto_resolve is True, fights until one side is eliminated.
    If False, resolves a single round (caller manages round-by-round flow).
    """
    rounds: list[RoundResult] = []

    while attacker.units > 1 and defender.units > 0:
        result = resolve_single_round(attacker, defender, rng=rng, tuning=tuning)
        rounds.append(result)
        if not auto_resolve:
            break

    winner = "attacker" if defender.units <= 0 else "defender"
    return BattleResult(
        rounds=rounds,
        attacker_remaining=attacker.units,
        defender_remaining=defender.units,
        attacker_retreated=False,
        winner=winner,
    )
