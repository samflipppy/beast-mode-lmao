#!/usr/bin/env python3
"""
BREAKTHROUGH: All Stage 1 answers are of the same type - likely LOCATIONS!
The meta-clue is: "EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD"

So each clue answer is a LOCATION/PLACE NAME!

Let me re-interpret each clue as leading to a location name:

1. "A cold noise?" → Place name that is a cold noise
   BRRR? No place. ACHOO? No.
   CRACK? SNAP? CHATTER?
   Wait - wordplay: Cold + Noise = ?
   Cold = ICE, FROST, SNOW, CHILL, NIPPY, ARCTIC, FRIGID
   Noise = BANG, DIN, POP, HUM, ROAR, CRACK, SNAP
   ICE + LAND = ICELAND! (a location!)
   SNAP + ? = ?
   Or: SHIVER? QUIVER?
   What about OSLO? NOME? ARCTIC?
   Or "cold noise" = BRRR → BURR → a place?
   Or CHILL + ? = CHILE?

2. "A natural disaster" → Location name
   TORNADO? VOLCANO? TSUNAMI?
   Location: POMPEII? No, that's associated with disaster.
   Wait - many locations ARE named after natural disasters or vice versa.
   What about NIAGARA (Falls - a natural wonder)?
   Or locations associated with disasters?

3. "MrBeast went to see in Greenville, NC" → Location name
   ECU? PIRATE? But these aren't really locations.
   Greenville itself? Or a venue IN Greenville?
   MrBeast went to see something at ECU - could be a GAME, a SHOW?
   Or "went to see" = visited a location. What location in Greenville?

4. "Nats" (2 wds.) → Location name that sounds like/relates to "Nats"
   WASHINGTON (Nationals)? Or DC?
   Wait - "Nats" 2 words = ? Two words for Nats?

5. "A certain Midwesterner" → Location name
   IOWA? OHIO? KANSAS? INDIANA?
   Or DAKOTAN → DAKOTA?

6. "A child's toy (2 wds, hyph.)" → Location name
   JACK-IN-THE-BOX? TOP-NOTCH?
   YO-YO → not a location
   POP-GUN → not a location
   But wait: PEW is in the grid... PEW-TER? No.
   BOWLING (Green)?

7. "Upset" → Location name
   TIPPED? CAPSIZED?
   Or "upset" as reversal: ROMA (AMOR reversed)?

8. "An item you can buy in MrBeast's store" → Location name
   TEE → a location starting with TEE?
   JERSEY (as in a shirt/jersey - New Jersey)?
   CAPE (as in Cape Cod)?
   HAT (Hatteras)?

9. "A US landmark (2 wds.)" → This IS already a landmark!
   So this is a US landmark that is also a location.
   MOUNT RUSHMORE? GOLDEN GATE? STATUE OF LIBERTY?
   Wait - but all answers should be locations, and a US landmark IS a location.
   So this one is straightforward.

10. "A type of food" → Location name
    TURKEY! (country + food)
    CHILE! (country + food)
    HAMBURG! LIMA! NAPOLI! DAMASCUS!
    JORDAN (the almond)? GUINEA?
    CORK (Ireland)? DATES?
    JAVA (coffee)?

11. "A literary outlaw (2 wds.)" → Location name
    ROBIN HOOD → NOTTINGHAM? SHERWOOD?
    Or: ROBIN HOOD itself is 2 words = a location?
    SHERWOOD FOREST?

12. "What you might say when you finish this!" → Location name
    EUREKA (city in California!!)
    DONE? VICTORIA? TRIUMPH?
    EUREKA is perfect - it's what you say when you solve something,
    AND it's a city in California!

EUREKA is very promising for #12!

Now let me re-search the grid for LOCATION NAMES:
"""

grid = [
    ['M','O','R','A','Y', None,'C','O','N'],
    ['U','A','N','L', None,'C','S','T','I'],
    ['H','D', None,'O','A','I','D','A', None],
    [None, None,'R','T','W','O', None, None,'R'],
    ['N','E','W','P','E','N','A','E','T'],
    [None, None,'C','I','V','I','N', None, None],
    ['P','E','D','B','N','S', None,'C', None],
    ['Y','O','H', None,'K','W','C', None,'S'],
    ['T','R','O','R','D','K', None,'S','C'],
]

rows = 9
cols = 9

dirs = [
    (0, 1, 'R'), (0, -1, 'L'),
    (1, 0, 'D'), (-1, 0, 'U'),
    (1, 1, 'DR'), (1, -1, 'DL'),
    (-1, 1, 'UR'), (-1, -1, 'UL'),
]

def find_any(word):
    results = []
    for r in range(rows):
        for c in range(cols):
            for dr, dc, dname in dirs:
                ok = True
                wc = 0
                info = []
                for k, ch in enumerate(word):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        cell = grid[nr][nc]
                        if cell == ch:
                            info.append(f'{ch}({nr},{nc})')
                        elif cell is None:
                            wc += 1
                            info.append(f'[{ch}]({nr},{nc})')
                        else:
                            ok = False
                            break
                    else:
                        ok = False
                        break
                if ok:
                    results.append((dname, wc, info))
    return results

