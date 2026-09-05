# gs4-wings-compare

Comparing Fizzleworth (Sorcerer) hunt statistics **with** vs **without** the
Energy Wings kit, to decide whether the wings are worth running.

- `variant = wing` — `Fizzleworth-attack-wing.lic` (sorcerer rotation + Energy
  Wings AOE/defensive tap + `Fizzleworth-wingguard.lic` reactive pull).
- `variant = base` — `Fizzleworth-attack-base.lic` (identical sorcerer rotation,
  no wings, wingguard killed).

Plan: 5 hunts each variant, same area/bounty type where possible.

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
| `duration` | bigshot's reported "Last Hunt" time (active hunting, not travel) |
| `kills` | count of undead soul-departures ("rises into the heavens") |
| `deaths` | Fizzleworth deaths ("You are dead!") |
| `attack_passes` | times bigshot invoked the attack script (one decision each) |
| `web_casts` / `maelstrom_casts` / `tether_casts` | `incant 118` / `cast #id` (710) / `incant 706` sent |
| `dmg_dealt` | sum of Maelstrom SMR ticks + ensorcelled-scepter flare + disease/mist DoT on creatures |
| `dmg_taken` | best-effort sum of damage to Fizzleworth (strict incoming attribution) |
| `wounds_taken` | rank-2+ wound messages on Fizzleworth (rib shatter, nerve, etc.) |
| `stun_events` | "You are stunned for N rounds" |
| `fled` | bigshot flee events |
| `bounty_progress` | kill-bounty start -> remaining at hunt end |

**Caveats**: `dmg_dealt` is inflated when mobs escape and get re-hit (the Den of
Rot pestilent visions submerge/resurface constantly). `dmg_taken` is
approximate — GS4 damage flavor text doesn't cleanly distinguish "wound to
right arm" on the player vs on a creature; the parser attributes only damage
that follows an explicit "... at you" style marker. Treat `kills`, `deaths`,
`wounds_taken`, `stun_events`, `fled`, and the cast counts as the hard numbers;
the two damage sums as directional.
