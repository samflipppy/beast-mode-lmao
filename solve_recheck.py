#!/usr/bin/env python3
"""
Let me reconsider: maybe the grid rows that have 10 entries really ARE 10 columns.
And the 8-entry row (row 5) is also 10 columns with trailing dots.
Maybe ALL rows are 10 columns.

Original user input:
Row 0: M O R A Y · C O N           = 9 entries
Row 1: U A N L · C S T I           = 9 entries
Row 2: H D · O A I D A ·           = 9 entries
Row 3: · · R T W O · · R R         = 10 entries
Row 4: N E W P E N A E T           = 9 entries
Row 5: · · C I V I N ·             = 8 entries
Row 6: P E D B N S · C ·           = 9 entries
Row 7: Y O H · K W C · S C        = 10 entries
Row 8: T R O R D K · S C           = 9 entries

If the grid is 10 columns wide:
Row 0: M O R A Y · C O N ·        (col 9 = dot)
Row 1: U A N L · C S T I ·        (col 9 = dot)
Row 2: H D · O A I D A · ·        (col 9 = dot)
Row 3: · · R T W O · · R R        (col 9 = R)
Row 4: N E W P E N A E T ·        (col 9 = dot)
Row 5: · · C I V I N · · ·        (cols 8,9 = dot)
Row 6: P E D B N S · C · ·        (col 9 = dot)
Row 7: Y O H · K W C · S C        (col 8=S, col 9=C)
Row 8: T R O R D K · S C ·        (col 8=C, col 9 = dot)

Hmm, in row 8 with 10 cols: col 7=S, col 8=C, col 9=dot
In row 7 with 10 cols: col 7=dot, col 8=S, col 9=C

That means S aligns at col 8 in both rows 7 and 8, and C at col 9 in row 7
and col 8 in row 8. These DON'T align vertically for word search purposes.

WAIT. Maybe I should look at this differently. What if the grid is NOT
space-separated single characters, but has some multi-char cells?

Actually, let me look at the user's EXACT formatting more carefully:
"· · R T W O · · R R"

Between items there are spaces. Each item is either a letter or ·.
This line has 10 items: ·, ·, R, T, W, O, ·, ·, R, R

"· · C I V I N ·"
This has 8 items: ·, ·, C, I, V, I, N, ·

For a 10-col grid, row 5 would need 2 more trailing dots.
For a 9-col grid, row 3 has 1 extra item and row 7 has 1 extra item.

What if the grid has variable width? Like a shaped grid?
Or what if I'm miscounting?

Let me consider: what if in the original puzzle, there IS NO space between
the last R and R in row 3? What if "R R" is actually two separate letters
in two columns? Or what if there are additional hidden columns?

You know what, let me just try EVERY possible word in a 10x10 grid version
where I fill in all the dots as wildcards, to see what could possibly work.

Actually, a better idea: let me write code that tries to place each target word
in EVERY possible position and direction in a 9-COLUMN grid where None cells
can be ANY letter. The key: the search should be completely unconstrained
for None cells.
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
                mismatches = 0
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
                            mismatches += 1
                            ok = False
                            break
                    else:
                        ok = False
                        break
                if ok:
                    results.append((dname, wc, len(word) - wc, ' '.join(info)))
    return results

# Test with key words - show results sorted by fewest wildcards
words = [
    'TORNADO', 'TWISTER', 'TSUNAMI', 'CYCLONE', 'TYPHOON', 'FLOOD',
    'EARTHQUAKE', 'BLIZZARD', 'DROUGHT', 'AVALANCHE', 'STORM', 'TEMPEST',
    'PIRATES', 'PIRATE', 'ECU',
    'ROBIN', 'HOOD', 'ROBINHOOD',
    'HOORAY', 'HURRAY', 'WAHOO', 'EUREKA', 'VOILA',
    'IOWAN', 'HOOSIER', 'KANSAN', 'OHIOAN', 'DAKOTAN',
    'IRATE', 'UPSET', 'ANGRY', 'CROSS', 'IRKED', 'LIVID', 'PEEVED',
    'HOODIE', 'SHIRT', 'TSHIRT', 'CAP', 'HAT', 'BEANIE',
    'ACHOO', 'SHIVER', 'CHATTER', 'BRRR',
    'YOYO', 'POPGUN', 'TOPKNOT', 'SEESAW',
    'CORN', 'TACO', 'STEW', 'NORI', 'RICE', 'BREAD',
    'PENNANT', 'TOWER', 'CIVIC', 'SWORD',
    'OLDNORTH', 'ROBROY',
    'NEWPENNY', 'PEDCAR',
    'JACKKNIFE', 'RAYGUN',
    # What if answers are shorter?
    'COLD', 'ICE', 'SNOW',
    'WAVE', 'GALE', 'WIND',
    'DROWN', 'SLIDE',
    'PIE', 'OAT', 'TEA', 'HAM', 'YAM',
    'MAD', 'IRE', 'VEX',
    'PEG', 'TOP', 'CAR',
]

print("=== WORD SEARCH RESULTS ===\n")
for w in sorted(set(words)):
    results = find_any(w)
    if results:
        # Sort by wildcards (fewest first)
        results.sort(key=lambda x: x[1])
        best = results[0]
        dname, wc, matched, info = best
        pct = matched / len(w) * 100
        if wc <= len(w) // 2:  # At most half wildcards
            print(f"  {w:15s} {dname:3s} wc={wc}/{len(w)} ({pct:.0f}% matched): {info}")
            if len(results) > 1 and results[1][1] == wc:
                # Show other equally good matches
                for r2 in results[1:3]:
                    print(f"  {'':15s} {r2[0]:3s} wc={r2[1]}/{len(w)}: {r2[3]}")

print("\n\n=== NOW CHECKING: What if the grid layout is completely different? ===")
print("Let me see all LONG strings (7+) that CAN be formed with wildcards:\n")

for r in range(rows):
    for c in range(cols):
        for dr, dc, dname in dirs:
            word = []
            wildcard_count = 0
            positions = []
            for k in range(9):
                nr, nc = r + k*dr, c + k*dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    cell = grid[nr][nc]
                    if cell:
                        word.append(cell)
                    else:
                        word.append('_')
                        wildcard_count += 1
                    positions.append((nr, nc))
                else:
                    break
            s = ''.join(word)
            if len(s) >= 7 and wildcard_count <= 2:
                print(f"  ({r},{c}) {dname}: {s}  (wc={wildcard_count})")
