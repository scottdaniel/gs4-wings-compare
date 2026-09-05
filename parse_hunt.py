#!/usr/bin/env python3
"""Parse a Saga/GS4 combat-log window and emit one CSV row of hunt stats.

Usage: parse_hunt.py <logfile> <start> <end> <date> <variant> <area> <hunt_type> <duration>
"""
import re, sys

logfile, start, end, date, variant, area, hunt_type, duration = (
    sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])

with open(logfile, encoding="utf-8", errors="replace") as fh:
    win = fh.readlines()[start-1:end]
txt = "".join(win)

CREATURE = re.compile(
    r"pestilent vision|Ivasian inciter|magna vereri|dark-eyed incubus|"
    r"the vereri|the inciter|the incubus|the vision", re.I)

# Fizzleworth's outgoing damage: Energy Maelstrom SMR ticks, ensorcelled-scepter
# flare, and his disease/mist DoT ("causing N").
OUT_ANCHOR = re.compile(
    r"Large hailstones|Large rocks|Violent winds|A heated breeze|"
    r"Brilliant flashes of lightning|winds form into a sinister vortex|"
    r"Consumed by the hallowed flames|webbing around .* catches fire|"
    r"flames surrounding .* continue to burn|sickly green miasma around|"
    r"Pus-filled sores erupt|Boils rupture|pockmarks appear|"
    r"virulent green mist (?:seeps|passes through|surrounding)|"
    r"You gesture at|The (?:hail|rocks|winds|bolts|heat) ")
# incoming (creature -> Fizzleworth) -- deliberately strict
IN_ANCHOR = re.compile(
    r"\bat you!|toward you\b|jabs into you|lunges hungrily for you|"
    r"lashes at you|kicks at you|thorns suddenly grow out from the ground|"
    r"jolts your whole body|One of the thorns")

DMG_FOR   = re.compile(r"(?:for|causing) (\d+) points of damage!")
DMG_HITS  = re.compile(r"hits for (\d+) points of damage!")
DMG_CONT  = re.compile(r"^\s*\.\.\. (\d+) points of damage!")

dealt = taken = 0
ctx = None           # 'out' | 'in'
ctx_age = 99
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
        if CREATURE.search(s):                 # names a creature -> Fizz dealt it
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

kills    = txt.count("rises into the heavens")
deaths   = len(re.findall(r"^\s*You are dead!", txt, re.M))
webs     = len(re.findall(r"\]>incant 118\b", txt))
maels    = len(re.findall(r"\]>cast #\d+", txt))
tethers  = len(re.findall(r"\]>incant 706\b", txt))
passes   = len(re.findall(r"Lich: custom/Fizzleworth-attack-\S+ active", txt))
sym_mana = len(re.findall(r"\]>symbol of mana", txt))
stun_ev  = len(re.findall(r"You are stunned for \d+ round", txt))
wounds   = len(re.findall(r"shatters a rib|wound to your|fractures your|"
                          r"nerve damage|snaps your", txt))
fled     = len(re.findall(r"\bYou (?:flee|retreat)\b|Bigshot.*flees", txt))
kr = [int(x) for x in re.findall(r"You have (\d+) kills remaining", txt)]
bounty = f"{kr[0]+1}/{'?' if kr[0]+1 != 10 else 10} -> {kr[-1]} left" if kr else ""

row = [date, logfile.split("/")[-1], variant, area, hunt_type, duration,
       kills, deaths, passes, webs, maels, tethers, sym_mana,
       dealt, taken, wounds, stun_ev, fled, bounty]
print(",".join(str(x) for x in row))
