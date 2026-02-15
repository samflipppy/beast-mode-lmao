#!/usr/bin/env python3
"""
Let me reconsider the grid. Maybe rows 3 and 7 are shifted, or maybe
the grid has a different structure than I assumed.

Key observation: Row 3 has 10 entries and row 7 has 10 entries,
while other rows have 8-9 entries. What if these extra-wide rows
indicate the grid is actually wider (like 10 cols) and some rows
are missing trailing cells?

OR: what if the original puzzle image has a shaped grid (not rectangular)?

Let me try yet another interpretation:
What if the grid is 9 columns wide, and rows 3 and 7 each have
a column shifted or there's a different alignment?

Actually, let me re-read the user's input MORE carefully:

Row 3: · · R T W O · · R R
That's: dot, dot, R, T, W, O, dot, dot, R, R = 10 items

Row 7: Y O H · K W C · S C
That's: Y, O, H, dot, K, W, C, dot, S, C = 10 items

All other rows have 8 or 9 items.

What if the LAST two items of rows 3 and 7 are actually in columns 8 and 9
(the 10th column)?

Let me also check: what if Rows 3 and 7 are wider because they have
an extra R and C respectively at the end, forming an irregular shape?

OR - maybe I should consider that rows 3 and 7 extend further right,
and rows with 9 columns might have an implicit dot at position 9.

Let me try yet another layout. What if column 9 exists for ALL rows,
but only has letters in some rows?

Row 0: M O R A Y · C O N [·]   <- col 9 implicit dot
Row 1: U A N L · C S T I [·]
Row 2: H D · O A I D A · [·]
Row 3: · · R T W O · · R R     <- col 9 = R
Row 4: N E W P E N A E T [·]
Row 5: · · C I V I N · [·] [·] <- extra dot at 8,9
Row 6: P E D B N S · C · [·]
Row 7: Y O H · K W C · S C     <- col 9 = C
Row 8: T R O R D K · S C [·]

Actually wait - row 8 has S C at the end (9 items), where col 7=S, col 8=C.
Row 7 has S C at the end too (10 items), where col 8=S, col 9=C.

So column alignment:
Col:  0 1 2 3 4 5 6 7 8 [9]
R0:   M O R A Y · C O N
R1:   U A N L · C S T I
R2:   H D · O A I D A ·
R3:   · · R T W O · · R  [R]
R4:   N E W P E N A E T
R5:   · · C I V I N ·
R6:   P E D B N S · C ·
R7:   Y O H · K W C · S  [C]
R8:   T R O R D K · S C

Hmm, that makes R3 col8=R, col9=R, and R7 col8=S, col9=C.
R8: col7=S, col8=C

So the S,C columns don't align between R7 and R8.
In R7: S is at col 8, C at col 9.
In R8: S is at col 7, C at col 8.

That seems odd for a word search. Unless the grid really IS ragged/shaped.

OK let me just try BOTH interpretations and see which gives more words.

Actually, let me try a completely different idea.
What if some of the rows have leading spaces/indentation that I'm not seeing?
What if rows 5 is actually:
  · · C I V I N · ·   (with an extra trailing dot)

making it 9 items, same as most rows?

And what if the grid is truly 9 columns, and rows 3 and 7 have 10 items because
they wrap or there's extra data?

Alternatively, what if I should ignore the trailing extra items?

Let me try a 9-col grid interpretation:
"""

# 9-column interpretation, take only first 9 items of each row:
raw_grid_9 = [
    "M O R A Y · C O N",       # 9
    "U A N L · C S T I",       # 9
    "H D · O A I D A ·",       # 9
    "· · R T W O · · R",       # 9 (drop trailing R)
    "N E W P E N A E T",       # 9
    "· · C I V I N · ·",       # 9 (add trailing dot)
    "P E D B N S · C ·",       # 9
    "Y O H · K W C · S",       # 9 (drop trailing C)
    "T R O R D K · S C",       # 9
]

