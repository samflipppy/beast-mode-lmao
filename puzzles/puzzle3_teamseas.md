# Puzzle 3: TeamSeas TV Shows — "I Cleaned the World's Dirtiest Beach"

## Basic Info
- **Source:** Imgur — imgur.com/gallery/puzzle-mD2eHYD
- **Video:** "I Cleaned the World's Dirtiest Beach #TeamSeas"
- **Puzzle Type:** TV Show identification + debris removal + coordinate extraction
- **Meta-Clue Word:** LEADS (5 letters) — ✅ CONFIRMED
- **Stage 1 Answer:** Unknown location name
- **BeastBot Response:** Confirmed as puzzle

## Puzzle Description
Three columns: "Before Cleanup" (19 TV shows by genre + year range), "Initial removed debris" (letters to remove), "After Cleanup" (row,col extraction coordinates).

## Extraction Method — CONFIRMED by Slackbot
1. Identify each TV show from its genre and exact start/end years
2. Remove the "debris" letters from each show's full title
3. Extract letters at the (row,col) positions given in "After Cleanup"
4. The 19 extracted pairs spell: "A TERM FOR CHIEF ROLES OR METALS WITH SYMBOL PB"
5. Answer: **LEADS** (Pb = lead, leads = chief roles)

## Key Slackbot Intel
- "Yes. Remove the debris letters from each full show title first, then use the cleaned titles to extract letters at the (row,col) positions"
- "Use exact years for matching when the listing gives specific start and end years"
- If a cleaned title is shorter than requested column → wrong show ID

## Detailed Solution
See puzzle3_solution.md and puzzle3_cards.md for full TV show identification tables.

## What We Still Need
- Stage 1 LOCATION answer (separate extraction from the same puzzle?)
- Verify all 19 TV show identifications with exact year matches
- Some shows have uncertain IDs that need verification
