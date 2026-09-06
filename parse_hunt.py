#!/usr/bin/env python3
"""Parse a Saga/GS4 combat-log window and emit one CSV row of hunt stats.

Usage: parse_hunt.py <logfile> <start> <end> <date> <variant> <area> <hunt_type> <duration>

<start>/<end> bracket the combat stretch: from the first "Bigshot hunting" /
first "Fizzleworth-attack-* active" to just past the last
"Fizzleworth-attack-* has exited" (before the rest/travel-out).
<duration> is bigshot's own "Last Hunt" figure.

`martial_prowess` (moonstone cube / spell 1705, extra SMR/maneuver defense) is
auto-detected: yes if a "moonstone cube ... disintegrates" rub happened in the
~2500 lines before the window and 1705 wasn't seen to fade before it starts.
It's an experimental confound -- H1 ran without it, H2-H5 with -- so keep it
consistent across the variant you're comparing.
"""
import re, sys

logfile, start, end, date, variant, area, hunt_type, duration = (
    sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])

with open(logfile, encoding="utf-8", errors="replace") as fh:
    all_lines = fh.readlines()
win = all_lines[start-1:end]
txt = "".join(win)

def hms_to_min(s):
    m = re.match(r"(?:(\d+)m)?\s*(?:(\d+)s)?", s.strip())
    return round(int(m.group(1) or 0) + int(m.group(2) or 0) / 60, 2) if m else 0

dur_min = hms_to_min(duration)

# Mind saturation is "Field Exp: N/1220". bigshot only reads it (via `exp`)
# while resting, so we can usually get the value going INTO the hunt (last
# reading before the window) but rarely the peak at the end. Start it from
# empty for a clean comparison -- otherwise this records where it actually was.
_pre = "".join(all_lines[:start-1])
_sm = re.findall(r"Field Exp: ([\d,]+)/1,?220", _pre)
start_mind = _sm[-1].replace(",", "") if _sm else "?"

# moonstone cube (Martial Prowess / 1705): a single-use rub, lasts ~1 hunt.
# Active for this hunt if it was rubbed in the run-up (last ~2500 lines before
# the window) and not also rubbed again inside the window (that'd be the NEXT
# hunt's prep bleeding in).
pre = "".join(all_lines[max(0, start-1-2500):start-1])
martial_prowess = "yes" if ("You rub a solid moonstone cube" in pre
                            and "You rub a solid moonstone cube" not in txt) else "no"

# ---------------------------------------------------------------- spell costs
# Targeted casts, from GS4 spell data (see Fizzleworth-attack-wing.lic header).
COST = {"web": 5, "maelstrom": 10, "tether": 6, "pain": 11,
        "corrupt": 3, "grasp": 9, "catalyst": 19}

# ---------------------------------------------------------------- kills
# Undead (pestilent vision) release a soul; everything else bigshot loots as a
# corpse ("You search the <creature>"). Visions dissolve before they can be
# looted, so the two signals don't overlap.
kills = (txt.count("rises into the heavens")
         + len(re.findall(r"^You search the (?!.*\bvision\b).+\.$", txt, re.M)))
deaths = len(re.findall(r"^\s*You are dead!", txt, re.M))

# ---------------------------------------------------------------- spell counts
# Command sends (what got attempted), across every script casting during the
# hunt -- Fizzleworth-attack-* AND fizzsac (the sac4mana harvest helper).
web_casts    = len(re.findall(r"\]>incant 118\b", txt))
mael_casts   = len(re.findall(r"\]>prep 710\b", txt))
tether_casts = len(re.findall(r"\]>(?:incant|prep|prepare) 706\b", txt))
pain_casts   = len(re.findall(r"\]>(?:incant|prep|prepare) 711\b", txt))
sym_mana_casts = len(re.findall(r"\]>symbol of mana\b", txt))
# Fizzleworth-attack-cat variant: Corrupt Essence / Grasp of the Grave / Dark
# Catalyst. 0 for base and wing. (Pain 711 for inciters lands in pain_casts,
# and ;reanim's Pain+Animate cast via Spell#cast so they don't show a `]>`
# echo -- reanim_runs counts the script invocations instead.)
corrupt_casts  = len(re.findall(r"\]>(?:incant|cast) 703\b", txt))
grasp_casts    = len(re.findall(r"\]>(?:incant|cast) 709\b", txt))
catalyst_casts = len(re.findall(r"\]>(?:incant|cast) 719\b", txt))
reanim_runs    = len(re.findall(r"Lich: custom/reanim active|Lich: reanim active", txt))
animate_casts  = len(re.findall(r"Animate Dead|animate the (?:corpse|body|remains)|rises to serve|shambles to its feet", txt))

