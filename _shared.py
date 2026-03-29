import json
from dataclasses import asdict
from typing import Any

from engine.heroes import HERO_TIERS
from engine.models import Army, Hero
from engine.structures import STRUCTURES
from engine.tuning import CombatTuning, PLANET_UPGRADE_MODES

DEFAULT_COMBAT_TUNING = CombatTuning()
ABILITY_MIN = -6
ABILITY_MAX = 6
VALUE_PER_UPGRADE_MIN = 0
VALUE_PER_UPGRADE_MAX = 4


# --- HTTP helpers ---

def send_json(h, data: Any, status: int = 200) -> None:
    body = json.dumps(data).encode()
    h.send_response(status)
    h.send_header("Content-Type", "application/json")
    h.send_header("Content-Length", str(len(body)))
    h.end_headers()
    h.wfile.write(body)


def read_json_body(h) -> dict:
    length = int(h.headers.get("Content-Length", 0))
    raw = h.rfile.read(length)
    return json.loads(raw) if raw else {}


# --- Parsing helpers ---

def _safe_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def _parse_army(data: dict) -> Army:
    hero = None
    hero_key = data.get("hero")
    if hero_key and hero_key in HERO_TIERS:
        hero = Hero(name=hero_key, die_size=HERO_TIERS[hero_key])
    structs = [STRUCTURES[s] for s in data.get("structures", []) if s in STRUCTURES]
    units = max(1, _safe_int(data.get("units", 1), 1))
    return Army(units=units, hero=hero, structures=structs)


def _parse_tuning(data: dict) -> CombatTuning:
    raw = data.get("balance", {})
    if not isinstance(raw, dict):
        raw = {}
    d = DEFAULT_COMBAT_TUNING
    return CombatTuning(
        attacker_ability=_clamp(_safe_int(raw.get("attacker_ability", d.attacker_ability), 0), ABILITY_MIN, ABILITY_MAX),
        defender_ability=_clamp(_safe_int(raw.get("defender_ability", d.defender_ability), 0), ABILITY_MIN, ABILITY_MAX),
        hero_upgrade_level=_clamp(_safe_int(raw.get("hero_upgrade_level", d.hero_upgrade_level), 0), 0, d.max_hero_upgrade_level),
        planet_upgrade_level=_clamp(_safe_int(raw.get("planet_upgrade_level", d.planet_upgrade_level), 0), 0, d.max_planet_upgrade_level),
        hero_value_per_upgrade=_clamp(_safe_int(raw.get("hero_value_per_upgrade", d.hero_value_per_upgrade), d.hero_value_per_upgrade), VALUE_PER_UPGRADE_MIN, VALUE_PER_UPGRADE_MAX),
        planet_value_per_upgrade=_clamp(_safe_int(raw.get("planet_value_per_upgrade", d.planet_value_per_upgrade), d.planet_value_per_upgrade), VALUE_PER_UPGRADE_MIN, VALUE_PER_UPGRADE_MAX),
        max_hero_upgrade_level=d.max_hero_upgrade_level,
        max_planet_upgrade_level=d.max_planet_upgrade_level,
        planet_upgrade_mode=(
            raw.get("planet_upgrade_mode")
            if raw.get("planet_upgrade_mode") in PLANET_UPGRADE_MODES
            else d.planet_upgrade_mode
        ),
    )


# --- Config spec builders ---

def attacker_slider_specs() -> list[dict]:
    d = DEFAULT_COMBAT_TUNING
    return [
        {"id": "atk-ability", "key": "attacker_ability", "label": "Ability value", "help": "Flat modifier added to each attacker comparison.", "min": ABILITY_MIN, "max": ABILITY_MAX, "step": 1, "value": d.attacker_ability},
        {"id": "hero-upgrade-level", "key": "hero_upgrade_level", "label": "Hero upgrade level", "help": "Current hero tech tier. Zero keeps baseline Risk odds.", "min": 0, "max": d.max_hero_upgrade_level, "step": 1, "value": d.hero_upgrade_level},
        {"id": "hero-value-per-upgrade", "key": "hero_value_per_upgrade", "label": "Hero value per upgrade", "help": "Multiplier for each hero upgrade level.", "min": VALUE_PER_UPGRADE_MIN, "max": VALUE_PER_UPGRADE_MAX, "step": 1, "value": d.hero_value_per_upgrade},
    ]


def defender_slider_specs() -> list[dict]:
    d = DEFAULT_COMBAT_TUNING
    return [
        {"id": "def-ability", "key": "defender_ability", "label": "Ability value", "help": "Flat modifier added to each defender comparison.", "min": ABILITY_MIN, "max": ABILITY_MAX, "step": 1, "value": d.defender_ability},
        {"id": "planet-upgrade-level", "key": "planet_upgrade_level", "label": "Planet upgrade level", "help": "Current planet defense tier. Zero keeps baseline Risk odds.", "min": 0, "max": d.max_planet_upgrade_level, "step": 1, "value": d.planet_upgrade_level},
        {"id": "planet-value-per-upgrade", "key": "planet_value_per_upgrade", "label": "Planet value per upgrade", "help": "Multiplier for each planet upgrade level.", "min": VALUE_PER_UPGRADE_MIN, "max": VALUE_PER_UPGRADE_MAX, "step": 1, "value": d.planet_value_per_upgrade},
    ]


def planet_upgrade_mode_specs() -> list[dict]:
    return [
        {"value": "flat_bonus", "label": "Flat Defender Bonus", "help": "Current model: each level adds a numeric defender comparison bonus."},
        {"value": "reroll_lowest_defender", "label": "Reroll Lowest Defender Die", "help": "Each level grants reroll power (up to 2 rerolls) on defender's lowest die each round."},
        {"value": "suppress_attacker_highest", "label": "Suppress Highest Attacker Die", "help": "Each level reduces the attacker's top die (up to -3) before comparisons."},
    ]


def structures_config() -> dict:
    return {key: {"name": s.name, "description": s.description} for key, s in STRUCTURES.items()}
