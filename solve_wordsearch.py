#!/usr/bin/env python3
"""
Solve the MrBeast word search puzzle.
The grid as given (dots represent empty/droplet cells):
"""

# Let me represent the grid exactly as given.
# Using None for empty/dot positions.

# Row 0: M O R A Y · C O N
# Row 1: U A N L · C S T I
# Row 2: H D · O A I D A ·
# Row 3: · · R T W O · · R R
# Row 4: N E W P E N A E T
# Row 5: · · C I V I N · ·
# Row 6: P E D B N S · C ·
# Row 7: Y O H · K W C · S C
# Row 8: T R O R D K · S C

# Let's figure out columns. Row 3 and 7 have 10 entries.
# Most rows have 9. Let me see if 10-column grid works.

# Actually, let me re-examine. Maybe the grid is 10 columns wide:
# R0: M O R A Y . C O N .    (10 cols, last is empty)
# R1: U A N L . C S T I .    (10 cols, pos4 empty, last empty)
# R2: H D . O A I D A . .    (10 cols, pos2 empty, pos8,9 empty)
# R3: . . R T W O . . R R    (10 cols, pos0,1,6,7 empty)
# R4: N E W P E N A E T .    (10 cols, last empty)
# R5: . . C I V I N . . .    (10 cols)
# R6: P E D B N S . C . .    (10 cols)
# R7: Y O H . K W C . S C    (10 cols)
# R8: T R O R D K . S C .    (10 cols)

# But actually that adds trailing dots that weren't in the original.
# Let me try 9 columns wide instead:
# R3 has: . . R T W O . . R R - that's 10 entries, doesn't fit 9 cols
# R7 has: Y O H . K W C . S C - that's 10 entries

# Maybe R3 should be: . R T W O . . R R (9 cols, first dot is in col 0)
# And . . is just one dot? No, that doesn't make sense.

# Let me try another approach: maybe the grid ISN'T rectangular.
# Or maybe I'm miscounting. Let me count very carefully.

# The user wrote:
# M O R A Y · C O N          <- 6 letters + 1 dot + 2 letters = 9 cells
# U A N L · C S T I          <- 4 letters + 1 dot + 4 letters = 9 cells
# H D · O A I D A ·          <- 2 letters + 1 dot + 5 letters + 1 dot = 9 cells
# · · R T W O · · R R        <- 2 dots + 4 letters + 2 dots + 2 letters = 10 cells
# N E W P E N A E T          <- 9 letters = 9 cells
# · · C I V I N · ·          <- 2 dots + 5 letters + 2 dots = 9 cells (wait: ·  · = 2)
#                             actually: · · C I V I N · = 8? No...
#                             Let me count: dot, dot, C, I, V, I, N, dot = 8?
#                             But there's a trailing dot too making 9

# Hmm, let me re-read the user's message more carefully:
# "· · C I V I N ·" - that's 8, but with trailing newline space maybe 9?
# Actually user wrote: "· · C I V I N ·"
# Counting: ·(1) ·(2) C(3) I(4) V(5) I(6) N(7) ·(8) ... = 8 cells
# vs row 4: N E W P E N A E T = 9 cells

# This is getting confusing. Let me just count the exact characters.

# Let me use a different approach. I'll define the grid as strings and parse:

raw_grid = [
    "M O R A Y · C O N",
    "U A N L · C S T I",
    "H D · O A I D A ·",
    "· · R T W O · · R R",
    "N E W P E N A E T",
    "· · C I V I N ·",
    "P E D B N S · C ·",
    "Y O H · K W C · S C",
    "T R O R D K · S C",
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

# Print grid dimensions
for i, row in enumerate(grid):
    print(f"Row {i}: {len(row)} cells -> {row}")

print()

# Find max width
max_width = max(len(row) for row in grid)
print(f"Max width: {max_width}")
print(f"Rows: {len(grid)}")

# Pad shorter rows with None
for i in range(len(grid)):
    while len(grid[i]) < max_width:
        grid[i].append(None)

print("\nPadded grid:")
for i, row in enumerate(grid):
    display = [c if c else '.' for c in row]
    print(f"Row {i}: {' '.join(display)}")

# Now search for words in all 8 directions
directions = [
    (0, 1),   # right
    (0, -1),  # left
    (1, 0),   # down
    (-1, 0),  # up
    (1, 1),   # down-right
    (1, -1),  # down-left
    (-1, 1),  # up-right
    (-1, -1), # up-left
]

dir_names = {
    (0, 1): "right",
    (0, -1): "left",
    (1, 0): "down",
    (-1, 0): "up",
    (1, 1): "down-right",
    (1, -1): "down-left",
    (-1, 1): "up-right",
    (-1, -1): "up-left",
}

rows = len(grid)
cols = max_width

def find_word(word):
    results = []
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                found = True
                positions = []
                for k, ch in enumerate(word):
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
                    results.append((r, c, dir_names[(dr, dc)], positions))
    return results

# List of candidate words for each clue
candidates = {
    "1. Cold noise": ["BRRR", "CHATTER", "SHIVER", "SNAP", "CRACK", "CHILL", "ICE", "BRRRRR", "BRRRR"],
    "2. Natural disaster": ["TORNADO", "TSUNAMI", "FLOOD", "DROUGHT", "CYCLONE", "TYPHOON", "TWISTER", "QUAKE", "EARTHQUAKE", "AVALANCHE", "MUDSLIDE", "WILDFIRE", "HURRICANE"],
    "3. MrBeast Greenville NC": ["PIRATES", "ECU", "PIRATE", "CAROLINA", "PANTHER"],
    "4. Nats (2 wds)": ["NATIONAL PARK", "NATIONAL TEAM", "NATURAL ONES", "WASHINGTON NATIONALS", "PESKY GNATS", "STINGING NATS"],
    "5. Midwesterner": ["IOWAN", "OHIOAN", "HOOSIER", "KANSAN", "DAKOTAN", "NEBRASKAN"],
    "6. Child's toy (2 wds hyph)": ["YOYO", "POPGUN", "JACKINTHEBOX", "TEDDY BEAR", "TOPKNOT", "PEDCAR", "PEDALCAR"],
    "7. Upset": ["MAD", "IRATE", "ANGRY", "MIFFED", "RILED", "PEEVED", "CROSS", "LIVID", "VEXED", "IRE", "IRKED", "SORE", "HURT", "DISTRAUGHT", "PERTURBED", "ANNOYED", "AGITATED", "BOTHERED", "DISTURBED", "OVERWROUGHT"],
    "8. MrBeast store item": ["HOODIE", "TSHIRT", "HAT", "CAP", "SHIRT", "TEE", "SHORTS", "PANTS", "SOCKS", "MUG", "POSTER", "STICKER", "FOOTBALL"],
    "9. US landmark (2 wds)": ["MOUNT RUSHMORE", "OLDNORTH", "PENNSTATION", "NEWPENN", "OLDNORTH", "WHITEHOUSE", "GRANDCANYON", "GOLDGATE"],
    "10. Type of food": ["CORN", "RICE", "TACO", "BREAD", "STEW", "PIE", "PORK", "BACON", "NORI", "ROAST", "OAT"],
    "11. Literary outlaw (2 wds)": ["ROBINHOOD", "ROBIN HOOD", "ROB ROY"],
    "12. Finish exclamation": ["HOORAY", "DONE", "EUREKA", "VOILA", "HURRAY", "HURRAH", "HUZZAH", "WOOHOO", "WAHOO", "YAHOO", "YAY", "MORAY", "HOOEY", "WHEW"],
}

# Flatten and search all candidates
print("\n=== SEARCHING FOR ALL CANDIDATE WORDS ===\n")
for clue, words in candidates.items():
    print(f"\n--- {clue} ---")
    for word in words:
        # Remove spaces for searching
        search_word = word.replace(" ", "")
        results = find_word(search_word)
        if results:
            for r, c, direction, positions in results:
                print(f"  FOUND '{word}' at ({r},{c}) going {direction}, positions: {positions}")

# Also search for some additional words I might have missed
print("\n=== SEARCHING ADDITIONAL WORDS ===\n")
additional = [
    "MORAY", "TOWER", "TWINS", "CIVIC", "PEDAL", "CAR", "NEWPEN",
    "PENN", "TROT", "TORT", "WREN", "PAWN", "ANEW", "TWIST",
    "KNIVES", "DIVA", "DIVE", "VINE", "VINES", "WINDS", "WIND",
    "SWORD", "WORD", "TROD", "RODE", "ROAD", "ROAM", "MOAN",
    "LOAN", "OAR", "OAT", "OINK", "INK", "SINK", "SKIN",
    "KIND", "BIND", "VINE", "WINE", "DINE", "NINE", "PINE",
    "CORD", "COIN", "ICON", "NICE", "DICE", "ICE", "ACE",
    "PEN", "NEW", "WADE", "WADI", "TOAD", "LOAD", "NOVA",
    "PANIC", "TROPE", "PETER", "PEWTER", "NEWTON", "DEPOT",
    "HORDE", "NORD", "HORN", "THORN", "NORTH", "WORTH",
    "IVORY", "IVORY", "AVID", "RAPID", "SNIDE", "SIDE",
    "HIDE", "RIDE", "WIDE", "PRIDE", "BRIDE", "STRIDE",
    "CON", "COD", "COT", "COW", "COP", "CUP", "CUR", "CUT",
    "EPIC", "DRONE", "ROPE", "HOPE", "COPE", "DOPE", "MOPE",
    "TROPHY", "PYTHON", "TYPHON",
    "NEWPENCE", "OLDPEN", "PENKNIFE",
    "PEDAL", "PEDALCAR",
    "STORK", "STOCK", "STICK", "STACK",
    "HOODIE", "HOOD",
    "ROBINHOOD",
    "DAD", "MOM", "MUD", "HUM",
    "NATURAL", "NATION", "NATIONAL",
    "IOWAN", "OHIOAN", "KANSAN",
    "IRATE",
    "CIVIC",
    "TWINE", "OPTIC", "TOPIC",
    "TONIC", "SONIC", "IRONIC",
    "WOLVERINE", "BADGER",
    # Try more specific compound words
    "NEWPENN", "OLDPENN",
    "PENBLADE", "PENKNIFE", "PENNANT",
    # Food
    "CORN", "RICE", "TACO", "BREAD", "PIE", "PORK", "BACON", "ROAST",
    "STEAK", "NORI", "OAT", "OATS", "YAM",
    # US Landmarks
    "WHITEHOUSE", "PENNAVE",
    # Try ROBIN HOOD as one word
    "ROBINHOOD",
    # ECU
    "ECU", "PIRATE",
    # Toys
    "TOPGUN", "POPGUN",
    "YOYO",
    # Try JACK IN THE BOX words
    "JACKINBOX",
    # Snow/Cold words
    "SNAP", "FROST", "BRRR", "CHATTER", "SHIVER",
    "ACHOO",
    # Others
    "DORK", "CORK", "PORK", "FORK", "WORK", "STORK",
    "TRICK", "TRACK", "CRACK", "WRACK",
    "DEBT", "DOUBT",
    "HOVER", "COVER", "LOVER", "OVER", "ROVER",
    "ADROIT", "DETROIT",
    "TWIST", "TWIT", "TWIN", "TWINS",
    "SWORD", "WORDS",
    "PEWIT", "KIWI",
    "OWL", "COW", "BOW", "ROW", "SOW", "TOW", "VOW", "WOW", "HOW", "NOW",
    "SCOW", "SHOW",
    "SNACK", "KNACK",
    "SHOD", "SHOCK",
]

found_additional = set()
for word in additional:
    search_word = word.replace(" ", "")
    results = find_word(search_word)
    if results and word not in found_additional:
        found_additional.add(word)
        for r, c, direction, positions in results:
            print(f"  FOUND '{word}' at ({r},{c}) going {direction}, positions: {positions}")

# Let's also extract all possible words of length 3+ in all directions
print("\n=== ALL STRINGS OF LENGTH 3+ IN ALL DIRECTIONS ===\n")

all_strings = set()
for r in range(rows):
    for c in range(cols):
        if grid[r][c] is None:
            continue
        for dr, dc in directions:
            word = ""
            positions = []
            for k in range(max(rows, cols)):
                nr, nc = r + k*dr, c + k*dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc]:
                    word += grid[nr][nc]
                    positions.append((nr, nc))
                    if len(word) >= 3:
                        all_strings.add((word, tuple(positions)))
                else:
                    break

# Print all unique strings
sorted_strings = sorted(all_strings, key=lambda x: (len(x[0]), x[0]))
for s, pos in sorted_strings:
    if len(s) >= 3 and len(s) <= 12:
        print(f"  {s} : {list(pos)}")
