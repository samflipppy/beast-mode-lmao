#!/usr/bin/env python3
"""
Use the english_words package to search for real words in the grid.
"""
from english_words import get_english_words_set

# Get English words, 3-12 chars
all_words = set()
for w in get_english_words_set(['web2'], lower=True, alpha=True):
    w_upper = w.upper()
    if 3 <= len(w_upper) <= 12 and w_upper.isalpha():
        all_words.add(w_upper)

# Also add specific candidates
specific = [
    "MORAY", "TORNADO", "PIRATES", "PIRATE", "ROBIN", "HOOD", "ROBINHOOD",
    "HOORAY", "HURRAY", "IOWAN", "KANSAN", "DAKOTAN", "OHIOAN",
    "IRATE", "HOODIE", "ACHOO", "CORN", "RICE", "TACO", "STEW", "NORI",
    "YOYO", "POPGUN", "PENNANT", "CIVIC", "TOWER", "IVORY", "ACORN",
    "NEWPENCE", "WREN", "TWINE", "SWORD", "NORTH", "PIRANHA",
    "PEDCAR", "PEDALCAR", "TOPKNOT", "PEDAL", "SEESAW",
    "HOOPLA", "TINCAN",
    "ECU", "TEA", "PEW", "OAT", "AWE", "ORE", "ROE",
    "AIDA", "CAP", "HAT", "TEE", "MUG",
    "OLDNORTH", "PENNSTATION",
    "HOTROD",
    # Words with K
    "KAYAK", "KIOSK",
]
for w in specific:
    all_words.add(w.upper())

print(f"Total dictionary: {len(all_words)} words")

# Grid (9 columns, dropping extras from rows 3 and 7)
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

def find_word(word):
    results = []
    for r in range(rows):
        for c in range(cols):
            for dr, dc, dname in directions:
                found = True
                positions = []
                for k, ch in enumerate(word):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == ch:
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

# First, determine which letters are in the grid
grid_letters = set()
for r in range(rows):
    for c in range(cols):
        if grid[r][c]:
            grid_letters.add(grid[r][c])

print(f"Letters in grid: {sorted(grid_letters)}")

# Filter words to only those whose letters are all in the grid
from collections import Counter
grid_letter_counts = Counter()
for r in range(rows):
    for c in range(cols):
        if grid[r][c]:
            grid_letter_counts[grid[r][c]] += 1

print(f"Letter counts: {dict(sorted(grid_letter_counts.items()))}")

# Search for all words
found = {}
for word in all_words:
    # Quick filter: all letters must be in grid
    if all(ch in grid_letters for ch in word):
        results = find_word(word)
        if results:
            found[word] = results

print(f"\n=== ALL ENGLISH WORDS FOUND IN GRID ===")
print(f"Total: {len(found)}\n")

for word in sorted(found.keys(), key=lambda w: (-len(w), w)):
    for r, c, dname, positions in found[word]:
        print(f"  {word:15s} at ({r},{c}) {dname:3s}  pos={positions}")

# Now let's also try the 10-column grid for rows 3 and 7
print("\n\n=== NOW TRYING WITH 10 COLUMNS (full rows 3 and 7) ===\n")

grid10 = [
    ['M','O','R','A','Y', None,'C','O','N', None],
    ['U','A','N','L', None,'C','S','T','I', None],
    ['H','D', None,'O','A','I','D','A', None, None],
    [None, None,'R','T','W','O', None, None,'R','R'],
    ['N','E','W','P','E','N','A','E','T', None],
    [None, None,'C','I','V','I','N', None, None, None],
    ['P','E','D','B','N','S', None,'C', None, None],
    ['Y','O','H', None,'K','W','C', None,'S','C'],
    ['T','R','O','R','D','K', None,'S','C', None],
]

rows10 = len(grid10)
cols10 = len(grid10[0])

def find_word10(word):
    results = []
    for r in range(rows10):
        for c in range(cols10):
            for dr, dc, dname in directions:
                found = True
                positions = []
                for k, ch in enumerate(word):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows10 and 0 <= nc < cols10:
                        if grid10[nr][nc] == ch:
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

found10 = {}
for word in all_words:
    if all(ch in grid_letters for ch in word):
        results = find_word10(word)
        if results:
            found10[word] = results

# Only show words found in 10-col but not 9-col
new_words = set(found10.keys()) - set(found.keys())
if new_words:
    print("Additional words found only in 10-col grid:")
    for word in sorted(new_words, key=lambda w: (-len(w), w)):
        for r, c, dname, positions in found10[word]:
            print(f"  {word:15s} at ({r},{c}) {dname:3s}  pos={positions}")
else:
    print("No additional words found in 10-col grid.")
