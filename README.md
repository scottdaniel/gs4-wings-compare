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
  - Den of Rot creatures: **pestilent vision** (non-corporeal undead),
    **magna vereri** (corporeal undead), **Ivasian inciter** and
    **dark-eyed incubus** (both living).
  - **magna vereri** → Web 118 (their attack is a CS beckon, not a caster
    threat; a snare is the useful disable). **Ivasian inciter / dark-eyed
    incubus / pestilent vision** → Corrupt Essence 703 (silence), once/target.
    Unrecognised → Web 118.
  - **pestilent vision** additionally → Symbol of Disruption *aura* (Voln,
    favor) — procs on Fizzleworth's hits against non-corporeal undead (RT +
    AS/DS/CS/TD/UAF penalties, no damage); gswiki recommends it on visions "to
    lower their TD to aid in warding them". Re-armed when it lapses. It *does*
    fire here (~5×/hunt on visions) — see the Disruption note — but the visions
    are already trivial, so the payoff is marginal.
  - **Symbol of Retribution** *aura* (Voln, favor) kept up every pass —
    reactive divine flare back at undead that strike Fizzleworth. **Dead weight
    in Den of Rot** (undead here never land a hit — see the Retribution
    section); set `RETRIBUTION = false`.
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

## Result (base n=5, wing n=8, cat n=3, ultima n=20; usable exp_per_min: base n=3, wing n=6, cat n=3, ultima n=20)

(19 of the 20 `ultima` hunts had Symbol of Retribution up — but the aura never
once fired in this content, so it's not a variable here. See the Retribution
section.)

| | base | wing | cat | ultima |
|---|---|---|---|---|
| deaths | 0 / 5 | 0 / 8 | 0 / 3 | 0 / 20 |
| dmg taken | ~0 (once 40, no cube) | ~0 (four hits: ~29+stun, ~15–30, ~10+2 knockdowns, ~5) | 0 / 3 | ~0 for 19; **63 + rank-2 wound + 5-round stun + knockdown** on one hunt (an inciter thorn during a fizzsac pause) |
| danger events (knockdown + enemy web + wound + stun) / hunt | 1.2 | 0.62 | 0 | 0.25 (2 harmless knockdowns + one 3-effect thorn hit, in 20) |
| exp_per_min | 188, 292, 317 (mean 265) | 268, 268, 245, 205, 153, 150 (mean 215) | 321, 249, 336 (mean 302; all short partials) | 130–314, mean 207, median 204 (n=20) |
| dmg_per_mana | 11.2 | 12.1 | **7.0** | 12.2 |
| sac4mana harvest | 4 / 5 | 1 / 8 (a post-combat tail harvest) | 1 / 3 (fix fired once; twice ran dry first) | 14 / 20 (inline top-off, reliable once dialed in) |

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

**ultima (experimental, n=20):** `base`'s Web/Maelstrom/Tether spine kept, but
the opener is creature-specific (Web on vereri, Corrupt Essence 703 on the
casters), plus two Voln self-auras (Symbol of Disruption + Symbol of
Retribution — both near-worthless in this content, see the notes below) and a
one-shot `;reanim` buddy off the first inciter. Hypothesis: same
leveling speed as `base` with fewer danger events, paid in Voln favor instead
of silver.

**The hypothesis holds on defense; on speed the metric is too noisy to call.**
exp_per_min ranges 130–314, mean **207**, median 204 (n=20). That's below
base's 265, but base's mean rests on n=3 (two of which were partial-mind starts
that read high) and `exp_per_min` is dominated by how full mind is at the start
and stop of a hunt, not by the rotation — the low ultima readings (130–166) are
all slow inciter-heavy pulls, the mid ones (195–235) are ordinary
partial-start → fried hunts. Need a matched-start base sample to compare
properly. `dmg_per_mana` 12.2, same as base/wing and ~1.7× cat. **Defense: 19
of 20 hunts took 0 damage** (vs base 1.2 danger/hunt). The two knockdowns on
those (hunts 12, 19) were a 5-second roundtime and nothing else. The 20th hunt
took the dataset's worst hit — an inciter thorn maneuver for ~63 + a rank-2
wound + a 5-round stun + a knockdown — but that landed while bigshot was paused
for a fizzsac harvest and the character had been wandered into a fresh room
mid-cast, i.e. the rotation wasn't defending. sac4mana harvested on **14 of
20** — once the inline `sacrifice mana` top-off (`mana < 45`) was dialed in it
fires mid-hunt almost every hunt (~90 mana each), so ultima has none of the
mana starvation that killed cat.

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
mana.** The two Voln auras it carries are both near-worthless in Den of Rot,
though: Retribution never fires, Disruption fires but changes nothing
measurable (see the two notes below). Run `ultima` here with `RETRIBUTION =
false` and Disruption optional — the rotation itself is the value, not the
symbols.

