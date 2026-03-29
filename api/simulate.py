from http.server import BaseHTTPRequestHandler
from dataclasses import asdict
from _shared import _safe_int, _parse_tuning, send_json, read_json_body
from engine.heroes import HERO_TIERS
from engine.models import Hero
from engine.structures import STRUCTURES
from engine.simulation import SimulationConfig, run_simulation


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = read_json_body(self)
        except Exception:
            send_json(self, {"error": "Invalid JSON body"}, 400)
            return

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
        send_json(self, asdict(result))

    def log_message(self, format, *args):
        pass
