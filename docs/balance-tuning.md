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
- `defender_total_bonus = defender_ability + planet_upgrade_level * planet_value_per_upgrade`

Dice are still rolled normally and defender still wins ties. The totals above are added during each dice comparison.

## Endgame Balance Testing

To test parity goals:

1. Start with equal armies and no structures/hero.
2. Set equal hero and planet upgrade levels.
3. Keep `hero_value_per_upgrade` and `planet_value_per_upgrade` equal.
4. Run Monte Carlo simulation and compare win rates.

This gives a quick check that "endgame attacker vs endgame defender" stays near even before introducing extra instant-speed variables.
