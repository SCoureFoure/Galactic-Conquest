import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from http.server import BaseHTTPRequestHandler
from dataclasses import asdict
from _shared import _parse_army, _parse_tuning, send_json, read_json_body
from engine.combat import resolve_battle


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = read_json_body(self)
        except Exception:
            send_json(self, {"error": "Invalid JSON body"}, 400)
            return

        attacker = _parse_army(data.get("attacker", {}))
        defender = _parse_army(data.get("defender", {}))
        auto = data.get("auto_resolve", True)
        tuning = _parse_tuning(data)

        result = resolve_battle(attacker, defender, auto_resolve=auto, tuning=tuning)
        send_json(self, asdict(result))

    def log_message(self, format, *args):
        pass
