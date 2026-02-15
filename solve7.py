#!/usr/bin/env python3
"""
Manual reasoning approach. Let me carefully look at what words CAN be formed
in each direction and try to match them to clues.

The grid (9-col):
     0 1 2 3 4 5 6 7 8
  0: M O R A Y · C O N
  1: U A N L · C S T I
  2: H D · O A I D A ·
  3: · · R T W O · · R
  4: N E W P E N A E T
  5: · · C I V I N · ·
  6: P E D B N S · C ·
  7: Y O H · K W C · S
  8: T R O R D K · S C

Key observations:
1. MORAY is clearly in row 0 going right
2. TWO is in row 3
3. NEWPEN spans row 4 (cols 0-5)
4. AIDA spans row 2 (cols 4-7)

But wait - for a word search puzzle, the answers need to be longer,
more interesting words. Let me think about what 12 words could all fit.

Let me trace longer paths more carefully.

Actually, let me reconsider. Maybe the grid as presented is CORRECT
and the words DO use the dot positions (water droplets mark those letters
for extraction later). In that case, dots are truly empty, and the
answers are shorter words.

OR - more likely - I'm misreading the grid. Let me look at this from
a completely different angle. Maybe the "·" characters are NOT dots
at all, but represent a specific letter or are just spacing artifacts.

Let me focus on what we KNOW:
- This is a word search
- There are 12 clues
- After finding all words, leftover/marked letters spell an answer
- The answer is one of: EVERY, TOWARDS, LOCATION, NAME, SOMEWHERE, AROUND, WORLD

Let me now think about each clue with fresh eyes and the actual grid.

Actually, I just realized something. The user said this is "Puzzle 1",
but based on my research, this might actually be "Puzzle 2" (I Built 100 Wells).
The meta-clue word for puzzle 2 (5 letters based on the structure) would be
one of: EVERY(5), LEADS(5), WORLD(5).

But more importantly for THIS puzzle, the answer should be a LOCATION
(based on the meta clue "EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD").

Wait, actually the 9 puzzles give 9 words of lengths: 5, 9, 5, 7, 8, 4, 9, 6, 5.
If this is puzzle 1, the word would be 5 letters = EVERY.
If this is puzzle 2, it would be 9 letters = CHALLENGE.

Hmm, the user said "Puzzle 1" and listed possible answers including
EVERY (5), TOWARDS (7), LOCATION (8), NAME (4), SOMEWHERE (9), AROUND (6), WORLD (5).

Let me now try to re-examine the grid with a focus on shorter words
that match the clues.

12 clues with likely short answers that ARE in this small grid:
"""

# The actual grid
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

rows = len(grid)
cols = len(grid[0])

directions = [
    (0, 1, "R"), (0, -1, "L"),
    (1, 0, "D"), (-1, 0, "U"),
    (1, 1, "DR"), (1, -1, "DL"),
    (-1, 1, "UR"), (-1, -1, "UL"),
]

def extract_string(r, c, dr, dc, length):
    """Extract a string starting from (r,c) in direction (dr,dc) for given length."""
    result = []
    positions = []
    for k in range(length):
        nr, nc = r + k*dr, c + k*dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc]:
                result.append(grid[nr][nc])
                positions.append((nr, nc))
            else:
                return None, None  # Hit a None
        else:
            return None, None  # Out of bounds
    return ''.join(result), positions

# Extract ALL possible strings of length 3-9 in all directions
print("=== ALL POSSIBLE STRINGS IN GRID (length 3-9) ===\n")

all_strings = {}
for r in range(rows):
    for c in range(cols):
        if grid[r][c] is None:
            continue
        for dr, dc, dname in directions:
            for length in range(3, 10):
                s, pos = extract_string(r, c, dr, dc, length)
                if s:
                    if s not in all_strings:
                        all_strings[s] = []
                    all_strings[s].append((r, c, dname, pos))

# Print strings sorted by length (longest first), only length 4+
print("Strings of length 4+:")
for s in sorted(all_strings.keys(), key=lambda x: (-len(x), x)):
    if len(s) >= 4:
        first = all_strings[s][0]
        r, c, dname, pos = first
        print(f"  {s:20s} ({len(s)}) at ({r},{c}) {dname}")

# Now let me manually analyze clues:
print("\n\n=== CLUE ANALYSIS ===\n")

