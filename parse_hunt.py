#!/usr/bin/env python3
"""Parse a Saga/GS4 combat-log window and emit one CSV row of hunt stats.

Usage: parse_hunt.py <logfile> <start> <end> <date> <variant> <area> <hunt_type> <duration>

<start>/<end> bracket the combat stretch: from the first "Bigshot hunting" /
first "Fizzleworth-attack-* active" to just past the last
"Fizzleworth-attack-* has exited" (before the rest/travel-out).
<duration> is bigshot's own "Last Hunt" figure.
"""
import re, sys

logfile, start, end, date, variant, area, hunt_type, duration = (
    sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])

with open(logfile, encoding="utf-8", errors="replace") as fh:
    win = fh.readlines()[start-1:end]
txt = "".join(win)

# ---------------------------------------------------------------- spell costs
# Targeted casts, from GS4 spell data (see Fizzleworth-attack-wing.lic header).
COST = {"web": 5, "maelstrom": 10, "tether": 6, "pain": 11}

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

# ---------------------------------------------------------------- mana
# mana_out: confirmed casts (landed the "gesture"/effect line) * cost, so a
# fizzled prep doesn't count. mana_in: explicit "N mana surge into you"
# (sac4mana's sacrifice); Symbol of Mana gives no number in the log -- see
# sym_mana_casts and the notes column.
web_conf    = len(re.findall(r"Cloudy wisps swirl about", txt))
mael_conf   = len(re.findall(r"The winds form into a sinister vortex surrounding", txt))
tether_conf = len(re.findall(r"Cracks form in the air around", txt))
pain_conf   = len(re.findall(r"melding the spiritual and elemental powers by sheer force of will into Pain", txt))
mana_out = (web_conf*COST["web"] + mael_conf*COST["maelstrom"]
            + tether_conf*COST["tether"] + pain_conf*COST["pain"])
mana_in = sum(int(x) for x in re.findall(r"feel (\d+) mana surge into you", txt))

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
DMG_FOR  = re.compile(r"(?:for|causing) (\d+) points of damage!")
DMG_HITS = re.compile(r"hits for (\d+) points of damage!")
DMG_CONT = re.compile(r"^\s*\.\.\. (\d+) points of damage!")

dealt = taken = 0
ctx, ctx_age = None, 99
for s in (l.rstrip("\n") for l in win):
    ctx_age += 1
    if OUT_ANCHOR.search(s):
        ctx, ctx_age = "out", 0
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

# ---------------------------------------------------------------- misc
passes  = len(re.findall(r"Lich: custom/Fizzleworth-attack-\S+ active", txt))
stun_ev = len(re.findall(r"You are stunned for \d+ round", txt))
wounds  = len(re.findall(r"shatters a rib|wound to your|fractures your|"
                         r"nerve damage|snaps your", txt))
fled    = len(re.findall(r"\bYou (?:flee|retreat)\b|Bigshot.*flees", txt))
kr = [int(x) for x in re.findall(r"You have (\d+) kills remaining", txt)]
bounty = f"{kr[0]+1} -> {kr[-1]} left" if kr else ""
dpm = round(dealt / mana_out, 2) if mana_out else ""

row = [date, logfile.split("/")[-1], variant, area, hunt_type, duration,
       kills, deaths, passes,
       web_casts, mael_casts, tether_casts, pain_casts, sym_mana_casts,
       mana_out, mana_in, dealt, taken, dpm,
       wounds, stun_ev, fled, bounty]
print(",".join(str(x) for x in row))
