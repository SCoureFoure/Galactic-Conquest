from http.server import BaseHTTPRequestHandler
from _shared import _safe_int, send_json, read_json_body
from engine.probabilities import (
    SINGLE_ROLL_PROBABILITIES,
    expected_losses,
    win_probability_exact,
)


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = read_json_body(self)
        except Exception:
            send_json(self, {"error": "Invalid JSON body"}, 400)
            return

        atk_units = max(2, min(50, _safe_int(data.get("attacker_units", 10), 10)))
        def_units = max(1, min(50, _safe_int(data.get("defender_units", 5), 5)))

        win_prob = win_probability_exact(atk_units, def_units)

        atk_dice = min(3, atk_units - 1)
        def_dice = min(2, def_units)
        atk_exp, def_exp = expected_losses(atk_dice, def_dice)

        roll_probs = {}
        for (ad, dd), outcomes in SINGLE_ROLL_PROBABILITIES.items():
            roll_probs[f"{ad}v{dd}"] = {
                f"atk_loses_{al}_def_loses_{dl}": round(float(p), 4)
                for (al, dl), p in outcomes.items()
            }

        send_json(self, {
            "attacker_units": atk_units,
            "defender_units": def_units,
            "attacker_win_probability": round(win_prob * 100, 2),
            "defender_win_probability": round((1 - win_prob) * 100, 2),
            "current_roll_type": f"{atk_dice}v{def_dice}",
            "expected_attacker_losses_per_roll": atk_exp,
            "expected_defender_losses_per_roll": def_exp,
            "single_roll_probabilities": roll_probs,
        })

    def log_message(self, format, *args):
        pass
