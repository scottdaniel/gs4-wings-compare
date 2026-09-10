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
- `variant = ultima` — `Fizzleworth-attack-ultima.lic` — `base`'s 710 → 706 →
  hold-DoT finish, but a creature-specific opener plus two Voln self-auras and
  a one-shot animate buddy. No wings.
  - **magna vereri** → Web 118 (they don't cast; a snare is the useful
    disable). **Ivasian inciter / dark-eyed incubus / pestilent vision** →
    Corrupt Essence 703 (all three cast; silence beats a web), once/target.
    Unrecognised → Web 118.
  - **pestilent vision** additionally → Symbol of Disruption *aura* (Voln,
    favor) — one cast covers every noncorporeal undead struck for rank×10s;
    gswiki recommends it on visions "to lower their TD to aid in warding
    them". Re-armed when it lapses, not per-creature.
  - **Symbol of Retribution** *aura* (Voln, favor) kept up every pass —
    reactive divine flare back at undead that strike Fizzleworth. Pure
    defence. `RETRIBUTION` knob to disable.
  - **One-shot buddy**: first inciter of the hunt with no animate up →
    `;reanim` (Pain 711 to death + Animate Dead 730). Just once per hunt
    (`$ult_reanim_done`, cleared by `;reanim die` and by `Fizzleworth-prep`);
    later inciters get the normal 703 → 710 → 706. Middle ground between
    `base` (no buddy) and `cat` (re-reanims on every buddy death).
  Experimental.

The `cat` / `ultima` animate buddy is dismissed in the field at end of hunt by
`Fizzleworth-anim-cleanup.lic` (weapon back to verlok → `tell anim die` →
`;eloot` the remains), with `Fizzleworth-prerest`'s `;reanim die` as a
town-side fallback — so no animated corpse (or its weapon / loot) is dragged
home.

Plan: 5 hunts each variant, same area/bounty type where possible.

Primary metric: **`exp_per_min`** = `(end_mind − start_mind) / duration_min`
(field exp the hunt earned, per minute of hunt) — leveling speed. `duration`
is bigshot's "Last Hunt" (excludes sac4mana harvest time); `end_mind` is a
decayed reading so "fried" hunts underestimate a little.

## Result (base n=5, wing n=8, cat n=3, ultima n=19 RETR-on + 1 RETR-off; usable exp_per_min: base n=3, wing n=6, cat n=3, ultima n=20)

`ultima` column = the 19 RETRIBUTION-on hunts. The one RETR-off hunt so far is
called out separately (it was disrupted by a fizzsac pause, not a fair sample).

| | base | wing | cat | ultima |
|---|---|---|---|---|
| deaths | 0 / 5 | 0 / 8 | 0 / 3 | 0 / 20 |
| dmg taken | ~0 (once 40, no cube) | ~0 (four hits: ~29+stun, ~15–30, ~10+2 knockdowns, ~5) | 0 / 3 | 0 / 19 on; **63 + rank-2 wound + 5-round stun + knockdown** on the 1 RETR-off hunt (during a fizzsac pause) |
| danger events (knockdown + enemy web + wound + stun) / hunt | 1.2 | 0.62 | 0 | 0.10 on (2 harmless knockdowns in 19); the RETR-off hunt had a wound + stun + knockdown in one hit |
| exp_per_min | 188, 292, 317 (mean 265) | 268, 268, 245, 205, 153, 150 (mean 215) | 321, 249, 336 (mean 302; all short partials) | 130–314, mean 207, median 204 (n=19 on; RETR-off hunt 203) |
| dmg_per_mana | 11.2 | 12.1 | **7.0** | 12.2 |
| sac4mana harvest | 4 / 5 | 1 / 8 (a post-combat tail harvest) | 1 / 3 (fix fired once; twice ran dry first) | 14 / 19 (inline top-off, reliable once dialed in) |

