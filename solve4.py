#!/usr/bin/env python3
"""
Focus approach: Only show words that match with 0 or 1 wildcard positions.
Also, wildcards should only be at positions that are ACTUALLY dots in the grid.
"""

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

max_width = max(len(row) for row in grid)
for i in range(len(grid)):
    while len(grid[i]) < max_width:
        grid[i].append(None)

rows_count = len(grid)
cols_count = max_width

# Identify dot positions (these are the water droplet extraction positions)
dot_positions = set()
for r in range(rows_count):
    for c in range(cols_count):
        if grid[r][c] is None:
            dot_positions.add((r, c))

print(f"Grid: {rows_count} x {cols_count}")
print(f"Dot positions ({len(dot_positions)}): {sorted(dot_positions)}")
print(f"Letter positions: {rows_count * cols_count - len(dot_positions)}")

print("\nGrid:")
for i, row in enumerate(grid):
    display = [c if c else '·' for c in row]
    print(f"  {i}: {' '.join(display)}")

directions = [
    (0, 1, "R"), (0, -1, "L"),
    (1, 0, "D"), (-1, 0, "U"),
    (1, 1, "DR"), (1, -1, "DL"),
    (-1, 1, "UR"), (-1, -1, "UL"),
]

def find_word_flex(word, max_wildcards=1):
    """Find word, allowing up to max_wildcards dot positions to be filled."""
    results = []
    for r in range(rows_count):
        for c in range(cols_count):
            for dr, dc, dname in directions:
                found = True
                positions = []
                wc_count = 0
                for k, ch in enumerate(word.upper()):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows_count and 0 <= nc < cols_count:
                        cell = grid[nr][nc]
                        if cell == ch:
                            positions.append((nr, nc, ch, False))
                        elif cell is None:
                            # This is a dot position - could be a hidden letter
                            positions.append((nr, nc, ch, True))
                            wc_count += 1
                            if wc_count > max_wildcards:
                                found = False
                                break
                        else:
                            found = False
                            break
                    else:
                        found = False
                        break
                if found:
                    wc_list = [(p[0], p[1], p[2]) for p in positions if p[3]]
                    results.append((r, c, dname, positions, wc_list, wc_count))
    return results

# EXACT matches (0 wildcards)
print("\n=== EXACT MATCHES (no wildcards needed) ===\n")

candidates = [
    "MORAY", "TWO", "NEW", "PEN", "AWE", "OWN", "AID", "AIDA", "CON",
    "TEA", "VIC", "ORE", "ROE", "AND", "OAT", "NOW", "HUM", "DOT",
    "PEW", "PED", "RAY", "ORA", "MOR", "STI", "ION", "SIN", "PYT",
    "YOH", "HOY", "TRO", "ORT", "ORD", "LOT", "CAT", "TAC", "WIS",
    "OWE", "EWE", "OAR",
    # Longer words
    "MORAY", "NEWPEN", "AIDA", "CIVIN", "CIVIC",
    "PEDBN", "PEDBNS",
    "NEWPENAET",
    "PENA", "NAET",
]

for word in sorted(set(candidates)):
    results = find_word_flex(word, 0)
    if results:
        for r, c, dname, positions, wc, wc_count in results:
            pos_str = [(p[0], p[1]) for p in positions]
            print(f"  {word:15s} at ({r},{c}) {dname:3s}: {pos_str}")

# 1-wildcard matches for likely answers
print("\n=== 1-WILDCARD MATCHES ===\n")

candidates_1wc = [
    # Clue-specific candidates
    "TORNADO", "TWISTER", "TSUNAMI", "CYCLONE", "DROUGHT",
    "PIRATES", "PIRATE",
    "ROBINHOOD", "ROBIN", "HOOD",
    "HOORAY", "HURRAY",
    "IOWAN", "KANSAN", "DAKOTAN",
    "IRATE", "CROSS", "IRKED", "ANGRY",
    "HOODIE", "SHIRT", "CAP",
    "ACHOO", "SNEEZE", "CHATTER",
    "CORN", "RICE", "TACO", "STEW", "NORI",
    "VOILA", "DONE",
    "YOYO", "POPGUN", "TOPGUN",
    "PENNANT",
    "CIVIC", "TOWER",
    "TOWN", "CROWN",
    "IVORY",
    "ACORN", "SCONE",
    "TRIDENT",
    "SWORD",
    "NORTH",
    "NEWPENCE",
    "NEWPENNY",
    "WREN",
    "PEDCAR",
    "TROD", "TREK",
    "TWINE",
    "TWINS",
    "TRICK", "STICK",
    "KNIT", "KNOT",
    "INK",
    "SINK",
    "RINK",
    "WINK",
    "KINK",
    "CIVIC",
    "DAVID",
    "NAIAD",
    "DIVAN",
    "DRIVEN",
    "NOVICE",
    "NOTICE",
    "INVOICE",
    "ADVICE",
    "DEVICE",
    "OPTIC",
    "TOPIC",
    "ANTIC",
    "ORCAS",
    "CANOE",
]

for word in sorted(set(candidates_1wc)):
    results = find_word_flex(word, 1)
    if results:
        for r, c, dname, positions, wc, wc_count in results:
            if wc_count <= 1:
                pos_str = [(p[0], p[1]) for p in positions]
                wc_str = f" [hidden letter at {wc}]" if wc else ""
                print(f"  {word:15s} at ({r},{c}) {dname:3s}: {pos_str}{wc_str}")

# 2-wildcard matches for longer words
print("\n=== 2-WILDCARD MATCHES (longer words only, 6+ letters) ===\n")

candidates_2wc = [
    "TORNADO", "TWISTER", "TSUNAMI", "CYCLONE",
    "PIRATES", "ROBINHOOD",
    "HOORAY", "HURRAY",
    "IOWAN", "DAKOTAN",
    "HOODIE",
    "CHATTER",
    "PENNANT", "NEWPENCE", "NEWPENNY",
    "ACORN",
    "TRIDENT",
    "NOVICE", "NOTICE", "INVOICE", "ADVICE", "DEVICE",
    "TOWER", "TOWERS",
    "TROWEL",
    "DRIVEN",
    "CANOE",
    "PEDCAR", "PEDALCAR",
    "TOPKNOT",
]

for word in sorted(set(candidates_2wc)):
    if len(word) >= 6:
        results = find_word_flex(word, 2)
        if results:
            for r, c, dname, positions, wc, wc_count in results:
                if wc_count <= 2:
                    pos_str = [(p[0], p[1]) for p in positions]
                    wc_str = f" [hidden letters at {wc}]" if wc else ""
                    print(f"  {word:15s} at ({r},{c}) {dname:3s}: {pos_str}{wc_str}")
