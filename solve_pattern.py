#!/usr/bin/env python3
"""
Pattern matching approach: For each long string extracted from the grid,
check if filling in the wildcards (_) could produce a real English word.
"""

from english_words import get_english_words_set
import re

# Get word list
all_words = set()
for w in get_english_words_set(['web2'], lower=True, alpha=True):
    w_upper = w.upper()
    if 3 <= len(w_upper) <= 12 and w_upper.isalpha():
        all_words.add(w_upper)

# Add additional specific words
for w in ["MORAY","TORNADO","PIRATES","PIRATE","ROBIN","HOOD","ROBINHOOD",
          "HOORAY","HURRAY","IOWAN","HOOSIER","KANSAN","OHIOAN","DAKOTAN",
          "IRATE","HOODIE","TSHIRT","ACHOO","YOYO","CORN","TACO","STEW",
          "NORI","PENNANT","TOWER","CIVIC","SWORD","PEDCAR","TOPKNOT",
          "SEESAW","TYPHOON","CYCLONE","ROBROY","OLDNORTH","NEWPENNY",
          "RAYGUN","POPGUN","JACKKNIFE","PENKNIFE","PEDALCAR",
          "WAHOO","EUREKA","VOILA","BRAVO","YAHOO","HUZZAH",
          "TROWEL","PEWTER","BOWIE","REVOLVER",
          "SNOWSTORM","BLIZZARD","MUDSLIDE","WILDFIRE",
          "TEE","HAT","CAP","MUG","SHIRT","SHORTS","PANTS","SOCKS",
          "ORCAS","WHALES"]:
    all_words.add(w)

print(f"Dictionary size: {len(all_words)}")

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

# Extract all strings of length 3-9 with their wildcard pattern
def extract_all():
    strings = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] is None:
                continue  # Don't start from wildcard
            for dr, dc, dname in dirs:
                for length in range(3, 10):
                    word = []
                    pattern = []
                    positions = []
                    wc_count = 0
                    valid = True
                    for k in range(length):
                        nr, nc = r + k*dr, c + k*dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            cell = grid[nr][nc]
                            if cell:
                                word.append(cell)
                                pattern.append(cell)
                            else:
                                word.append('_')
                                pattern.append('.')  # regex wildcard
                                wc_count += 1
                            positions.append((nr, nc))
                        else:
                            valid = False
                            break
                    if valid and wc_count > 0 and wc_count <= 3:
                        s = ''.join(word)
                        p = ''.join(pattern)
                        strings.append((s, p, r, c, dname, positions, wc_count))
    return strings

all_strings = extract_all()
print(f"Total strings with wildcards: {len(all_strings)}")

# For each string with wildcards, check if any dictionary word matches the pattern
print("\n=== PATTERN MATCHES ===\n")

# Build a length-indexed dict
words_by_length = {}
for w in all_words:
    l = len(w)
    if l not in words_by_length:
        words_by_length[l] = []
    words_by_length[l].append(w)

matches_found = []
for s, p, r, c, dname, positions, wc_count in all_strings:
    length = len(s)
    if length in words_by_length:
        regex = re.compile('^' + p + '$')
        for w in words_by_length[length]:
            if regex.match(w):
                matches_found.append((w, s, p, r, c, dname, positions, wc_count))

# Sort by length (longest first) then by wildcards (fewest first)
matches_found.sort(key=lambda x: (-len(x[0]), x[7]))

# De-duplicate
seen = set()
for w, s, p, r, c, dname, positions, wc_count in matches_found:
    key = (w, r, c, dname)
    if key in seen:
        continue
    seen.add(key)
    # Only show words with <= 2 wildcards for length <= 5,
    # or <= 3 wildcards for length 6+
    max_wc = 2 if len(w) <= 5 else 3
    if wc_count <= max_wc:
        pct = (len(w) - wc_count) / len(w) * 100
        # Format positions with wildcards highlighted
        pos_str = []
        for i, (pr, pc) in enumerate(positions):
            if grid[pr][pc]:
                pos_str.append(f"{grid[pr][pc]}({pr},{pc})")
            else:
                pos_str.append(f"[{w[i]}]({pr},{pc})")
        print(f"  {w:15s} len={len(w)} wc={wc_count} {pct:.0f}% at ({r},{c}) {dname}: {' '.join(pos_str)}")
