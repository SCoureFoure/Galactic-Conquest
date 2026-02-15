from __future__ import annotations

from engine.models import Structure


# Pre-defined structures available in the game
#
# Design philosophy: structures are ARMOR, not evasion.
# The attacker still swings big with hero dice — but a fortified planet
# absorbs the punishment. Structures reduce/negate defender losses.
STRUCTURES: dict[str, Structure] = {
    "shield_generator": Structure(
        "Shield Generator",
        "absorb",
        "Planetary energy shield absorbs incoming fire. "
        "Negates 1 defender loss per combat round.",
    ),
    "orbital_battery": Structure(
        "Orbital Battery",
        "extra_defender_die",
        "Automated weapons platform in high orbit. "
        "Grants the defender +1 extra die when defending.",
    ),
    "fortress": Structure(
        "Fortress",
        "absorb",
        "Deep underground bunker complex protects garrison troops. "
        "Negates 1 defender loss per combat round.",
    ),
}


def has_effect(structures: list[Structure], effect: str) -> bool:
    """Check if any structure in the list provides the given effect."""
    return any(s.effect == effect for s in structures)


def damage_absorbed(structures: list[Structure]) -> int:
    """Return the number of defender losses negated per round by structures."""
    return sum(1 for s in structures if s.effect == "absorb")


def extra_defender_dice(structures: list[Structure]) -> int:
    """Return the number of extra dice granted by structures."""
    return sum(1 for s in structures if s.effect == "extra_defender_die")
