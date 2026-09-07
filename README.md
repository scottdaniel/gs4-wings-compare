# gs4-wings-compare

Comparing Fizzleworth (Sorcerer) hunt statistics **with** vs **without** the
Energy Wings kit, to decide whether the wings are worth running.

- `variant = base` — `Fizzleworth-attack-base.lic` — Web 118 → Energy Maelstrom
  710 → Tenebrous Tether 706. No wings.
- `variant = wing` — `Fizzleworth-attack-wing.lic` — the base rotation plus the
  Energy Wings kit (AOE / defensive tap) and `Fizzleworth-wingguard.lic`
  (reactive Prismatic Aegis / Crawling Shadow on enemy prep).
- `variant = cat` — `Fizzleworth-attack-cat.lic` — completely different, no
  wings. Casters (vision / vereri / incubus): Corrupt Essence 703 (silence,
  once/target) → Dark Catalyst 719 (CS-vs-TD insta-kill attempt, refunds 1–14
  mana). Ivasian inciters (Dark Catalyst can't one-shot them): `;reanim` the
  first (Pain 711 to death, then Animate Dead 730 the corpse into a buddy),
  then Pain 711 the rest to death (each cast = 20–35% max HP + 3–7s roundtime
  lockout). Grasp of the Grave 709 (area knockdown) when ≥2 in the room.
  Flee at 4. Experimental.

Plan: 5 hunts each variant, same area/bounty type where possible.

Primary metric: **`exp_per_min`** = `(end_mind − start_mind) / duration_min`
(field exp the hunt earned, per minute of hunt) — leveling speed. `duration`
is bigshot's "Last Hunt" (excludes sac4mana harvest time); `end_mind` is a
decayed reading so "fried" hunts underestimate a little.

## Result (base n=5, wing n=6; usable exp_per_min: base n=3, wing n=3-4)

| | base | wing |
|---|---|---|
| deaths | 0 / 5 | 0 / 6 |
| dmg taken | ~0 (once 40, no cube) | ~0 (once ~15–30, once ~5) |
| knockdowns+webs / hunt | ~0.6 | ~0.2 |
| exp_per_min | 188, 292, 317 (mean ~265) | 268, 268, 244 (mean ~260; + a 150 outlier on a barely-rested 1m47s hunt) |
| sac4mana mana harvest | usual | **0 of 6** |

**Defense — clear:** across 11 hunts this content never threatened
Fizzleworth. 0 deaths, ~0 damage, with or without wings *and* with or without
the moonstone cube. The wings' whole reason to exist doesn't show up here.

**exp_per_min — no detectable difference, and not enough data to claim one.**
Base and wing central tendency are ~the same (~260), but base's three points
range 188→317 — huge hunt-to-hunt variance (mob escapes, knockdown lockouts,
ward RNG). n≈3 per side has no power to detect a wing effect against that
noise. Earlier drafts of this README overstated it as "not significant" — more
honestly: **underpowered; no difference visible.**

**One real (minor) cost:** every wing hunt failed to get a sac4mana mana
harvest — the wing verbs keep the attack script continuously busy so
sac4mana's "don't harvest mid-fight" guard never opens. 3 of 6 wing hunts
ended out of mana.

Verdict: the wings buy **nothing measurable** for this content — no survival
benefit (nothing was killing him anyway) and no clear exp/min gain. Not worth
40M here. Selling.

## Cost context

Energy Wings run **~40,000,000 silver**. A moonstone cube (spell 1705,
Martial Prowess — additive SMR / maneuver defense, one rub ≈ one hunt) is
**~850 silver**. So ~47,000 cubes buy what the wings cost — on the order of a
year of nonstop hunting.

The two overlap on one thing: extra maneuver defense (the wings' Luminous
Flight evade bonus / reactive Prismatic Aegis vs the cube's SMR bonus). On
that axis alone the cube wins on cost by ~4 orders of magnitude, and the base
hunts show Fizzleworth survives maneuvers fine with *or* without either
(H1 = no cube, still 0 deaths).

So the question this data has to answer is whether the wings earn 40M with the
things the cube can't do:

- **Swarm clear** — Blinding Reprisal / Blast of Brilliance hitting 5–10
  targets at once (would show up as higher `kills`, shorter `duration`).
- **Reactive shield with no consumable** — Prismatic Aegis on enemy prep,
  no cube charge spent.
- **Group utility** — Wings of Warding's party DS/TD buff.
- **Zero upkeep / permanence** — never buy or rub anything.

If the `wing` rows don't move `kills`, `duration`, or `dmg_per_mana`
meaningfully above the cube-only `base` baseline (H2–H5), the 40M is buying
convenience and a marginal maneuver save.

## Files

- `hunts.csv` — one row per hunt. Append as logs come in.
- `parse_hunt.py` — extracts a row from a Saga log window:
  ```
  python3 parse_hunt.py <logfile> <start_line> <end_line> <date> <variant> <area> <hunt_type> <duration>
  ```
  Pick `<start_line>`/`<end_line>` around the combat stretch (first
  `Bigshot hunting` / first `Fizzleworth-attack-* active` to just past the last
  `Fizzleworth-attack-* has exited`). `<duration>` is bigshot's own
  "Last Hunt" figure.

## Column notes

| column | meaning |
|---|---|
| `martial_prowess` | was the moonstone cube (spell 1705, extra SMR / maneuver defense) rubbed and active for this hunt. **Confound** — H1 ran without it, H2 onward with it. Auto-detected from a pre-window "rub a solid moonstone cube". Keep it consistent across whatever you're comparing. |
| `start_mind` / `end_mind` / `mind_gained` | field exp (`Field Exp: N/~1210`) at hunt start (from prep's `exp`, older logs use the last rest reading) and at the first rest reading after; `mind_gained` = end − start = the field exp the hunt actually cost. `end_mind` is a decayed lower bound (bigshot reads `exp` a bit into the rest), so `mind_gained` is a slight underestimate. |
| `duration` / `duration_min` | bigshot's reported "Last Hunt" time (active hunting, not travel) |
| `kills_per_min` | `kills / duration_min` |
| `exp_per_min` | `mind_gained / duration_min` — **the primary metric**: field exp earned per minute of hunt (leveling speed). |
| `kills_per_100mind` | `kills / mind_gained × 100` — kept for reference. |
| `kills` | undead soul-departures ("rises into the heavens") + non-undead corpses bigshot looted ("You search the &lt;creature&gt;") |
| `deaths` | Fizzleworth deaths ("You are dead!") |
| `attack_passes` | times bigshot invoked the attack script (one decision each) |
| `web_casts` / `maelstrom_casts` / `tether_casts` / `pain_casts` | `incant 118` / `prep 710` / `incant\|prep 706` / `prep\|prepare 711` command sends, from **any** script in the window (attack-* and fizzsac) |
| `corrupt_casts` / `grasp_casts` / `catalyst_casts` | `cat` variant only — `incant 703` / `709` / `719` sends. 0 for base/wing. (Inciter Pain 711 lands in `pain_casts`.) |
| `reanim_runs` / `animate_casts` | `cat` variant — times `;reanim` ran / an Animate Dead corpse-raise landed. |
| `symbol_mana_casts` | `symbol of mana` sends (bigshot casts it; the game logs no mana amount) |
| `mana_out` | confirmed casts only, priced at targeted cost (Web 5, Maelstrom 10, Tether 6, Pain 11) |
| `mana_in` | "N mana surge into you" (sac4mana's `sacrifice mana`) + 50 per `symbol_mana_casts` (Symbol of Mana is a flat 50-point refill, unlogged). Excludes natural regen. |
| `dmg_dealt` | Maelstrom SMR ticks + ensorcelled-scepter flare + disease/mist DoT + fizzsac Pain, on creatures |
| `dmg_taken` | best-effort sum of damage to Fizzleworth (only damage right after an explicit "...at you" marker) |
| `dmg_per_mana` | `dmg_dealt / mana_out` — the mana-efficiency number |
| `wounds_taken` | rank-2+ wound messages on Fizzleworth (rib shatter, nerve, etc.) |
| `stun_events` | "You are stunned for N rounds" |
| `knockdowns` | SMR-maneuver knockdowns on Fizzleworth ("acute sense of vulnerability", ~10s roundtime each). Sorcerers defend maneuvers badly and CS/bolt spells well, so this is the real incoming-danger signal — not `dmg_taken`. |
| `webbed_by_enemy` | times a creature's Web maneuver ensnared Fizzleworth ("You become ensnared in thick strands of webbing"). Immobilize, no damage. |
| `fled` | bigshot flee events |
| `wing_tap` / `wing_knock` / `wing_fold` / `wing_push` / `wing_aegis` | Energy Wings verbs fired (command sends): Luminous Flight (evade buff) / Blast of Brilliance (≤5-target AOE) / Blinding Reprisal (≤10-target AOE) / Wings of Warding (group DS/TD buff) / Prismatic Aegis (reactive shield, from `Fizzleworth-wingguard` on an enemy prep). All 0 for `variant = base`. |
| `bounty_progress` | kill-bounty start -> remaining at hunt end (target creature only, so ≤ `kills`) |

**Caveats**: `dmg_dealt` is inflated when mobs escape and get re-hit (the Den of
Rot pestilent visions / incubi submerge and resurface constantly). `dmg_taken`
is approximate — GS4 damage flavor text doesn't cleanly distinguish "wound to
right arm" on the player vs on a creature. The parser only books damage as
taken when it directly follows a confirmed-contact marker ("...hits for N",
"jabs into you", "jolts your whole body", etc.), and it clears the "incoming"
context the moment a whiff shows up ("A clean miss", "Warded off", "dissipates
upon impact", "you are unaffected", "you evade", …) so a Maelstrom DoT tick
that interleaves right after a missed enemy attack isn't misattributed. Treat
`kills`, `deaths`, `wounds_taken`, `stun_events`, `knockdowns`,
`webbed_by_enemy`, `fled`, and the cast counts as the hard numbers; the damage
sums (and `dmg_per_mana`) as directional.
