#!/usr/bin/env python3
"""
Re-approach: The dots in the grid likely represent positions where there ARE letters
but they're marked with water droplets. The user may have transcribed the grid
incorrectly by putting dots where they couldn't see the letters clearly, or the
dots represent a special marking.

Let me assume the grid IS fully filled and the dots represent unknown letters.
I'll try to figure out what those letters are based on the clue answers.

Grid with ? for unknown positions:
Row 0: M O R A Y ? C O N
Row 1: U A N L ? C S T I
Row 2: H D ? O A I D A ?
Row 3: ? ? R T W O ? ? R R
Row 4: N E W P E N A E T
Row 5: ? ? C I V I N ?
Row 6: P E D B N S ? C ?
Row 7: Y O H ? K W C ? S C
Row 8: T R O R D K ? S C

Unknown positions (row, col):
(0,5), (1,4), (2,2), (2,8), (3,0), (3,1), (3,6), (3,7),
(5,0), (5,1), (5,7), (6,6), (6,8), (7,3), (7,7), (8,6)

That's 16 unknown positions. Wait, the grid is not rectangular.
Let me reconsider the column alignment.

Actually, looking at the grid dimensions again:
Row 0: 9 cells (with dot at pos 5)
Row 1: 9 cells (with dot at pos 4)
Row 2: 9 cells (with dots at pos 2, 8)
Row 3: 10 cells (with dots at pos 0, 1, 6, 7)
Row 4: 9 cells (no dots)
Row 5: 8 cells (with dots at pos 0, 1, 7) -- WAIT this is only 8 cells
Row 6: 9 cells (with dots at pos 6, 8)
Row 7: 10 cells (with dots at pos 3, 7)
Row 8: 9 cells (with dot at pos 6)

The rows are different lengths! Maybe rows 3 and 7 have 10 columns because
of an extra column at the right. Or maybe the grid is actually 10 columns
and some cells at the right are just blank (not part of grid).

Let me try a 9-column interpretation where rows 3, 7, 8 are also 9 columns:
Hmm, row 3 has: · · R T W O · · R R = 10 items
Row 7: Y O H · K W C · S C = 10 items

Actually you know what, maybe the grid is RAGGED -- shaped like Africa or a water droplet!
That's a common puzzle design. Let me look at this differently.

Wait -- maybe I should try a completely different grid interpretation. What if:
- Row 5 has a trailing dot I'm missing (making it 9)
- Rows 3 and 7 having 10 is correct

OR maybe the grid columns shift. Let me try to see if there's a pattern:

Maybe this is a hex grid or some other unusual layout. But word searches are
typically rectangular.

Let me try the simplest approach: treat the whole thing as a 9-column grid,
where row 3 wraps or has an error. But the user explicitly wrote 10 items for row 3.

Actually let me re-read the user's post:
```
· · R T W O · · R R
```
That's indeed 10 items. And:
```
Y O H · K W C · S C
```
Also 10 items. And row 5:
```
· · C I V I N ·
```
That's 8 items. Hmm.

And row 8:
```
T R O R D K · S C
```
That's 9 items.

OK wait -- maybe the user made transcription errors. Let me try to work with
what I have and be flexible about the grid dimensions.

Actually, you know what, let me try a different approach entirely.
Let me forget about the exact grid positions for a moment and just look at
what letters are available in the grid, and think about what words could be
formed from those letters.

Letters in the grid:
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

all_letters = []
for row_str in raw_grid:
    cells = row_str.split()
    for c in cells:
        if c != '·':
            all_letters.append(c)

from collections import Counter
letter_counts = Counter(all_letters)
print("Letter frequency:")
for letter, count in sorted(letter_counts.items()):
    print(f"  {letter}: {count}")
print(f"\nTotal letters: {sum(letter_counts.values())}")
print(f"Available letters: {''.join(sorted(all_letters))}")

# Now let me think about each clue and what answer COULD be formed from these letters
# and would make sense:

print("\n\n=== CLUE ANALYSIS ===\n")

clues = [
    ("1. 'A cold noise?'", "Wordplay: cold=having a cold, noise=sound. ACHOO? SNEEZE? COUGH? Or: cold temperature noise = BRRR, CHATTER. Letters available suggest CHATTER is unlikely (no H near right letters). Wait, H is in grid. Actually ACHOO: A,C,H,O,O - all in grid!"),
    ("2. 'A natural disaster'", "TORNADO needs T,O,R,N,A,D,O - all available! TWO is in grid, TROD is partially there. Could be DROUGHT? D,R,O,U,G,H,T - no G in grid. FLOOD? No F. TSUNAMI? No second letter issues."),
    ("3. 'MrBeast went to see in Greenville, NC'", "ECU Pirates! PIRATES = P,I,R,A,T,E,S - all in grid!"),
    ("4. 'Nats' (2 wds)", "Anagram of NATS = ANTS, TANS. Or 'two nats' = TWO NATS? Or wordplay."),
    ("5. 'A certain Midwesterner'", "IOWAN = I,O,W,A,N - all in grid! Or DAKOTAN? D,A,K,O,T,A,N - all in grid!"),
    ("6. 'A child's toy (2 wds, hyph.)'", "YO-YO = Y,O,Y,O - only one Y... POP-GUN - no G. What about TOP-KNOT? Not a toy. JACK-IN-BOX? No J. PED-I-CAR?"),
    ("7. 'Upset'", "IRATE = I,R,A,T,E - all available! Or CROSS, IRKED, etc."),
    ("8. 'An item you can buy in MrBeast's store'", "HOODIE = H,O,O,D,I,E - all available! Or HAT, CAP, SHIRT, TEE."),
    ("9. 'A US landmark (2 wds.)'", "Need to think of landmarks... TWIN PEAKS? No, that's not really a landmark. OLD NORTH? MOUNT... no second T... PENN... NEW PENN???"),
    ("10. 'A type of food'", "CORN, RICE, TACO, PIE, OAT, TEA (drink not food), STEW, NORI (seaweed). CORN = C,O,R,N all in grid."),
    ("11. 'A literary outlaw (2 wds.)'", "ROBIN HOOD = R,O,B,I,N + H,O,O,D - all letters available!"),
    ("12. 'What you might say when you finish this!'", "HOORAY, DONE, VOILA. HOORAY = H,O,O,R,A,Y - all in grid! Or DONE = D,O,N,E."),
]

for clue, analysis in clues:
    print(f"{clue}")
    print(f"  Analysis: {analysis}")
    print()

# Now let me search the grid for these specific candidates,
# treating dots as unknown/wildcard positions

grid = []
for row_str in raw_grid:
    cells = row_str.split()
    row = []
    for c in cells:
        if c == '·':
            row.append('?')  # unknown
        else:
            row.append(c)
    grid.append(row)

max_width = max(len(row) for row in grid)
for i in range(len(grid)):
    while len(grid[i]) < max_width:
        grid[i].append('?')

rows_count = len(grid)
cols_count = max_width

print(f"\nGrid dimensions: {rows_count} x {cols_count}")
print("Grid with unknowns:")
for i, row in enumerate(grid):
    print(f"  {i}: {' '.join(row)}")

# Search allowing wildcards (?) to match any letter
directions = [
    (0, 1, "right"), (0, -1, "left"),
    (1, 0, "down"), (-1, 0, "up"),
    (1, 1, "DR"), (1, -1, "DL"),
    (-1, 1, "UR"), (-1, -1, "UL"),
]

def find_word_with_wildcards(word):
    """Find word allowing ? cells to match any letter."""
    results = []
    for r in range(rows_count):
        for c in range(cols_count):
            for dr, dc, dname in directions:
                found = True
                positions = []
                wildcards = []
                for k, ch in enumerate(word.upper()):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows_count and 0 <= nc < cols_count:
                        cell = grid[nr][nc]
                        if cell == ch:
                            positions.append((nr, nc, ch, False))
                        elif cell == '?':
                            positions.append((nr, nc, ch, True))
                            wildcards.append((nr, nc, ch))
                        else:
                            found = False
                            break
                    else:
                        found = False
                        break
                if found:
                    results.append((r, c, dname, positions, wildcards))
    return results

# Search for key candidates
key_words = [
    "TORNADO", "TWISTER", "TSUNAMI", "CYCLONE", "AVALANCHE", "DROUGHT",
    "PIRATES", "PIRATE", "ECU",
    "ROBINHOOD", "ROBIN", "HOOD",
    "HOORAY", "HURRAY", "HOOEY",
    "IOWAN", "OHIOAN", "KANSAN", "DAKOTAN",
    "IRATE", "CROSS", "IRKED",
    "HOODIE", "SHIRT", "HAT", "CAP", "TEE",
    "ACHOO", "BRRR", "SNEEZE", "CHATTER",
    "CORN", "RICE", "TACO", "STEW", "NORI", "OAT", "BREAD",
    "MORAY", "VOILA", "DONE", "EUREKA",
    "YOYO",
    "PENNANT", "OLDNORTH",
    "CIVIC",
    "TWIN", "TWINS",
    "TOWER",
    "PEDAL", "PEDALCAR",
    "IVORY", "DAVID",
    "DROIT", "ADROIT",
    "PENWIPER",
    "NEWPENCE",
    "DICKENS",
    "ANET",
    "TOWN", "NEWTON",
    "ACORN",
    "UNICORN",
    "ICON",
    "OWNTWO",  # "own two" as in "on your own two feet"?
    "TWOPENCE",
    "TROWEL",
    "PEWIT",
    "SOVIET",
    "NOVICE",
    "ADVICE",
    "DEVICE",
    "INVOICE",
    "NAIAD",
    "WADI",
    "TRIDENT",
    "PRESIDENT",
    "INCIDENT",
    "ACCIDENT",
    "EVIDENT",
    "RESIDENT",
    "ANCIENT",
    "PATIENT",
    "ORIENT",
    "OPTIC",
    "TOPIC",
    "TROPIC",
    "NORDICK",
    "TONIC",
    "SONIC",
    "IRONIC",
    "CHRONIC",
    "NEWPENN",
    "NEWPORT",
    "PENSION",
    "VINTAGE",
    "NATIVE",
    "RAVEN",
    "HAVEN",
    "HEAVEN",
    "DRIVEN",
    "WOVEN",
    "OVEN",
    "SEVEN",
    "PROVEN",
    "ROWAN",
    "COWAN",
    "DIWAN",
    "DIVAN",
    "CROTCHET",
    "ROCKET",
    "SOCKET",
    "POCKET",
    "CRICKET",
    "WICKET",
    "TICKET",
    "BASKET",
    "CASKET",
    "BONNET",
    "HORNET",
    "CORNET",
    "SONNET",
    "CARROT",
    "PARROT",
    "SWORD",
    "WORDS",
    "TROPIC",
    "NORDICK",
    "ANTIC",
    # Let me think about ROBIN HOOD more carefully.
    # If we allow wildcards, maybe it goes through dot positions.
    # The ? positions might reveal the hidden answer word.
]

print("\n\n=== SEARCHING WITH WILDCARDS ===\n")
for word in sorted(set(key_words)):
    results = find_word_with_wildcards(word)
    if results:
        for r, c, direction, positions, wildcards in results:
            wc_info = f" [wildcards: {wildcards}]" if wildcards else ""
            pos_str = [(p[0], p[1], p[2], "WC" if p[3] else "OK") for p in positions]
            print(f"  FOUND '{word}' at ({r},{c}) going {direction}: {pos_str}{wc_info}")
