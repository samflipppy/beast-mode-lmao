#!/usr/bin/env python3
"""
Key finding: MORAY is in the grid at 100% - and Moray IS a location (region in Scotland).
Let me search more systematically for ALL location names in the grid.

Also: the puzzle's 9-word meta-clue confirms all answers should be locations.
"EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD"

And importantly, all 50 Stage 1 answers are "of a certain type" - likely all locations.

Let me also consider: MORAY the location is in SCOTLAND.
The puzzle is about wells in AFRICA.
Maybe answers are all African locations?

Or: MORAY could be the answer to a specific clue. Moray = MORAY EEL
(a type of fish/animal). "A cold noise?" → Moray? Doesn't quite fit.
Maybe "What you might say when you finish" → MORAY sounds like "HOORAY" (Mo-ray)?
That's a stretch.

Let me search for a much larger list of world locations.
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
                info = []
                for k, ch in enumerate(word.upper()):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        cell = grid[nr][nc]
                        if cell == ch:
                            info.append(f'{ch}({nr},{nc})')
                        elif cell is None:
                            wc += 1
                            info.append(f'[{ch}]({nr},{nc})')
                        else:
                            ok = False
                            break
                    else:
                        ok = False
                        break
                if ok:
                    results.append((dname, wc, info))
    return results

# Comprehensive list of world locations (cities, countries, regions, landmarks)
# Focus on 3-9 letter names
locations_raw = """
ACCRA ADEN AIDA ALEPPO ALGIERS ALMATY AMMAN AMSTERDAM ANKARA ANTIGUA
ARUBA ASPEN ASTANA ATHENS AUSTIN BALI BAMAKO BATH BEIJING BELFAST
BELIZE BENIN BERLIN BERN BERNE BHUTAN BOISE BOLIV BOLOGNA BOMBAY
BONN BORDEAUX BOSTON BREMEN BRUNEI BRUSSELS BUCHAREST BUDAPEST
CAIRO CALGARY CAMDEN CANCUN CANNES CANTON CAPE CAPRI CARACAS
CHAD CHILE CHINA COLOMBO COLOGNE COMO CONGO CORK COSTA CRETE
CRIMEA CROATIA CUBA CYPRUS CZECH DAKAR DALLAS DAMASCUS DARWIN
DELHI DENMARK DENVER DERBY DEVON DHAKA DOHA DOVER DUBLIN DURHAM
EDINBURGH EDMONTON EGYPT ESSEN ESSEX ETHIOPIA EUREKA FIJI FINLAND
FLORENCE FLORIDA FRANCE FREETOWN GABON GAMBIA GAZA GENOA GENEVA
GEORGIA GERMANY GHANA GIZA GOLF GREECE GREENVILLE GUAM GUINEA
GUYANA HAITI HAMILTON HANOI HARLEM HAVANA HAWAII HOLLAND HONDURAS
HUNGARY IBADAN ICELAND IDAHO ILLINOIS INDIA INDIANA INDONESIA IOWA
IRAN IRAQ IRELAND ISTANBUL ITALY IVORY JACKSONVILLE JAMAICA JAPAN
JAVA JERSEY JORDAN KAMPALA KANPUR KANSAS KARACHI KATHMANDU KENT
KENYA KINGSTON KINSHASA KOREA KUWAIT KYOTO LAGOS LAOS LATVIA
LEEDS LEON LESOTHO LIBERIA LIBYA LIMA LISBON LIVERP LONDON LUANDA
LUXEMBOURG LYON MACAO MADAGASCAR MADRID MALAWI MALAYSIA MALDIVES
MALI MALTA MANAUS MANILA MAPUTO MARS MECCA MELBOURNE MEMPHIS
MEXICO MIAMI MICHIGAN MIDWAY MILAN MINNESOTA MOBILE MONACO MORAY
MOSCOW MUNICH MUSCAT NAIROBI NAMIBIA NANTES NAPLES NARNIA NATAL
NEBRASKA NEPAL NEVADA NEWARK NEWHAVEN NEWPORT NEWTOWN NEWYORK
NIAGARA NICE NIGER NIGERIA NILE NORFOLK NORMANDY NORTH NORTHPOLE
NORWAY NORWICH OHIO OKLAHOMA OMAN ONTARIO OSAKA OSLO OTTAWA OXFORD
PADUA PAKISTAN PALAU PALM PANAMA PARIS PEKING PENN PERSIA PERU PETRA
PHNOM PHOENIX PISA PLANO PLUTO POLAND PORTO PORTUGAL PRAGUE PUEBLA
QATAR RABAT RANGOON RENO RHODES RICHMOND ROME RUSSIA RWANDA
SACRAMENTO SAHARA SALEM SAMOA SANAA SANTIAGO SARDINIA SATURN SAVANNA
SENEGAL SEOUL SHANGHAI SHERWOOD SIBERIA SIERRA SINGAPORE SOFIA SOMALI
SOUTHPOLE SPAIN STAFFORD STOCKHOLM SUDAN SURREY SWEDEN SYDNEY SYRIA
TABRIZ TAHITI TAIPEI TAMPA TANGO TASHKENT TEHRAN TEXAS THAILAND
TIBET TOGO TOKYO TOLEDO TONGA TORONTO TRINIDAD TRIPOLI TROY TUNIS
TURKEY TUVALU UGANDA UTAH VENICE VERMONT VIENNA VIETNAM WALES WARSAW
WICHITA WINDSOR WISCONSIN WUHAN YEMEN YOKOHAMA YORK YUKON ZAMBIA
ZIMBABWE ZURICH
NOTTINGHAM DAKOTA EDINBURGH CORNWALL DEVON SOMERSET DORSET KENT
SURREY ESSEX SUFFOLK NORFOLK NORWOOD EASTWICK WESTPORT
CHARLESTON SAVANNAH RALEIGH DURHAM CHARLOTTE
TWINPEAKS TWINFALLS NEWPENN OLDNORTH MOUNTRUSHMORE GRANDCANYON
PENNSTATION CAPECOD NEWJERSEY NEWMEXICO NEWORLEANS NEWPORT
IVORYCOAST
GREENVILLE
""".split()

# Remove duplicates and filter
locations = sorted(set(loc.upper() for loc in locations_raw if len(loc) >= 3))

print(f"Searching {len(locations)} location names...\n")
print("=== LOCATIONS FOUND IN GRID ===\n")

found_locations = []
for loc in locations:
    results = find_any(loc)
    if results:
        results.sort(key=lambda x: x[1])
        best = results[0]
        dname, wc, info = best
        max_wc = max(1, len(loc) // 3)  # Allow ~1/3 wildcards
        if wc <= max_wc:
            pct = (len(loc) - wc) / len(loc) * 100
            found_locations.append((loc, dname, wc, len(loc), pct, info))

# Sort by match percentage (highest first), then by length (longest first)
found_locations.sort(key=lambda x: (-x[4], -x[3]))

for loc, dname, wc, length, pct, info in found_locations:
    print(f"  {loc:20s} len={length} {dname:3s} wc={wc} ({pct:.0f}%): {' '.join(info)}")

print(f"\n\nTotal locations found: {len(found_locations)}")

# Now let me also check: can I find SHERWOOD (Sherwood Forest - Robin Hood's location)?
# Or NOTTINGHAM?
print("\n=== SPECIFIC CHECKS ===")
for word in ["SHERWOOD", "NOTTINGHAM", "EUREKA", "ICELAND", "GREENVILLE",
             "NEWPENN", "CORNWALL", "MORAY", "TROY", "ADEN", "TWIN",
             "KENT", "OHIO", "IOWA", "YORK", "CORK", "BOISE", "WACO",
             "DENVER", "DOVER", "NAIROBI", "ACCRA", "GHANA", "IVORYCOAST",
             "DAKOTA", "KANSAS", "NEBRASKA", "INDIANA"]:
    results = find_any(word)
    if results:
        results.sort(key=lambda x: x[1])
        for dname, wc, info in results[:2]:
            if wc <= len(word) // 2:
                print(f"  {word:20s} {dname:3s} wc={wc}/{len(word)}: {' '.join(info)}")
    else:
        pass  # Don't print non-matches

# What about AIDA? That's a location in Ethiopia and an opera
print("\n=== AIDA (place/opera) ===")
for dname, wc, info in find_any("AIDA"):
    print(f"  AIDA {dname} wc={wc}: {' '.join(info)}")

# What about DEVON, CONWAY, MORAY, ORKNEY?
print("\n=== Scottish/British locations ===")
for word in ["MORAY", "DEVON", "CONWAY", "ORKNEY", "LEWIS", "ROSS",
             "BATH", "HULL", "YORK", "DEAL", "RYE", "ELY", "WYE"]:
    results = find_any(word)
    if results:
        for dname, wc, info in results:
            if wc == 0:
                print(f"  {word:15s} {dname:3s} (exact): {' '.join(info)}")