**Defense — clear:** across 36 hunts, 0 deaths, and only twice did anything
land hard. Incoming damage is otherwise near-zero, with or without wings *and*
with or without the moonstone cube. The two real hits: incubus field effects
(icy stalagmites / "column of frigid air") on wing hunts 6–7 for ~15–30 and a
short stun; and one inciter thorn maneuver on the RETR-off hunt for ~63 + a
rank-2 wound + a 5-round stun + a knockdown — but that one landed while bigshot
was paused for a fizzsac harvest and the character was wandered into a fresh
room mid-cast, i.e. the rotation wasn't defending. Nothing the wings would have
stopped. The wings' whole reason to exist still doesn't show up here.

**exp_per_min — no wing benefit visible; if anything wing trends lower, but
it's confounded.** base 265 vs wing 215 vs cat 285 — but the two lowest wing
points (153, 205) are a heavily-decayed `end_mind` reading and a barely-rested
partial start, not real slowdowns, and base's three points still range 188→317
on their own. Huge hunt-to-hunt variance (mob escapes, knockdown lockouts, ward
RNG), n≈3–6 per variant: **underpowered; no wing gain, and no clean case that
wings cost exp either.**

**One real (minor) cost:** the wing verbs keep the attack script continuously
busy, so sac4mana's "don't harvest mid-fight" guard almost never opens *during*
combat. Only 1 of 8 wing hunts landed a harvest, and that one was a post-combat
tail harvest (mana still low, quiet room after the last kill) — the same kind
base gets. Most wing hunts ended fried or out of mana with no quiet tail, so
the harvest never fired.

Verdict: the wings buy **nothing measurable** for this content — no survival
benefit (nothing was killing him anyway) and no clear exp/min gain. Not worth
40M here. Selling.

**cat (experimental, n=3) — done, not viable here.** A completely different
rotation, no wings. `dmg_per_mana` ~7, far the worst of any variant (Pain
lockouts + Dark Catalyst are mana-hungry), and it can't sustain a hunt: all
three cat runs ended out of mana in **under 3 minutes** (2:05, 2:53, 1:48).
The `-cat` inline `sacrifice mana` fix (fires at mana < 45) helped once — cat
hunt 2 got an 89-mana harvest and lasted 2:53 — but cat hunts 1 and 3 hit
empty before the guard opened at all. The high `exp_per_min` numbers (321,
249, 336) are all near-empty-start partials, so the per-minute rate is
inflated by the front-loaded absorption curve, not a real speed advantage.
Not worth pursuing for this content.

**ultima (experimental, n=19, all RETRIBUTION on):** `base`'s Web/Maelstrom/
Tether spine kept, but the opener is creature-specific (Web on vereri, Corrupt
Essence 703 on the casters), plus two Voln self-auras (Symbol of Disruption on
visions to drop their TD, Symbol of Retribution always-on for the reactive
undead flare) and a one-shot `;reanim` buddy off the first inciter. Hypothesis:
same leveling speed as `base` with fewer danger events, paid in Voln favor
instead of silver.

**The hypothesis holds on defense; on speed the metric is too noisy to call.**
exp_per_min ranges 130–314, mean **207**, median 204 (n=19). That's below
base's 265, but base's mean rests on n=3 (two of which were partial-mind starts
that read high) and `exp_per_min` is dominated by how full mind is at the start
and stop of a hunt, not by the rotation — the low ultima readings (130–166) are
all slow inciter-heavy pulls, the mid ones (195–235) are ordinary
partial-start → fried hunts. Need a matched-start base sample to compare
properly. `dmg_per_mana` 12.2, same as base/wing and ~1.7× cat. **0 damage
taken across all 19 hunts, two knockdowns** (vs base 1.2 danger/hunt) — the
"fewer maneuvers land" claim is now on solid n. Both knockdowns (hunts 12 and
19) were a 5-second roundtime and nothing else — no wound, stun, or damage.
sac4mana harvested on **14 of 19** — once the inline `sacrifice mana` top-off
(`mana < 45`) was dialed in it fires mid-hunt almost every hunt (~90 mana
each), so ultima has none of the mana starvation that killed cat.

Data note: four ultima hunts (3, 7, 10, 18) turned a bounty in right after the
hunt, which dumps ~450 field exp into the pool before bigshot reads `exp` —
their `end_mind` was reading 1641–1709 and inflating `exp_per_min` to 260–321.
`parse_hunt.py` now stops the `end_mind` scan at a bounty turn-in and clamps a
post-bounty reading to the cap; those four now read ~158–198.

