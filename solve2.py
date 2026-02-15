#!/usr/bin/env python3
"""
Re-analyze the word search grid more carefully.
Let me think about what words could be hiding and work backwards from the clues.
"""

# Grid as given (None = empty/dot position):
raw_grid = [
    "M O R A Y · C O N",      # Row 0
    "U A N L · C S T I",      # Row 1
    "H D · O A I D A ·",      # Row 2
    "· · R T W O · · R R",    # Row 3
    "N E W P E N A E T",      # Row 4
    "· · C I V I N ·",        # Row 5 (only 8 entries)
    "P E D B N S · C ·",      # Row 6
    "Y O H · K W C · S C",   # Row 7
    "T R O R D K · S C",      # Row 8
]

grid = []
for row_str in raw_grid:
    cells = row_str.split()
    row = []
    for c in cells:
        if c == '·':
            row.append(None)
        else:
            row.append(c)
    grid.append(row)

# Pad to max width
max_width = max(len(row) for row in grid)
for i in range(len(grid)):
    while len(grid[i]) < max_width:
        grid[i].append(None)

rows = len(grid)
cols = max_width

print("Grid:")
for i, row in enumerate(grid):
    display = [c if c else '.' for c in row]
    print(f"  {i}: {' '.join(display)}")
print()

# All 8 directions
directions = [
    (0, 1, "right"), (0, -1, "left"),
    (1, 0, "down"), (-1, 0, "up"),
    (1, 1, "DR"), (1, -1, "DL"),
    (-1, 1, "UR"), (-1, -1, "UL"),
]

def find_word(word):
    results = []
    for r in range(rows):
        for c in range(cols):
            for dr, dc, dname in directions:
                found = True
                positions = []
                for k, ch in enumerate(word.upper()):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] and grid[nr][nc] == ch:
                            positions.append((nr, nc))
                        else:
                            found = False
                            break
                    else:
                        found = False
                        break
                if found:
                    results.append((r, c, dname, positions))
    return results