# Search for location names that match clue answers
locations = [
    # Clue 1: Cold noise → location
    "ICELAND", "OSLO", "NOME", "CHILE", "ARCTIC",
    "SIBERIA", "ALASKA", "YUKON", "NUNAVUT",
    "BURR", "SNAP",  # Burr Ridge? Snap?

    # Clue 2: Natural disaster → location
    "POMPEII", "TORNADO", "CYCLONE", "STORM",
    "VESUVIUS", "KRAKATOA", "KATRINA",

    # Clue 3: Greenville NC
    "GREENVILLE", "CAROLINA", "PIRATE", "ECU",

    # Clue 4: Nats (2 wds)
    "WASHINGTON", "TWONAT",

    # Clue 5: Midwesterner
    "IOWA", "OHIO", "INDIANA", "KANSAS", "DAKOTA",
    "NEBRASKA", "WISCONSIN", "MICHIGAN", "MINNESOTA",
    "ILLINOIS",

    # Clue 6: Child's toy (2 wds, hyph)
    "TOPEKA",  # TOP + EKA?

    # Clue 7: Upset
    "TROY",  # Troy -> overthrown/upset city?
    "TIPPERA",  # Tipperary?

    # Clue 8: MrBeast store item
    "JERSEY",  # New Jersey - jersey is clothing
    "CAPE",  # Cape Cod - cape is clothing
    "PANAMA",  # Panama hat
    "STETSON",

    # Clue 9: US landmark (2 wds)
    "RUSHMORE", "GOLDENGATE", "MOUNTVERNON",
    "LIBERTYBEL", "GRANDCANYON", "WHITEHOUSE",
    "PLYMOUTH", "ALAMO", "PENNSTATION",
    "ELLISISLAND", "OLDNORTH",

    # Clue 10: Food → location
    "TURKEY", "CHILE", "HAMBURG", "LIMA",
    "CORK", "JAVA", "NAPLES", "BOLOGNA",
    "GUINEA", "JORDAN", "DAMASCUS", "BATH",
    "BISCAY", "MADEIRA", "SARDINIA",

    # Clue 11: Literary outlaw (2 wds)
    "NOTTINGHAM", "SHERWOOD",
    "ROBINHOOD",  # Robin Hood, Texas? Robin Hood, Maine?

    # Clue 12: Finish exclamation
    "EUREKA",  # Eureka, California!
    "VICTORIA", "TRIUMPH",
    "DONEGAL",  # Done + gal?

    # Additional locations to try
    "DARWIN", "PERTH", "YORK", "OXFORD",
    "CAMBRIDGE", "CAIRO", "ROME", "PARIS",
    "MADRID", "VIENNA", "TOKYO", "DELHI",
    "DUBAI", "NAIROBI", "ACCRA",  # Ghana - mentioned in puzzle!
    "KAMPALA", "KINSHASA", "DAKAR", "RABAT",
    "TRIPOLI", "TUNIS", "ALGIERS",
    "BOSTON", "DENVER", "AUSTIN", "RENO",
    "KENT", "DOVER", "YORK",
    "DARWIN", "BOISE", "WACO",
    "ADEN", "NICE", "TROD",
    "TWIN", "NEWPENN",
    "NEWPORT", "NEWTOWN", "NEWHAVEN",
    "STOCKTON", "TRENTON", "PRINCETON",
    "CAMDEN", "EDISON", "HOBOKEN",
    "NORWOOD", "EASTWICK", "WESTPORT",
    "NORTH", "SOUTH", "EAST", "WEST",
    "NEWARK", "NEWMARKET",
    "MORAY", "DEVON", "CORNWALL",
    "KENT", "ESSEX", "SURREY",
    "STAFFORD", "OXFORD", "NORFOLK",

    # Key Africa locations (since the video is about wells in Africa)
    "ACCRA", "GHANA", "NAIROBI", "KENYA",
    "KAMPALA", "UGANDA", "RWANDA",
    "CHAD", "MALI", "NIGER", "TOGO", "BENIN",
    "SENEGAL", "GAMBIA", "CONGO",
]

print("=== SEARCHING FOR LOCATION NAMES ===\n")
for word in sorted(set(locations)):
    results = find_any(word.upper())
    if results:
        results.sort(key=lambda x: x[1])
        best = results[0]
        dname, wc, info = best
        if wc <= len(word) // 2:
            pct = (len(word) - wc) / len(word) * 100
            print(f"  {word:20s} {dname:3s} wc={wc}/{len(word)} ({pct:.0f}%): {' '.join(info)}")

# Also search for some specific compound names
compounds = [
    "NEWPENN", "NEWPORT", "NEWTOWN", "NEWYORK",
    "OLDNORTH", "PEDALCAR",
    "CAPECOD", "NEWJERSEY",
]
print("\nCompound names:")
for word in compounds:
    results = find_any(word.upper())
    if results:
        results.sort(key=lambda x: x[1])
        best = results[0]
        dname, wc, info = best
        if wc <= len(word) // 2:
            pct = (len(word) - wc) / len(word) * 100
            print(f"  {word:20s} {dname:3s} wc={wc}/{len(word)} ({pct:.0f}%): {' '.join(info)}")
