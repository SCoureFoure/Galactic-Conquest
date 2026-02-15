# Combat System Design — Strategic Requirements & Pitfalls

## Purpose

Define a combat system for a territory-control sci-fi strategy game that:

- Resolves battles quickly
- Rewards planning and timing
- Avoids Risk-style stalemates
- Supports heroes, structures, and tactical cards
- Keeps domination as the primary win condition
- Scales for both family play and competitive depth

---

## Core Design Goals

### 1. Decisive but Uncertain Outcomes
Combat should:

- Produce meaningful territorial change
- Not require excessive dice rolling
- Preserve tension and unpredictability
- Avoid deterministic auto-wins

A "typical successful attack" should:

- Capture territory
- Inflict moderate losses
- Create positional advantage
- Enable momentum (cards, production, etc.)

---

### 2. Asymmetry Between Attack and Defense

Clear role separation:

**Attack advantages (mobile):**
- Heroes / command units
- Tactical cards
- Initiative (choosing when to fight)

**Defense advantages (stationary):**
- Planet upgrades
- Terrain effects
- Tie rules
- Prepared positions

Neither side should dominate universally.

---

### 3. Quantity vs Quality Balance

Combat should consider both:

- **Quantity:** Number of units present
- **Quality:** Hero tiers, upgrades, modifiers

Quality should amplify armies — not replace them.

---

### 4. Persistence Across Multiple Rounds

Battles may consist of repeated combat rounds until one side retreats or is destroyed.

Design considerations:

- How many units can be lost per round?
- Can combat stall indefinitely?
- Is retreat possible?
- Are there attrition mechanics?

---

### 5. Integration with the Economy

Combat outcomes should impact:

- Production capacity
- Infrastructure survival
- Resource flow
- Future reinforcement capability

War should target meaningful assets, not just unit stacks.

---

### 6. Incentives for Aggression

Successful combat should yield benefits beyond territory:

- Tactical cards
- Access to key systems (e.g., Core)
- Economic disruption of opponent
- Hero progression (optional)

Passive play should not generate equivalent rewards.

---

### 7. Clarity and Speed

Rules must be easy to execute:

- Minimal arithmetic
- Few conditional steps
- No hidden calculations
- Fast resolution per round

Target: most combats resolved in seconds, not minutes.

---

## Key Mechanic Decisions to Finalize

### A. Dice Model

Options include:

- Classic Risk multi-dice attrition
- Modified multi-dice with upgraded die types
- Single-roll resolution
- Hybrid systems (best die, bonuses, etc.)

Questions to answer:

- Do larger armies roll more dice?
- Do heroes upgrade die size?
- How much randomness is acceptable?

---

### B. Tie Resolution

Default Risk rule: defender wins ties.

Consider whether:

- This applies universally
- It changes with upgrades or terrain
- It should be neutral in some cases

Tie rules strongly influence defensive power.

---

### C. Hero Effects

Heroes may:

- Upgrade one die (e.g., d6 → d8/d10)
- Apply only to attack
- Persist until damage occurs
- Provide special abilities

Key balance concerns:

- Heroes should create breakthroughs
- Not guarantee victory
- Not render units irrelevant

---

### D. Defensive Structures

Planet upgrades may provide:

- Rerolls
- Tie advantages
- Bonus damage
- Damage reduction
- One-time effects

Structures should:

- Strengthen key locations
- Be counterable
- Not create unbreakable fortresses

---

### E. Retreat and Commitment Rules

Decide:

- Can attackers retreat after seeing results?
- Must attackers commit fully?
- Can defenders withdraw?

Retreat rules strongly affect risk tolerance.

---

### F. Infrastructure Interaction

Combat may affect:

- Structures destroyed or disabled
- Production loss
- Economic disruption

Targeting infrastructure should be viable but not game-ending.

---

## Anti-Stalemate Systems

### 1. Momentum Rewards

Players gain advantages from successful aggression:

- Card draws
- Control bonuses
- Access to strategic systems

---

### 2. Core System Incentive

Control of a central objective grants ongoing benefits but is difficult to defend.

Purpose:

- Draw players into conflict
- Prevent static borders
- Provide comeback opportunities

---

### 3. Two-Player Endgame Collapse

When only two players remain, introduce escalating pressure:

Example: Galactic Collapse Track

- Production penalties
- Defense degradation
- Unit attrition
- Final sudden-death condition

Goal: guarantee game termination.

---

## Major Pitfalls to Avoid

### Pitfall 1 — Defensive Turtling

Symptoms:

- Players avoid attacking entirely
- Fortified positions cannot be broken
- Map freezes

Causes:

- Strong tie rules
- Stackable defenses
- Equal reinforcement rates

Mitigation:

- Attack advantages
- Attrition mechanics
- Objectives that reward movement

---

### Pitfall 2 — Attrition Grind

Symptoms:

- Large battles take many rounds
- Minimal territorial change
- Player fatigue

Mitigation:

- Limit units lost per round appropriately
- Provide breakthrough tools (heroes, cards)
- Avoid excessive dice comparisons

---

### Pitfall 3 — Economic Snowball

Symptoms:

- Early winner becomes unstoppable
- Combat becomes cleanup

Mitigation:

- Infrastructure vulnerability
- Diminishing returns
- Multiple attack vectors

---

### Pitfall 4 — Hero Dominance

Symptoms:

- Heroes determine outcomes alone
- Armies become secondary
- Players focus solely on hero survival

Mitigation:

- Limit hero impact per battle
- Allow counters
- Restrict stacking of effects

---

### Pitfall 5 — Infrastructure Sniping

Symptoms:

- Raids cripple players permanently
- Recovery impossible

Mitigation:

- Cheap rebuilding
- Temporary disable instead of destruction
- Protected core assets

---

### Pitfall 6 — Analysis Paralysis

Symptoms:

- Long turns
- Overwhelming decision space

Mitigation:

- Limit actions per turn
- Simplify combat math
- Use intuitive mechanics

---

### Pitfall 7 — Leader Dogpiling

Symptoms:

- All players attack leader
- Second place wins by default

Mitigation:

- Multiple victory paths
- Hard objectives
- Endgame triggers

---

## Desired Play Experience

The combat system should create:

- Tactical decision-making
- Dramatic battles
- Visible momentum swings
- Strategic positioning importance
- A cinematic final showdown

Players should feel:

> "Smart choices and timing win wars — not just luck or waiting."

---

## Next Steps for Playtesting

1. Test combat rules in isolation
2. Simulate equal-strength engagements
3. Evaluate battle duration
4. Observe player willingness to attack
5. Test endgame collapse conditions
6. Adjust numbers before adding advanced systems

---

## Guiding Principle

Combat is the engine of the game.

If combat:

- Is engaging
- Produces change
- Encourages action
- Resolves decisively

Then the rest of the design can succeed.

If combat stagnates, the game will stagnate.
