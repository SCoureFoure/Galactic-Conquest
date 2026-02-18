# Balance Tuning Workflow

This project now supports numeric combat tuning without changing base Risk rules.

## Baseline Guarantee

When these values are all zero/default, combat behaves like the existing Risk-based engine:

- `attacker_ability = 0`
- `defender_ability = 0`
- `hero_upgrade_level = 0`
- `planet_upgrade_level = 0`

This preserves early-game baseline odds when nobody has upgraded heroes or planets.

## Tunable Values

The UI and API expose:

- Attacker ability value
- Defender ability value
- Hero upgrade level (default max: 3)
- Planet upgrade level (default max: 3)
- Hero value per upgrade
- Planet value per upgrade

Effective round modifiers are:

- `attacker_total_bonus = attacker_ability + hero_upgrade_level * hero_value_per_upgrade`
- `defender_total_bonus = defender_ability + planet_upgrade_level * planet_value_per_upgrade` (flat mode only)

Planet upgrades now support multiple combat modes:

- `flat_bonus` (default): adds a numeric defender bonus per level (existing behavior).
- `reroll_lowest_defender`: planet upgrade power grants up to 2 rerolls of defender's lowest die each round.
- `suppress_attacker_highest`: planet upgrade power reduces the attacker's highest die by up to 3 each round.

All modes preserve base Risk behavior when `planet_upgrade_level = 0`.

## Endgame Balance Testing

To test parity goals:

1. Start with equal armies and no structures/hero.
2. Set equal hero and planet upgrade levels.
3. Keep `hero_value_per_upgrade` and `planet_value_per_upgrade` equal.
4. Run Monte Carlo simulation and compare win rates.

This gives a quick check that "endgame attacker vs endgame defender" stays near even before introducing extra instant-speed variables.

## Planet Defense Playtest Loop

To compare combat-focused planet upgrades without using damage negation:

1. Fix baseline armies (example: attacker 10, defender 10).
2. Set hero and attacker sliders to your target test profile.
3. Run simulations for each `planet_upgrade_mode` at levels 1, 2, and 3.
4. Capture:
   - Defender win rate
   - Average rounds
   - Average remaining units on win
5. Prefer modes where:
   - Defender win rate scales with level
   - Battles stay decisive (round count does not explode)
   - Endgame parity target remains near 50/50 for equal investment