# Let me think about each clue carefully:
#
# 1. "A cold noise?" - Think about what noise is cold. BRRR? Or maybe ICE + a sound?
#    SNAP (cold snap)? CHATTER (teeth chattering)? Let's look for these.
#    Could also be wordplay: "A cold noise" = a noise that is cold = BRRRR
#    Or: noise = DIN, cold DIN = ... no
#    Or: ICE CRACK?
#    Wait - "A cold noise?" with the question mark suggests wordplay.
#    Cold = ICY, CHILL, FROST, FRIGID, COOL, RAW
#    Noise = DIN, BANG, POP, CRACK, SNAP, BOOM, ROAR, HUM
#    "A cold noise" could be... ACHOO (cold -> sneezing)?
#    Let me check: ACHOO - no 'A' adjacent to 'C' in the right way...
#
# 2. "A natural disaster" - TORNADO, FLOOD, DROUGHT, TSUNAMI, etc.
#    TORNADO = T-O-R-N-A-D-O. Let me check manually:
#    T at (4,8), O at... need adjacent O. T(4,8) has no O neighbor.
#    T at (8,0), R at (8,1), O at (8,2) - TRO... then N? (8,2)O's neighbors...
#    T(1,7), R(3,8)? Not adjacent.
#    TWISTER: T-W-I-S-T-E-R... T(3,3) W(3,4) I(2,5)? Not adjacent to W at (3,4)
#    Wait, (3,4) W neighbors include (2,5) I? That's diagonal, yes!
#    T(3,3) W(3,4) I(2,5) S(1,6) T(1,7) E(4,7)? No, (1,7) is T but E would need to be next
#    Not working.
#
# 3. "MrBeast went to see in Greenville, NC" - ECU PIRATES
#    PIRATES = P-I-R-A-T-E-S
#    P(4,3) I(5,3) ... need R adjacent to I(5,3): no R nearby
#    P(6,0) ... I? no I adjacent
#    Let's check for PIRATE or ECU
#
# 4. "Nats" (2 wds) - Could be an anagram hint? NATS = ANTS rearranged?
#    "Nats" as in gnats without the G? PESKY GNATS? NO GNATS?
#    NATS could be baseball Washington Nationals...
#    Wait - maybe it's literally wordplay on "nats" = two words that mean "nats"
#    STINGING INSECTS? NO, too long
#    Could be NATIONAL something... or NAT KING (Cole)?
#    or literally "two nats" = a word that's 2 words meaning/sounding like "nats"
#
# 5. "A certain Midwesterner" - IOWAN, OHIOAN, HOOSIER, KANSAN
#    IOWAN = I-O-W-A-N
#    I(1,8) O? Not adjacent. I(2,5) O(2,3)? Not adjacent.
#    OHIOAN = not likely in grid
#    KANSAN = K...
#
# 6. "A child's toy (2 wds, hyph.)" - YO-YO, POP-GUN, PED-CAR
#    PED is in the grid at (6,0-2)! PED... CAR? C-A-R
#    PED at (6,0)(6,1)(6,2), then need connection...
#    Actually PEDAL-CAR? No, that's not hyphenated normally
#    What about PEN-KNIFE? No, not a toy
#    TOP-KNOT? Not a toy
#    JACK-IN-BOX?
#    YO-YO: Y(0,4)O(0,3)... then Y-O again? Y(0,4) O(0,3) Y... no Y adjacent to (0,3)
#    POP-GUN: not seeing POP in grid
#
# 7. "Upset" - IRATE, MAD, ANGRY, LIVID, MIFFED, IRKED
#    Could also mean OVERTURNED (upset as in turned over)
#    IRATE - not found directly
#    CROSS? No
#    Let's try:
#    PEEVED, ANNOYED, VEXED, RILED
#    ORNERY?
#
# 8. "An item you can buy in MrBeast's store" - HOODIE, HAT, TEE, SHIRT
#    HAT = H-A-T
#    H(2,0) A? A(0,3)? not adjacent. H(7,2) A? no A adjacent.
#    TEE = T(3,3) E... T(4,8) E(4,7) E(4,4)? not adjacent
#    CAP? C(1,5) A(2,4)? Not adjacent. Actually (1,5)C neighbors: (2,4)A? yes diagonal!
#    C(1,5) A(2,4) P? P(4,3)? Not adjacent to A(2,4)... no wait P(4,3) is 2 rows away.
#    Hmm. Let me think...
#
# 9. "A US landmark (2 wds.)" - Could be OLD NORTH (church in Boston)
#    Or MOUNT RUSHMORE, PENN STATION, etc.
#    NEWPENN area is interesting - NEW PENN... PENN as in Pennsylvania?
#    But what US landmark has NEW and PENN?
#    Actually: NEW YORK? No Y adjacent...
#    PENN TOWER? No.
#
# 10. "A type of food" - CORN, RICE, TACO, BREAD, PIE, etc.
#     CORN = C-O-R-N. C(0,6) O(0,7) R? No R adjacent.
#     C(1,5) O(3,5)? Not adjacent.
#     TACO = T-A-C-O. T(3,3) A(0,3)? no. T(1,7) A(2,7)? yes! C? (1,5)? no.
#     OAT = O(0,1) A(1,1)? yes! T? (1,1) neighbors... no T adjacent.
#     O(2,3) A(2,4) T(3,3)? (2,4) to (3,3) is diagonal. Yes!
#     OAT at (2,3)(2,4)(3,3) going down-left!
#     Actually let's check: O at (2,3), A at (2,4), T at... (2,4) to (3,3) is (r+1,c-1) = DL
#     But O to A is (2,3) to (2,4) which is right, not DL. So not consistent direction.
#     RICE? R-I-C-E. R(3,2) I? no I adjacent. R(0,2) I? no.
#     NORI? N-O-R-I.
#     STEW? S-T-E-W.
#     BREAD? PIE? YAM? NOR?
#
# 11. "A literary outlaw (2 wds.)" - ROBIN HOOD
#     ROBIN = R-O-B-I-N, HOOD = H-O-O-D
#     R(8,3) O(8,2) B? No B adjacent.
#     R(3,2)? O... (2,3)? R(3,2) to O(2,3) is UL... then B?
#     Let's look: R(8,1) O(7,1)? up. then B? (6,1) = E. No.
#     R(0,2) O(0,1) B? no B adjacent to (0,1).
#     HOOD: H(2,0) O(0,1)? no. H(7,2) O(7,1)? yes! O(8,2)? H(7,2)O(7,1)O(8,2)?
#     no, (7,1) to (8,2) is DR, but (7,2) to (7,1) is left. Not consistent.
#     H(7,2) O(8,2)? down. O... (8,2) neighbors: R(8,1), R(8,3), H(7,2), D(6,2), etc.
#     No second O adjacent to O(8,2).
#     What about ROB ROY? R-O-B R-O-Y
#     R(8,3) O(8,2) B? no B near.
#
# 12. "What you might say when you finish this!" - HOORAY, DONE, etc.
#     We found MORAY. Could the answer actually be "HOORAY"?
#     But wait - we found MORAY, not HOORAY.
#     Actually... "What you might say when you finish" - the question mark suggests wordplay?
#     Or maybe it's just DONE, VOILA, etc.
#     Let me search more carefully.

