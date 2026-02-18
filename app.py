from dataclasses import asdict
from typing import Any

from flask import Flask, jsonify, render_template, request

from engine.combat import resolve_battle, resolve_single_round
from engine.heroes import HERO_TIERS
from engine.models import Army, Hero
from engine.probabilities import (
    SINGLE_ROLL_PROBABILITIES,
    expected_losses,
    win_probability_exact,
)
from engine.simulation import SimulationConfig, run_simulation
from engine.structures import STRUCTURES
from engine.tuning import CombatTuning, PLANET_UPGRADE_MODES

app = Flask(__name__)

DEFAULT_COMBAT_TUNING = CombatTuning()
ABILITY_MIN = -6
ABILITY_MAX = 6
VALUE_PER_UPGRADE_MIN = 0
VALUE_PER_UPGRADE_MAX = 4


def _safe_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _clamp(value: int, minimum: int, maximum: int) -> int:
    if value < minimum:
        return minimum
    if value > maximum:
        return maximum
    return value


def _parse_army(data: dict) -> Army:
    hero = None
    hero_key = data.get("hero")
    if hero_key and hero_key in HERO_TIERS:
        hero = Hero(name=hero_key, die_size=HERO_TIERS[hero_key])

    structs = [STRUCTURES[s] for s in data.get("structures", []) if s in STRUCTURES]
    units = max(1, _safe_int(data.get("units", 1), 1))
    return Army(units=units, hero=hero, structures=structs)


def _parse_tuning(data: dict) -> CombatTuning:
    raw_balance = data.get("balance", {})
    if not isinstance(raw_balance, dict):
        raw_balance = {}

    return CombatTuning(
        attacker_ability=_clamp(
            _safe_int(raw_balance.get("attacker_ability", DEFAULT_COMBAT_TUNING.attacker_ability), 0),
            ABILITY_MIN,
            ABILITY_MAX,
        ),
        defender_ability=_clamp(
            _safe_int(raw_balance.get("defender_ability", DEFAULT_COMBAT_TUNING.defender_ability), 0),
            ABILITY_MIN,
            ABILITY_MAX,
        ),
        hero_upgrade_level=_clamp(
            _safe_int(raw_balance.get("hero_upgrade_level", DEFAULT_COMBAT_TUNING.hero_upgrade_level), 0),
            0,
            DEFAULT_COMBAT_TUNING.max_hero_upgrade_level,
        ),
        planet_upgrade_level=_clamp(
            _safe_int(raw_balance.get("planet_upgrade_level", DEFAULT_COMBAT_TUNING.planet_upgrade_level), 0),
            0,
            DEFAULT_COMBAT_TUNING.max_planet_upgrade_level,
        ),
        hero_value_per_upgrade=_clamp(
            _safe_int(
                raw_balance.get("hero_value_per_upgrade", DEFAULT_COMBAT_TUNING.hero_value_per_upgrade),
                DEFAULT_COMBAT_TUNING.hero_value_per_upgrade,
            ),
            VALUE_PER_UPGRADE_MIN,
            VALUE_PER_UPGRADE_MAX,
        ),
        planet_value_per_upgrade=_clamp(
            _safe_int(
                raw_balance.get("planet_value_per_upgrade", DEFAULT_COMBAT_TUNING.planet_value_per_upgrade),
                DEFAULT_COMBAT_TUNING.planet_value_per_upgrade,
            ),
            VALUE_PER_UPGRADE_MIN,
            VALUE_PER_UPGRADE_MAX,
        ),
        max_hero_upgrade_level=DEFAULT_COMBAT_TUNING.max_hero_upgrade_level,
        max_planet_upgrade_level=DEFAULT_COMBAT_TUNING.max_planet_upgrade_level,
        planet_upgrade_mode=(
            raw_balance.get("planet_upgrade_mode")
            if raw_balance.get("planet_upgrade_mode") in PLANET_UPGRADE_MODES
            else DEFAULT_COMBAT_TUNING.planet_upgrade_mode
        ),
    )


def _attacker_slider_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "atk-ability",
            "key": "attacker_ability",
            "label": "Ability value",
            "help": "Flat modifier added to each attacker comparison.",
            "min": ABILITY_MIN,
            "max": ABILITY_MAX,
            "step": 1,
            "value": DEFAULT_COMBAT_TUNING.attacker_ability,
        },
        {
            "id": "hero-upgrade-level",
            "key": "hero_upgrade_level",
            "label": "Hero upgrade level",
            "help": "Current hero tech tier. Zero keeps baseline Risk odds.",
            "min": 0,
            "max": DEFAULT_COMBAT_TUNING.max_hero_upgrade_level,
            "step": 1,
            "value": DEFAULT_COMBAT_TUNING.hero_upgrade_level,
        },
        {
            "id": "hero-value-per-upgrade",
            "key": "hero_value_per_upgrade",
            "label": "Hero value per upgrade",
            "help": "Multiplier for each hero upgrade level.",
            "min": VALUE_PER_UPGRADE_MIN,
            "max": VALUE_PER_UPGRADE_MAX,
            "step": 1,
            "value": DEFAULT_COMBAT_TUNING.hero_value_per_upgrade,
        },
    ]


