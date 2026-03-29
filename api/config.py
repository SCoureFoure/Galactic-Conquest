from http.server import BaseHTTPRequestHandler
from _shared import (
    attacker_slider_specs,
    defender_slider_specs,
    planet_upgrade_mode_specs,
    structures_config,
    send_json,
    DEFAULT_COMBAT_TUNING,
)
from engine.heroes import HERO_TIERS


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        send_json(self, {
            "hero_tiers": HERO_TIERS,
            "structures": structures_config(),
            "attacker_sliders": attacker_slider_specs(),
            "defender_sliders": defender_slider_specs(),
            "planet_upgrade_modes": planet_upgrade_mode_specs(),
            "default_planet_upgrade_mode": DEFAULT_COMBAT_TUNING.planet_upgrade_mode,
        })

    def log_message(self, format, *args):
        pass