# Let me search for a much larger list of words
import itertools

big_word_list = [
    # Clue 1: Cold noise
    "ACHOO", "BRRR", "CHATTER", "SHIVER", "SNAP", "CRACK", "CHILL",
    "SNEEZE", "SNIFF", "BRRRR", "COLD",

    # Clue 2: Natural disaster
    "TORNADO", "TWISTER", "FLOOD", "DROUGHT", "TSUNAMI", "CYCLONE",
    "TYPHOON", "QUAKE", "AVALANCHE", "MUDSLIDE", "WILDFIRE", "HURRICANE",
    "BLIZZARD", "ERUPTION", "TREMOR", "TEMPEST", "SQUALL",

    # Clue 3: Greenville NC
    "PIRATES", "PIRATE", "ECU", "CAROLINA", "PANTHER", "CATAMOUNT",
    "BUCCANEER",

    # Clue 4: Nats (2 words)
    "NATKING", "ANTSY",

    # Clue 5: Midwesterner
    "IOWAN", "OHIOAN", "HOOSIER", "KANSAN", "DAKOTAN", "NEBRASKAN",
    "BUCKEYE", "BADGER", "HAWKEYE", "WOLVERINE", "GOPHER",

    # Clue 6: Child's toy (2 words, hyphenated)
    "YOYO", "POPGUN", "PEDALCAR", "PINWHEEL", "TOPKNOT",
    "HOPTOP", "TIPTOP", "SEESAW",

    # Clue 7: Upset
    "IRATE", "MAD", "ANGRY", "LIVID", "MIFFED", "IRKED", "PEEVED",
    "CROSS", "VEXED", "RILED", "SORE", "HURT", "ANNOYED", "PERTURBED",
    "AGITATED", "ORNERY", "TICKED",

    # Clue 8: MrBeast store item
    "HOODIE", "HAT", "CAP", "SHIRT", "TEE", "SHORTS", "PANTS",
    "SOCKS", "MUG", "POSTER", "STICKER", "FOOTBALL", "TSHIRT",
    "BEANIE", "SNAPBACK", "SWEATSHIRT", "TANKTOPL",

    # Clue 9: US landmark (2 words)
    "PENNSTATION", "OLDNORTH", "WHITEHOUSE", "GRANDCANYON",
    "MOUNTRUSHMORE", "GOLDENGATE", "NEWPORTPIER",
    "TWINPEAKS", "OLDPORT", "NEWPENN",
    "LIBERTYBEL", "STATUEOFLIBERTY",

    # Clue 10: Food
    "CORN", "RICE", "TACO", "BREAD", "PIE", "PORK", "BACON",
    "ROAST", "STEAK", "NORI", "OAT", "OATS", "YAM", "HAM",
    "STEW", "SOUP", "PASTA", "PIZZA", "SUSHI", "RAMEN",
    "TOFU", "KALE", "SALAD", "WRAP", "ROLL", "BUN",

    # Clue 11: Literary outlaw (2 words)
    "ROBINHOOD", "ROBROYSON", "ROBROY",

    # Clue 12: Finish exclamation
    "HOORAY", "DONE", "EUREKA", "VOILA", "HURRAY", "HURRAH",
    "HUZZAH", "WOOHOO", "WAHOO", "YAHOO", "YAY", "HOOEY",
    "WHEW", "TADA", "FINISHED", "COMPLETE", "MORAY",

    # Additional common words to try
    "TOWER", "TWINS", "CIVIC", "PEDAL", "DROIT", "ADROIT",
    "SWORD", "WORDS", "IVORY", "VIOLIN", "RAPID", "VODKA",
    "KNACK", "SNACK", "STACK", "STOCK", "STICK", "THICK",
    "TRICK", "TRACK", "WRACK", "BLACK", "CLOCK", "BLOCK",
    "DRIVE", "THRIVE", "STRIVE", "ARRIVE",
    "HOARD", "BOARD", "CHORD", "SWORD",
    "SCONE", "CONE", "STONE", "DRONE", "THRONE",
    "IVORY", "AVID", "DAVID",
    "HORNET", "HORNS", "ACORN", "UNICORN",
    "WAND", "BAND", "SAND", "LAND", "HAND", "GRAND",
    "AWE", "OWE", "OWN", "OWL", "OWL",
    "PAWN", "DAWN", "FAWN", "LAWN", "YAWN",
    "KNIT", "KNOT", "KNOB", "KNOW", "KNEW", "KNEE",
    "DIVA", "DIVE", "VINE", "VINE", "WINE", "DINE",
    "WREN", "WHEN", "THEN", "OVEN", "EVEN", "SEVEN",
    "NICK", "PICK", "KICK", "SICK", "TICK", "WICK",
    "COIN", "JOIN", "LOIN", "GROIN",
    "ICON", "NICE", "DICE", "MICE", "RICE", "VICE",
    "ADVICE", "DEVICE", "NOVICE", "INVOICE",
    "DEPOT", "PIVOT", "RIVET",
    "EPIC", "OPTIC", "TOPIC", "TROPIC", "NORDIC",
    "TONIC", "SONIC", "IRONIC", "CHRONIC",
    "TRICK", "BRICK", "CHICK", "THICK", "QUICK",
    "CRISP", "WISP", "WASP",
    "SWORD", "WORLD", "WHIRL",
    "TWIST", "WRIST", "MOIST", "HOIST", "JOIST",
    "PEWIT", "KIWI", "WIKI",
    "OWNED", "TOWER", "POWER", "LOWER", "MOWER",
    "CIDER", "RIDER", "WIDER", "SPIDER",
    "UNDER", "WONDER", "THUNDER", "BLUNDER",
    "TROD", "PROD", "PLOD",
    "HORDE", "CHORD", "FJORD",
    "NORTH", "WORTH", "FORTH", "EARTH",
    "TWO", "OWL", "OWN", "OWE", "AWE", "EWE",
    "AIDA", "OAID", "WREN",

    # Let me try ROBIN and HOOD separately
    "ROBIN", "HOOD",

    # More targeted:
    "DORK", "CORK", "FORK", "PORK", "WORK", "STORK",
    "TROD", "SWORD",
    "CROWD", "CROWN", "CLOWN", "BROWN", "DROWN", "FROWN", "GROWN",
    "SHOWN", "SOWN", "TOWN", "DOWN", "GOWN", "OWN",
    "NEWT", "PEWT",
    "ANET", "PEANUT",
    "PENKNIFE",
    "PENNANT",
    # Let's try very short words
    "TWO", "OAR", "OAK", "DAD", "MOM", "PEW",
    "NAP", "PAN", "TAN", "VAN", "RAN", "CAN", "DAN", "FAN", "MAN",
    "PEA", "SEA", "TEA",
    "NET", "PET", "SET", "WET", "BET", "GET", "JET", "LET", "MET",
    "WAD", "DAM", "RAM", "JAM", "HAM", "YAM",
    "AID", "BID", "DID", "HID", "KID", "LID", "RID",
    "NEW", "DEW", "FEW", "HEW", "JEW", "MEW", "PEW", "SEW",
    "AWE", "EWE", "OWE",
    "PEW", "DEW",
    "ORE", "IRE", "ARE",
    "AND", "END",
    "INK", "LINK", "SINK", "RINK", "WINK", "PINK", "MINK", "KINK",
    "OOH", "COO", "MOO", "BOO", "GOO", "TOO", "WOO", "ZOO",
    # Maybe the grid has CIVIC
    "CIVIC",
    # Other
    "DAVID", "AIDA",
    # PEDRO?
    "PEDRO",
    # CDS, DVD
    # RADIAN
    "RADIAN",
    # NADIR
    "NADIR",
    # TROPIC
    "TROPIC",
    # TOWN
    "TOWN",
    "OWT",  # reversed TWO
    # IOWA
    "IOWA",
    # WAND
    "WAND",
    # PANDA
    "PANDA",
    # DEN, PEN, HEN, BEN, KEN, MEN, TEN, YEN, ZEN
    "DEN", "HEN", "BEN", "KEN", "MEN", "TEN", "YEN", "ZEN",
    # Specifically: what about TORNADO as T-O-R-N-A-D-O?
    # T(8,0) going... O(8,2)? not adjacent to T(8,0)... wait T(8,0) R(8,1) O(8,2) is right.
    # But then we need R(8,1) after T going right: TRO... then N: need N at (8,3) but it's R
    # TORNADO won't work that way.
    # What about TWISTER going backwards?
    # TYPHOON
    # What about TWO-NADO? No...
    # CYCLONE?
    # Let me look for flood: F-L-O-O-D - no F in grid

    # PEW
    "PEW",
    # Wait - cold noise could be "CHATTER" but also could be "ACHOO" (you have a cold!)
    # "A cold noise?" - You have a cold = you sneeze = ACHOO
    # But also the ? suggests wordplay
    # ICE + noise = ICE CRACK? ICE POP?
    # COLD = C-O-L-D, look for that

    # ROB? ROD? ROT? ROW? ROE?
    "ROB", "ROD", "ROT", "ROW", "ROE",
    # ROBIN: R-O-B-I-N
    # R at (3,8), O? no O adjacent
    # R at (8,3), O at (8,2), B? no B adjacent to (8,2)
    # R at (0,2), O at (0,1), B? no B adjacent to (0,1)

    # Let me reconsider the grid. Maybe I have the grid WRONG.
    # The user typed dots as · but maybe those positions actually have letters
    # that were obscured or are water droplet markers ON TOP of letters.

    # With the grid as-is, let me search for partial words
    "PEDBN", "PEDBNS",

    # TOWER going up from T(8,0)?
    # T(8,0) O(7,1)? (8,0) to (7,1) = UL... no, that's up-right
    # Actually (8,0) to (7,0) = up = Y. T-Y not TOWER
    # T(8,0) to (7,1) = up-right = O. T-O going UR.
    # Then (7,1) to (6,2)=D? T-O-D not TOWER

    # TWIN
    "TWIN",
    # T(3,3) W(3,4) I(5,3)? (3,4)to(5,3)? That's 2 rows, not adjacent
    # T(3,3) W(3,4) I(2,5)? (3,4)to(2,5) is UL... wait (3,4) to (2,5) is (-1,+1) = UR
    # T(3,3) W(3,4) I... I at (2,5) via UR from W. then N? from (2,5) going UR = (1,6) = S. no.
    # T(4,8) going where?

    # NEWPENCE - a British coin
    "NEWPENCE",
    # N(4,0) E(4,1) W(4,2) P(4,3) E(4,4) N(4,5) ... then C(5,2)? not adjacent to N(4,5)
    # Wait: after NEWPEN, C would need to be adjacent to N(4,5)
    # N(4,5) neighbors: (3,4)W (3,5)O (3,6)None (4,4)E (4,6)A (5,4)V (5,5)I (5,6)N
    # No C adjacent to N(4,5). So NEWPENCE doesn't work reading straight.

    # Let me try: what if clue 9 (US landmark, 2 words) is "OLD NORTH"?
    # Let me look for OLD: O-L-D
    # O(0,1) L(1,3)? not adjacent
    # O(2,3) L(1,3)? yes, up! D? D(2,1)? (1,3) to (2,1)? not adjacent.
    # O(3,5) L? no L adjacent

    # What about PEW?
    # P(4,3) E(4,2)? no wait E(4,4)? P(4,3) to E(4,4) is right. W(4,2) is left of P.
    # PEW: P(4,3) E(4,4) W(3,4)? (4,4) to (3,4) = up. But P to E is right, E to W is up.
    # Not a straight line.
    # P(6,0) E(6,1) W? no W adjacent to (6,1)

    # HOW about checking words reading diagonally more carefully

    # ANODE? DIODE?
    # DIVE: D(2,6) I(2,5)? going left. V? (2,4)=A. No.
    # D(6,2) I(5,3)? going UR. V(5,4)? wait (5,3) to (5,4) is right, not UR.
    # Not consistent.

    # VIE, VIN, VIC
    "VIE", "VIC",

    # STAID
    "STAID",

    # NAIAD (water nymph - fits the water theme!)
    "NAIAD",

    # NIT
    "NIT",

    # KNIVES
    "KNIVES",

    # PECAN?
    "PECAN",

    # CANOE - fits water theme
    "CANOE",

    # WADI (dry river bed - water related!)
    "WADI",

    # OINK
    "OINK",

    # TEA
    "TEA",

    # PEA
    "PEA",

    # Let me try some more obscure but fitting answers:
    # Clue 1: "A cold noise?" with ? = wordplay
    # Cold = having a cold (illness). Noise of a cold = SNEEZE, COUGH, SNIFFLE, ACHOO
    # Or: Cold as in temperature. Cold noise = ?
    # SNAP as in "cold snap"? But that's a weather term, not a noise.
    # What if "cold" modifies "noise" literally: a noise that makes you cold = CHILL?
    # Or a noise ABOUT cold?
    # BRRR is the most obvious "cold noise"
    # But maybe it's a pun: MOAN (sounds like MOWN?) No...
    # ICE CREAM? No...
    # AH-CHOO!

    # Wait, I see TWO in the grid at (3,3)(3,4)(3,5)
    # I see OWT (reverse TWO) at same spot going left

    # What if there are letters hidden under the dots?
    # That would make this a fully filled 9x10 or 10x10 grid.
]

# Remove duplicates
big_word_list = list(set(big_word_list))

print("=== SEARCHING BIG WORD LIST ===\n")
found = {}
for word in sorted(big_word_list):
    results = find_word(word)
    if results:
        found[word] = results
        for r, c, direction, positions in results:
            print(f"  FOUND '{word}' at ({r},{c}) going {direction}: {positions}")

print(f"\n\nTotal unique words found: {len(found)}")
print("Words found:", sorted(found.keys()))