Rough edges: an early hunt (09.08 #2) died to `encumbered` at 1m45s (loot
weight, not danger). `reanim_runs` counts the end-of-hunt `;reanim die` cleanup
as a run. `dmg_taken` on the buddy hunts (once 28, 89, 66, 55) was always the
reanim buddy's thorn AoE landing on a creature, not incoming — `parse_hunt.py`
tracks a `buddy` context (`An animated <creature>` attack lines + non-player
thorn lines) that books that damage as neither taken nor dealt; every ultima
hunt now reads 0 taken, matching its 0 wounds/stun.
Verdict: **ultima works — matches base speed, quieter, self-sufficient on
mana.** Cost is Voln favor for the auras.

### Symbol of Retribution: is it earning its favor?

`RETRIBUTION = true` (default) vs `false` in `Fizzleworth-attack-ultima.lic`.
Retribution is a self-aura that flares divine damage back at undead that
*strike* Fizzleworth — reactive only, no damage block, no maneuver defense.

**Favor** comes only from releasing undead (`ceil(level/15 × creatureLevel)`
each) or, for Voln Masters, the Master's-Hall globe (~500 favor / deed). No
prayer refill, no decay (gswiki: Favor). Whole-session favor from the 09.09
run: **824,680 → ~821,891 over 5 hunts ≈ −450/hunt**. Per hunt: ~2,000–2,400
spent on symbols (a ~−1,550 batch of courage/protection/supremacy + Retribution
+ Disruption, plus ~−500–950 in mid-hunt aura recasts on longer hunts) against
~1,900 back from ~6 vision releases at ~320 each. The 822k pool ÷ 450 ≈ ~1,800
hunts of runway, so it drains slowly but only undead kills refill it.

**Retribution's damage share (09.09, RETRIBUTION on):** 11 flares over ~5.5
hunts — 51/54/92/90/73/64/58/53/82/54/80, **751 total, ~68 avg, ~1–3
flares/hunt**.

| hunt | Retribution dmg | total outgoing | share |
|---|---|---|---|
| 1 | 236 (3 flares) | ~1,876 | ~13% |
| 2 | 137 (2 flares) | ~2,443 | ~6% |
| 3 | 58 (1 flare)   | ~2,327 | ~2.5% |

~7% of output on average, highly variable (depends on how often a creature
lands a hit — rare here, since 703 silences the casters). Buys **no
survivability**.

**The test:** collect `exp_per_min` / `kills_per_min` / `dmg_per_mana` and the
per-hunt favor delta with Retribution on (09.09 night) vs off (next night). If
losing ~7% of damage doesn't slow the hunts, `RETRIBUTION = false` saves
~300–600 favor/hunt for free.

**On-arm baseline** (19 `ultima` rows, RETRIBUTION on): `exp_per_min` mean
207, median 204 (130–314), `kills_per_min` mean 4.6, `dmg_per_mana` mean 12.2,
0 damage taken, 2 harmless knockdowns in 19.

**Off-arm, hunt 1** (RETRIBUTION off, 09.10 - 3): `exp_per_min` 203, 17 kills /
4m40s — right in the on-arm range. But it also carries the worst hit in the
dataset: an inciter thorn maneuver for ~63 + a rank-2 sternum wound + a 5-round
stun + a knockdown, which ended the hunt. **RETRIBUTION off did not cause it** —
that's a maneuver, and Retribution only flares at attacks that land; the
exposure was a fizzsac harvest pause that wandered Fizzleworth into a fresh room
mid-cast. Doesn't count as a real off-arm sample. Off-arm still effectively
n=0. Hunts 6–13 are the 09.09 - 9 marathon,
14–19 the 09.10 - 2 marathon (both had a couple of unrepresentative hunts —
a fizzsac Pain-grind, a slow double-reanim — left out). Off-arm still TODO.

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
  "Last Hunt" figure. The parser strips a leading `[HH:MM:SS] ` client
  timestamp from every line, so timestamped and untimestamped logs both work.

## Column notes