# ---------------------------------------------------------------- mana
# mana_out: confirmed casts (landed the "gesture"/effect line) * cost, so a
# fizzled prep doesn't count. mana_in: explicit "N mana surge into you"
# (sac4mana's sacrifice) + a flat 50 per Symbol of Mana (the game logs no
# number; Fizzleworth's Symbol of Mana is always a 50-point refill).
SYMBOL_OF_MANA = 50
# "about a/an/the <creature>" is Fizzleworth's Web; "about you" is a creature
# webbing HIM -- don't price that as mana spent.
web_conf    = len(re.findall(r"Cloudy wisps swirl about (?:a |an |the )", txt))
mael_conf   = len(re.findall(r"The winds form into a sinister vortex surrounding", txt))
tether_conf = len(re.findall(r"Cracks form in the air around", txt))
pain_conf   = len(re.findall(r"melding the spiritual and elemental powers by sheer force of will into Pain", txt))
# cat variant confirmed casts -- markers TENTATIVE, verify against a real cat
# log. Fall back to the command-send count if the marker never matched.
corrupt_conf  = len(re.findall(r"blood red haze eddies and swirls around (?:a |an |the )", txt)) or corrupt_casts
grasp_conf    = len(re.findall(r"grotesque limbs .* burst (?:up )?out of the (?:floor|ground)", txt)) or grasp_casts
catalyst_conf = len(re.findall(r"drawing forth the elemental energies|Dark Catalyst|converting .* mana into", txt)) or catalyst_casts
mana_out = (web_conf*COST["web"] + mael_conf*COST["maelstrom"]
            + tether_conf*COST["tether"] + pain_conf*COST["pain"]
            + corrupt_conf*COST["corrupt"] + grasp_conf*COST["grasp"]
            + catalyst_conf*COST["catalyst"])
mana_in = (sum(int(x) for x in re.findall(r"feel (\d+) mana surge into you", txt))
           + SYMBOL_OF_MANA * sym_mana_casts)

# ---------------------------------------------------------------- damage
CREATURE = re.compile(
    r"pestilent vision|Ivasian inciter|magna vereri|dark-eyed incubus|"
    r"the vereri|the inciter|the incubus|the vision", re.I)
OUT_ANCHOR = re.compile(
    r"Large hailstones|Large rocks|Violent winds|A heated breeze|"
    r"Brilliant flashes of lightning|winds form into a sinister vortex|"
    r"Consumed by the hallowed flames|webbing around .* catches fire|"
    r"flames surrounding .* continue to burn|sickly green miasma around|"
    r"Pus-filled sores erupt|Boils rupture|pockmarks appear|"
    r"virulent green mist (?:seeps|passes through|surrounding)|"
    r"shudders and twists in intense pain|contorts in excruciating agony|"
    r"You gesture at|The (?:hail|rocks|winds|bolts|heat) ")
IN_ANCHOR = re.compile(
    r"\bat you!|toward you\b|jabs into you|lunges hungrily for you|"
    r"lashes at you|kicks at you|thorns suddenly grow out from the ground|"
    r"jolts your whole body|One of the thorns")
# The vast majority of incoming attacks whiff (Fizzleworth's DS/TD is huge).
# When an "in" sequence resolves as a miss/ward, clear the context so a
# Maelstrom DoT tick that interleaves right after doesn't get booked as taken.
MISS = re.compile(
    r"A clean miss|Warded off|dissipates upon impact|but you are unaffected|"
    r"to no effect|whacks your legs to no effect|You (?:evade|dodge)|"
    r"manage to jump out of the way|misses you|evade the attack")