### Symbol of Retribution: it does nothing in this content — turn it off

`RETRIBUTION = true` (default) vs `false` in `Fizzleworth-attack-ultima.lic`.
Per [gswiki](https://gswiki.play.net/Symbol_of_Retribution), the self-cast aura
"reactively flares with divine retribution at **undead who manage to strike the
player**" — flare message `** Your aura unleashes a blast of divine retribution
at the <undead>! **`. Undead only; reactive only; no damage block, no maneuver
defense.

**Across all 19 RETRIBUTION-on hunts the aura flared exactly 0 times.**
`grep "aura unleashes a blast of divine retribution"` over every log: no hits.
The Den of Rot undead are pestilent visions and magna vereri (inciters and
incubi are living, so Retribution never applies to them). Neither undead ever
landed a hit on Fizzleworth: every vision "vile energies" gaze and every vereri
"beckon" in the 09.09/09.10 marathons was warded off (his TD ~385 vs their CS
~315; vereri beckons 16/16 warded). So Retribution had nothing to react to.

**Earlier draft of this section was wrong.** It credited Retribution with "11
flares, 751 dmg, ~7% of output (51/54/92/90/73/64/58/53/82/54/80)". Those are
the **faewood scepter's holy-fire flare** (`Your faewood scepter bursts alight
with leaping tongues of holy fire! → Consumed by the hallowed flames, a
<creature> is ravaged for N`) — an *offensive* weapon flare on Fizzleworth's
own hits, already inside `dmg_dealt`. Unrelated to Symbol of Retribution.

**Verdict: `RETRIBUTION = false`.** It can't help here — the undead never land
a hit — so the favor it costs (part of the ~2,000/hunt symbol batch) is pure
waste. No on/off exp comparison needed; there's nothing to compare. Keep it
only if you take `ultima` somewhere with undead that actually connect.

The 09.10 - 3 hunt below is nominally the first "off" hunt but tells us nothing
about Retribution — the hard hit on it came from an Ivasian *inciter* (living,
not undead), which Retribution would never touch on or off.

### Symbol of Disruption: it fires, but the payoff is thin

Per [gswiki](https://gswiki.play.net/Symbol_of_Disruption): procs on the
caster's hits against **non-corporeal undead**, hitting them with roundtime +
AS/DS/CS/TD/UAF/UDF/Mana-Control penalties (no direct damage). Proc line:
`The <undead> writhes as its spectral form bends and warps uncontrollably!` →
`It's like fighting fog!`.

Unlike Retribution, **this one works** — it procs **~5×/hunt**, always on
pestilent visions (magna vereri are corporeal undead, so they never get it;
97/97 procs in the marathons were "vision"). But its stated job — lower vision
TD so Fizzleworth wards them — is nearly moot here: against visions his warding
already succeeds **~93%** (CS ~390 vs TD ~260–315), disrupted or not (32/34
land after a recent proc, 61/66 without). The ~7% ward failures it might turn
around are worth ~0.3 casts/hunt. The visions also die in 1–2 Maelstrom hits +
the disease DoT and land nothing on Fizzleworth regardless.

So Disruption is doing *something* real, but nothing that moves `exp_per_min`,
`kills_per_min`, or defense in this content. If favor is tight, it's a
reasonable cut too; if you keep one Voln aura for `ultima` here, keep this one
over Retribution (at least it fires). The real value would show up against
non-corporeal undead with TD high enough to actually resist him.

**ultima row set** (20 hunts, 19 with the aura up + 1 without — the aura never
fired either way, see above): `exp_per_min` mean 207, median 204 (130–314),
`kills_per_min` mean 4.6, `dmg_per_mana` mean 12.2, 0 damage taken except the
one inciter thorn hit. Hunts 6–13 are the 09.09 - 9 marathon, 14–19 the
09.10 - 2 marathon, 20 the 09.10 - 3 hunt (all had a couple of unrepresentative
hunts — a fizzsac Pain-grind, a slow double-reanim — left out).

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
| `disruption_casts` / `retribution_casts` | `ultima` only — `symbol of disruption` / `symbol of retribution` sends (Voln self-auras, favor not mana; each covers rank×10s so counts are low). 0 for base/wing/cat. These count *casts*, not effect: Retribution never once flared in this content and Disruption's proc isn't tracked as a column (it fires ~5×/hunt on visions — see the aura notes). |
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