grid9 = []
for row_str in raw_grid_9:
    cells = row_str.split()[:9]  # take only first 9
    row = []
    for c in cells:
        if c == '·':
            row.append(None)
        else:
            row.append(c)
    grid9.append(row)

# Ensure all rows are 9
for i in range(len(grid9)):
    while len(grid9[i]) < 9:
        grid9[i].append(None)

print("9-COLUMN GRID:")
for i, row in enumerate(grid9):
    display = [c if c else '·' for c in row]
    print(f"  {i}: {' '.join(display)}")

print()

# Now let me also try a 10-column grid
raw_grid_10 = [
    "M O R A Y · C O N ·",      # 10 (add trailing dot)
    "U A N L · C S T I ·",      # 10
    "H D · O A I D A · ·",      # 10
    "· · R T W O · · R R",      # 10
    "N E W P E N A E T ·",      # 10
    "· · C I V I N · · ·",      # 10
    "P E D B N S · C · ·",      # 10
    "Y O H · K W C · S C",     # 10
    "T R O R D K · S C ·",      # 10
]

grid10 = []
for row_str in raw_grid_10:
    cells = row_str.split()[:10]
    row = []
    for c in cells:
        if c == '·':
            row.append(None)
        else:
            row.append(c)
    grid10.append(row)

for i in range(len(grid10)):
    while len(grid10[i]) < 10:
        grid10[i].append(None)

print("10-COLUMN GRID:")
for i, row in enumerate(grid10):
    display = [c if c else '·' for c in row]
    print(f"  {i}: {' '.join(display)}")

# Now search BOTH grids for a comprehensive word list
directions = [
    (0, 1, "R"), (0, -1, "L"),
    (1, 0, "D"), (-1, 0, "U"),
    (1, 1, "DR"), (1, -1, "DL"),
    (-1, 1, "UR"), (-1, -1, "UL"),
]

def find_word_in_grid(grid, word):
    rows = len(grid)
    cols = len(grid[0])
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

# Comprehensive word list for the 9-column grid
import sys

# Load a dictionary
dict_words = set()
for dict_path in ['/usr/share/dict/words', '/usr/share/dict/american-english']:
    try:
        with open(dict_path) as f:
            for line in f:
                w = line.strip().upper()
                if 3 <= len(w) <= 10:
                    dict_words.add(w)
    except FileNotFoundError:
        pass

print(f"\nDictionary size: {len(dict_words)} words (3-10 chars)")

# Search 9-column grid
print("\n=== 9-COLUMN GRID: ALL DICTIONARY WORDS FOUND ===\n")
found_9 = {}
for word in sorted(dict_words):
    results = find_word_in_grid(grid9, word)
    if results:
        found_9[word] = results

for word in sorted(found_9.keys(), key=lambda w: (-len(w), w)):
    for r, c, dname, positions in found_9[word]:
        print(f"  {word:15s} at ({r},{c}) {dname:3s}: {positions}")

print(f"\nTotal words found in 9-col grid: {len(found_9)}")
print(f"Words: {sorted(found_9.keys())}")

# Search 10-column grid
print("\n=== 10-COLUMN GRID: ALL DICTIONARY WORDS FOUND ===\n")
found_10 = {}
for word in sorted(dict_words):
    results = find_word_in_grid(grid10, word)
    if results:
        found_10[word] = results

for word in sorted(found_10.keys(), key=lambda w: (-len(w), w)):
    for r, c, dname, positions in found_10[word]:
        print(f"  {word:15s} at ({r},{c}) {dname:3s}: {positions}")

print(f"\nTotal words found in 10-col grid: {len(found_10)}")
print(f"Words: {sorted(found_10.keys())}")

# Differences
only_in_10 = set(found_10.keys()) - set(found_9.keys())
only_in_9 = set(found_9.keys()) - set(found_10.keys())
print(f"\nOnly in 10-col: {sorted(only_in_10)}")
print(f"Only in 9-col: {sorted(only_in_9)}")