| column | meaning |
|---|---|
| `martial_prowess` | was the moonstone cube (spell 1705, extra SMR / maneuver defense) rubbed and active for this hunt. **Confound** — H1 ran without it, H2 onward with it. Auto-detected from a pre-window "rub a solid moonstone cube". Keep it consistent across whatever you're comparing. |
| `start_mind` / `end_mind` / `mind_gained` | field exp (`Field Exp: N/~1210`) at hunt start (from prep's `exp`, older logs use the last rest reading) and at the first rest reading after; `mind_gained` = end − start = the field exp the hunt actually cost. `end_mind` is a decayed lower bound (bigshot reads `exp` a bit into the rest), so `mind_gained` is a slight underestimate. The `end_mind` scan stops at a bounty turn-in (`earned N bounty points, M experience`) — that dumps ~450 field exp into the pool, so a post-bounty reading isn't what the hunt earned; a reading above the cap is clamped to it, and a fried hunt whose only reading is post-bounty gets `end_mind` = cap. |
| `duration` / `duration_min` | bigshot's reported "Last Hunt" time (active hunting, not travel) |
| `kills_per_min` | `kills / duration_min` |
| `exp_per_min` | `mind_gained / duration_min` — **the primary metric**: field exp earned per minute of hunt (leveling speed). |
| `kills_per_100mind` | `kills / mind_gained × 100` — kept for reference. |
| `kills` | undead soul-departures ("rises into the heavens") + non-undead corpses bigshot looted ("You search the &lt;creature&gt;") |
| `deaths` | Fizzleworth deaths ("You are dead!") |
| `attack_passes` | times bigshot invoked the attack script (one decision each) |
| `web_casts` / `maelstrom_casts` / `tether_casts` / `pain_casts` | `incant 118` / `prep 710` / `incant\|prep 706` / `prep\|prepare 711` command sends, from **any** script in the window (attack-* and fizzsac) |
| `corrupt_casts` / `grasp_casts` / `catalyst_casts` | `incant 703` / `709` / `719` sends. `corrupt_casts` fires for both `cat` and `ultima`; `grasp`/`catalyst` are `cat` only. 0 for base/wing. (Inciter Pain 711 lands in `pain_casts`.) |
| `reanim_runs` / `animate_casts` | `cat` / `ultima` — times `;reanim` ran / an Animate Dead corpse-raise landed. `ultima` caps `reanim_runs` at 1 per hunt by design. |
| `disruption_casts` / `retribution_casts` | `ultima` only — `symbol of disruption` / `symbol of retribution` sends (Voln self-auras, favor not mana; each covers rank×10s so counts are low). 0 for base/wing/cat. |
| `symbol_mana_casts` | `symbol of mana` sends (bigshot casts it; the game logs no mana amount) |
| `mana_out` | confirmed casts only, priced at targeted cost (Web 5, Maelstrom 10, Tether 6, Pain 11) |
| `mana_in` | "N mana surge into you" (sac4mana's `sacrifice mana`) + 50 per `symbol_mana_casts` (Symbol of Mana is a flat 50-point refill, unlogged). Excludes natural regen. |
| `dmg_dealt` | Maelstrom SMR ticks + ensorcelled-scepter flare + disease/mist DoT + fizzsac Pain, on creatures |
| `dmg_taken` | best-effort sum of damage to Fizzleworth (only damage right after an explicit "...at you" marker; the reanim buddy's attacks on creatures are excluded) |
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
taken when it directly follows a player-directed contact marker ("...hits for
N" while in an incoming context, "jabs into you", "jolts your whole body",
etc.), it clears the "incoming" context the moment a whiff shows up ("A clean
miss", "Warded off", "dissipates upon impact", "you are unaffected", "you
evade", …), and it tracks a separate `buddy` context for the `cat` / `ultima`
reanim buddy (`An animated <creature>` attack lines + thorn maneuvers aimed at
a creature) so the buddy's own damage lands in neither `dmg_taken` nor
`dmg_dealt`. Treat
`kills`, `deaths`, `wounds_taken`, `stun_events`, `knockdowns`,
`webbed_by_enemy`, `fled`, and the cast counts as the hard numbers; the damage
sums (and `dmg_per_mana`) as directional.