# Let me check specific sequences that could be answers:
#
# Clue 1: "A cold noise?"
# - Could be ACHOO (having a cold -> sneezing)
# - Looking for A-C-H-O-O in the grid
# - A(0,3) -> C? A(0,3) neighbors: O(0,2), Y(0,4), N(1,2), L(1,3), None(0,5), None(1,4)
#   No C adjacent to A(0,3).
# - A(2,4) -> C(1,5)? Yes, UL... no, (2,4) to (1,5) is (-1,+1) = UR.
#   A(2,4) -> C(1,5) via UR. Then H? (0,6)=C, not H.
# - A(2,7) -> C? neighbors of (2,7): D(2,6), None(2,8), None(3,7), None(3,8), I(1,8), T(1,7), A(2,7)
#   No C adjacent.
# - A(4,6) -> C? neighbors: N(4,5), E(4,7), I(5,5), N(5,6), S(6,5), None(5,7), None(3,6)
#   No C adjacent.
#
# ACHOO doesn't seem to work. What about SNAP?
# S(1,6) N(1,2)? Not adjacent. S(6,5) N(6,4)? Yes! Left.
# S(6,5) N(6,4) A? neighbors of N(6,4): B(6,3), S(6,5), I(5,3), V(5,4), K(7,4), W(7,5)
#   No A adjacent.
# S(7,8) N? neighbors: C(8,8), None(6,8), C(7,6), W(7,5), K(8,5)? No N adjacent.
#
# Let me try ICE: I(1,8) C(7,6)? Not adjacent.
# I(2,5) C(1,5)? Yes, up! E? (0,5)=None.
#
# What about CHATTER? C-H-A-T-T-E-R
# C(0,6) H? None adjacent. C(1,5) H? None adjacent.
# C(7,6) H? No... (7,6) neighbors: W(7,5), None(7,7), S(6,5)?, K(8,5)?
#   Actually C(7,6) neighbors: (6,5)S, (6,6)None, (6,7)C, (7,5)W, (7,7)None, (8,5)K, (8,6)None, (8,7)S
#   No H adjacent.
#
# Hmm. Let me think differently. What if "cold noise" is MOAN?
# M(0,0) O(0,1) A(1,1) N(1,2)?
# M->O is right. O(0,1) -> A(1,1)? (0,1) to (1,1) is down. A(1,1)->N(1,2)? right.
# Not a straight line (changes direction). Word search needs straight lines.
#
# What about the answer being embedded across dots?
# Maybe the grid truly has letters where dots are, and we need those to complete words.

# Let me try something: what if I look at the shape of the grid differently?
# In the original puzzle image, maybe some rows are offset (like a hex grid)
# or the grid is shaped like a water droplet.

# For now, let me list all strings that are actual words:
from english_words import get_english_words_set
words_set = set()
for w in get_english_words_set(['web2'], lower=True, alpha=True):
    if 3 <= len(w) <= 12:
        words_set.add(w.upper())

# Add common words that might not be in web2
extra = ["MORAY","TEA","AWE","CON","AID","PEN","NEW","TWO","PED","RAY","OWN",
         "ION","SIN","LOT","DOT","HUM","ORE","ROE","HOY","VIC","WEN","WIN","WON",
         "YAR","CAT","AND","NOW","DIE","DOE","ITS","TOD","ORT","LAO","NAE","NEP",
         "SAR","RHE","WIS","RAH","RAS","EAN","ENS","IAO","IDA","IDO","INO","ISO",
         "ALO","ARO","DAO","MOR","TOL","MORAY","AIDA","CION","IONI","IVIN","MORA","TEAN"]
for w in extra:
    words_set.add(w.upper())

print("Looking for real words in all extracted strings:")
real_words_found = {}
for s in all_strings:
    if s in words_set:
        real_words_found[s] = all_strings[s]

for word in sorted(real_words_found.keys(), key=lambda w: (-len(w), w)):
    entries = real_words_found[word]
    for r, c, dname, pos in entries:
        print(f"  {word:15s} ({len(word)}) at ({r},{c}) {dname:3s} {pos}")

print(f"\nAll real words found: {sorted(real_words_found.keys())}")

# Count how many cells each word uses
used_cells = set()
for word, entries in real_words_found.items():
    for r, c, dname, pos in entries:
        for p in pos:
            used_cells.add(p)

print(f"\nCells used by at least one real word: {len(used_cells)}")
total_letter_cells = sum(1 for r in range(rows) for c in range(cols) if grid[r][c])
print(f"Total letter cells: {total_letter_cells}")
print(f"Unused cells: {total_letter_cells - len(used_cells)}")

# Show unused cells
all_letter_cells = set()
for r in range(rows):
    for c in range(cols):
        if grid[r][c]:
            all_letter_cells.add((r, c))

unused = all_letter_cells - used_cells
print(f"Unused letter positions: {sorted(unused)}")
for r, c in sorted(unused):
    print(f"  ({r},{c}) = {grid[r][c]}")