DMG_FOR  = re.compile(r"(?:for|causing) (\d+) points of damage!")
DMG_HITS = re.compile(r"hits for (\d+) points of damage!")
DMG_CONT = re.compile(r"^\s*\.\.\. (\d+) points of damage!")

dealt = taken = 0
ctx, ctx_age = None, 99
for s in (l.rstrip("\n") for l in win):
    ctx_age += 1
    if OUT_ANCHOR.search(s):
        ctx, ctx_age = "out", 0
    elif MISS.search(s):
        # a whiffed incoming attack -- clear "in", and don't let the same line
        # re-arm it via IN_ANCHOR ("beam snakes out toward you, but dissipates")
        if ctx == "in":
            ctx = None
    elif IN_ANCHOR.search(s):
        ctx, ctx_age = "in", 0
    m = DMG_HITS.search(s)
    if m:
        taken += int(m.group(1)); ctx, ctx_age = "in", 0; continue
    m = DMG_FOR.search(s)
    if m:
        n = int(m.group(1))
        if CREATURE.search(s):
            dealt += n; ctx, ctx_age = "out", 0
        elif ctx == "in" and ctx_age <= 3:
            taken += n
        else:
            dealt += n; ctx, ctx_age = "out", 0
        continue
    m = DMG_CONT.search(s)
    if m:
        n = int(m.group(1))
        if ctx == "in" and ctx_age <= 3:
            taken += n
        elif ctx == "out":
            dealt += n
        continue

# ---------------------------------------------------------------- wing kit
# All 0 for the `base` variant (no wing code). For `wing`: which Energy Wings
# verb fired, by command send. tap = Luminous Flight (evade buff); knock =
# Blast of Brilliance (<=5-target AOE); fold = Blinding Reprisal (<=10-target
# AOE); push = Wings of Warding (group DS/TD buff); aegis = Prismatic Aegis
# (reactive shield, fired by Fizzleworth-wingguard on an enemy prep).
wing_tap   = len(re.findall(r"\]>tap my wing pin",   txt))
wing_knock = len(re.findall(r"\]>knock my wing pin", txt))
wing_fold  = len(re.findall(r"\]>fold my wing pin",  txt))
wing_push  = len(re.findall(r"\]>push my wing pin",  txt))
wing_aegis = len(re.findall(r"\]>pull my wing pin",  txt))

# ---------------------------------------------------------------- misc
passes  = len(re.findall(r"Lich: custom/Fizzleworth-attack-\S+ active", txt))
stun_ev = len(re.findall(r"You are stunned for \d+ round", txt))
wounds  = len(re.findall(r"shatters a rib|wound to your|fractures your|"
                         r"nerve damage|snaps your", txt))
# SMR-maneuver knockdowns -- a creature pins/sweeps Fizzleworth prone, which
# comes with "acute sense of vulnerability" and a 10s roundtime. Sorcerers
# defend these badly (low maneuver defense) and CS/bolt attacks well, so this
# is the number that actually reflects incoming danger.
knockdowns = txt.count("acute sense of vulnerability")
# a creature webs Fizzleworth (its own SMR maneuver) -- immobilizes, no damage
webbed = txt.count("You become ensnared in thick strands of webbing")
fled    = len(re.findall(r"\bYou (?:flee|retreat)\b|Bigshot.*flees", txt))
kr = [int(x) for x in re.findall(r"You have (\d+) kills remaining", txt)]
bounty = f"{kr[0]+1} -> {kr[-1]} left" if kr else ""
dpm = round(dealt / mana_out, 2) if mana_out else ""
kpm = round(kills / dur_min, 2) if dur_min else ""

row = [date, logfile.split("/")[-1], variant, martial_prowess, start_mind, area, hunt_type,
       duration, dur_min,
       kills, kpm, deaths, passes,
       web_casts, mael_casts, tether_casts, pain_casts, sym_mana_casts,
       corrupt_casts, grasp_casts, catalyst_casts, reanim_runs, animate_casts,
       mana_out, mana_in, dealt, taken, dpm,
       wounds, stun_ev, knockdowns, webbed, fled,
       wing_tap, wing_knock, wing_fold, wing_push, wing_aegis,
       bounty]
print(",".join(str(x) for x in row))