def _defender_slider_specs() -> list[dict[str, Any]]:
    return [
        {
            "id": "def-ability",
            "key": "defender_ability",
            "label": "Ability value",
            "help": "Flat modifier added to each defender comparison.",
            "min": ABILITY_MIN,
            "max": ABILITY_MAX,
            "step": 1,
            "value": DEFAULT_COMBAT_TUNING.defender_ability,
        },
        {
            "id": "planet-upgrade-level",
            "key": "planet_upgrade_level",
            "label": "Planet upgrade level",
            "help": "Current planet defense tier. Zero keeps baseline Risk odds.",
            "min": 0,
            "max": DEFAULT_COMBAT_TUNING.max_planet_upgrade_level,
            "step": 1,
            "value": DEFAULT_COMBAT_TUNING.planet_upgrade_level,
        },
        {
            "id": "planet-value-per-upgrade",
            "key": "planet_value_per_upgrade",
            "label": "Planet value per upgrade",
            "help": "Multiplier for each planet upgrade level.",
            "min": VALUE_PER_UPGRADE_MIN,
            "max": VALUE_PER_UPGRADE_MAX,
            "step": 1,
            "value": DEFAULT_COMBAT_TUNING.planet_value_per_upgrade,
        },
    ]


def _planet_upgrade_mode_specs() -> list[dict[str, str]]:
    return [
        {
            "value": "flat_bonus",
            "label": "Flat Defender Bonus",
            "help": "Current model: each level adds a numeric defender comparison bonus.",
        },
        {
            "value": "reroll_lowest_defender",
            "label": "Reroll Lowest Defender Die",
            "help": "Each level grants reroll power (up to 2 rerolls) on defender's lowest die each round.",
        },
        {
            "value": "suppress_attacker_highest",
            "label": "Suppress Highest Attacker Die",
            "help": "Each level reduces the attacker's top die (up to -3) before comparisons.",
        },
    ]


@app.route("/")
def index():
    return render_template(
        "index.html",
        hero_tiers=HERO_TIERS,
        structures=STRUCTURES,
        attacker_sliders=_attacker_slider_specs(),
        defender_sliders=_defender_slider_specs(),
        planet_upgrade_modes=_planet_upgrade_mode_specs(),
        default_planet_upgrade_mode=DEFAULT_COMBAT_TUNING.planet_upgrade_mode,
    )


@app.route("/api/battle", methods=["POST"])
def battle():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    attacker = _parse_army(data.get("attacker", {}))
    defender = _parse_army(data.get("defender", {}))
    auto = data.get("auto_resolve", True)
    tuning = _parse_tuning(data)

    result = resolve_battle(attacker, defender, auto_resolve=auto, tuning=tuning)
    return jsonify(asdict(result))


@app.route("/api/round", methods=["POST"])
def single_round():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    attacker = _parse_army(data.get("attacker", {}))
    defender = _parse_army(data.get("defender", {}))
    tuning = _parse_tuning(data)

    result = resolve_single_round(attacker, defender, tuning=tuning)
    return jsonify(asdict(result))


@app.route("/api/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    atk = data.get("attacker", {})
    dfn = data.get("defender", {})

    hero_atk = None
    if atk.get("hero") and atk["hero"] in HERO_TIERS:
        hero_atk = Hero(name=atk["hero"], die_size=HERO_TIERS[atk["hero"]])

    structs = [STRUCTURES[s] for s in dfn.get("structures", []) if s in STRUCTURES]
    tuning = _parse_tuning(data)

    config = SimulationConfig(
        attacker_units=max(2, _safe_int(atk.get("units", 10), 10)),
        defender_units=max(1, _safe_int(dfn.get("units", 5), 5)),
        attacker_hero=hero_atk,
        defender_structures=structs,
        tuning=tuning,
        num_battles=min(50000, max(100, _safe_int(data.get("num_battles", 10000), 10000))),
    )

    result = run_simulation(config)
    return jsonify(asdict(result))


@app.route("/api/exact", methods=["POST"])
def exact_probability():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    atk_units = max(2, min(50, _safe_int(data.get("attacker_units", 10), 10)))
    def_units = max(1, min(50, _safe_int(data.get("defender_units", 5), 5)))

    win_prob = win_probability_exact(atk_units, def_units)

    # Single-roll stats for the main combat phase (3v2)
    atk_dice = min(3, atk_units - 1)
    def_dice = min(2, def_units)
    atk_exp, def_exp = expected_losses(atk_dice, def_dice)

    # Build the per-roll probability breakdown
    roll_probs = {}
    for (ad, dd), outcomes in SINGLE_ROLL_PROBABILITIES.items():
        roll_probs[f"{ad}v{dd}"] = {
            f"atk_loses_{al}_def_loses_{dl}": round(float(p), 4)
            for (al, dl), p in outcomes.items()
        }

    return jsonify({
        "attacker_units": atk_units,
        "defender_units": def_units,
        "attacker_win_probability": round(win_prob * 100, 2),
        "defender_win_probability": round((1 - win_prob) * 100, 2),
        "current_roll_type": f"{atk_dice}v{def_dice}",
        "expected_attacker_losses_per_roll": atk_exp,
        "expected_defender_losses_per_roll": def_exp,
        "single_roll_probabilities": roll_probs,
    })


if __name__ == "__main__":
    app.run(debug=True)
