#!/usr/bin/env python3
"""
Search for a massive list of locations, including:
- All countries
- Major cities
- US states and cities
- Regions and territories
- Famous landmarks as locations
- Less common but valid place names
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
    w = word.upper()
    for r in range(rows):
        for c in range(cols):
            for dr, dc, dname in dirs:
                ok = True
                wc = 0
                known = 0
                info = []
                for k, ch in enumerate(w):
                    nr, nc = r + k*dr, c + k*dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        cell = grid[nr][nc]
                        if cell == ch:
                            known += 1
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
                    results.append((dname, wc, known, info))
    return results

# Massive location list - let me think about what 3-9 letter locations exist
# that use the letters available: M,O,R,A,Y,C,N,U,L,S,T,I,H,D,W,P,E,V,B,K
# (no F,G,J,Q,X,Z in the grid's known letters!)

# Locations to check (comprehensive):
locs = set()

# Countries (3-9 letters, no F/G/J/Q/X/Z needed)
countries = [
    "CHAD", "CHILE", "CHINA", "CONGO", "CUBA", "IRAN", "IRAQ", "ITALY",
    "LAOS", "MALI", "OMAN", "PERU", "TOGO", "BENIN", "BRUNEI", "BURMA",
    "CHILE", "CHINA", "COMOROS", "CROATIA", "DENMARK", "HAITI", "INDIA",
    "IRELAND", "KENYA", "KOREA", "KUWAIT", "LIBERIA", "LIBYA", "MALTA",
    "MOROCCO", "NAURU", "NEPAL", "NIGER", "NORWAY", "PALAU", "PANAMA",
    "POLAND", "SAMOA", "SPAIN", "SUDAN", "SWEDEN", "SYRIA", "TONGA",
    "TURKEY", "TUVALU", "YEMEN", "ZAMBIA",
    "BAHRAIN", "BHUTAN", "BOLIVIA", "BOTSWANA", "CAMEROON",
    "DJIBOUTI", "DOMINICA", "ERITREA", "ESTONIA", "ESWATINI",
    "ETHIOPIA", "HONDURAS", "HUNGARY", "ICELAND", "INDONESIA",
    "KIRIBATI", "LESOTHO", "MALAYSIA", "MALDIVES", "MARSHALL",
    "MYANMAR", "PAKISTAN", "PORTUGAL", "ROMANIA", "RWANDA",
    "SENEGAL", "SERBIA", "SLOVAKIA", "SLOVENIA", "SOMALIA",
    "SURINAME", "THAILAND", "TIMOR", "TRINIDAD", "TUNISIA",
    "TURKMEN", "UKRAINE", "URUGUAY", "VANUATU", "VIETNAM",
    "ZIMBABWE",
]
locs.update(countries)

# US States
states = [
    "ALASKA", "HAWAII", "IDAHO", "IOWA", "KANSAS", "MAINE", "MICHIGAN",
    "MINNESOTA", "MONTANA", "NEBRASKA", "NEVADA", "OHIO", "OKLAHOMA",
    "INDIANA", "MARYLAND", "KENTUCKY", "MISSOURI", "CAROLINA",
    "DAKOTA", "TENNESSEE", "VERMONT", "VIRGINIA", "WISCONSIN",
    "WYOMING", "COLORADO", "CONNECTICUT", "DELAWARE", "ILLINOIS",
    "LOUISIANA", "MISSISSIPPI", "ARKANSAS", "UTAH", "ALABAMA",
    "NEBRASKA", "MICHIGAN", "WISCONSIN", "MINNESOTA",
    "NORTHDAKOTA", "SOUTHDAKOTA",
]
locs.update(states)

# Major world cities (3-9 letters)
cities = [
    "ACCRA", "ADEN", "ALEPPO", "ALMA", "AMMAN", "ANKARA", "ASPEN",
    "ATHENS", "AUSTIN", "BAKU", "BALI", "BAMAKO", "BERN", "BERLIN",
    "BOGOTA", "BONN", "BOSTON", "BRASILIA", "BREMEN", "BRNO",
    "CAIRNS", "CAIRO", "CAMDEN", "CANCUN", "CANTON", "CAPRI",
    "COLOMBO", "COMO", "CORK", "DAMASCUS", "DARWIN", "DELHI",
    "DENVER", "DERBY", "DHAKA", "DOHA", "DOVER", "DUBLIN",
    "DURBAN", "DURHAM", "EDINBURGH", "EDMONTON", "EUREKA",
    "FLORENCE", "HAVANA", "HELSINKI", "HANOI", "HARLEM", "HOUSTON",
    "HULL", "IBADAN", "ISTANBUL", "KAMPALA", "KANPUR", "KARACHI",
    "KENT", "KHARTOUM", "KIEL", "KINGSTON", "KINSHASA", "KOBE",
    "KYOTO", "LAGOS", "LEEDS", "LEON", "LIMA", "LISBON", "LONDON",
    "LUANDA", "LYON", "MACAO", "MADRID", "MALMO", "MANAUS", "MANILA",
    "MAPUTO", "MECCA", "MELBOURNE", "MEMPHIS", "MIAMI", "MILAN",
    "MINSK", "MOBILE", "MOSCOW", "MUMBAI", "MUNICH", "MUSCAT",
    "NAIROBI", "NANTES", "NAPLES", "NEWARK", "NEWPORT", "NEWTOWN",
    "NIAMEY", "NICE", "NORWICH", "OSAKA", "OSLO", "OTTAWA", "OXFORD",
    "PADUA", "PARIS", "PERTH", "PETRA", "PISA", "PORTO", "PRAGUE",
    "PUEBLA", "RABAT", "RENO", "RHODES", "RICHMOND", "RIYADH", "ROME",
    "SACRAMENTO", "SALEM", "SANAA", "SANTIAGO", "SEOUL", "SEVILLA",
    "SOFIA", "STOCKHOLM", "SYDNEY", "TAIPEI", "TAMPA", "TEHRAN",
    "TOKYO", "TOLEDO", "TORONTO", "TRIPOLI", "TROY", "TUNIS",
    "VIENNA", "WACO", "WARSAW", "WICHITA", "WINDSOR", "WUHAN",
    "YOKOHAMA", "YORK", "ZURICH",
    # Smaller/less common cities
    "AARHUS", "ABILENE", "AKRON", "ALBANY", "ALTON", "ANTRIM",
    "ARLES", "AVON", "BATH", "BREST", "CADIZ", "CAEN", "DAVOS",
    "DEAL", "DIEPPE", "DIJON", "DOVER", "DORTMUND", "DUNDEE",
    "ELKO", "ELY", "ENID", "ERIE", "ESSEN", "EXETER",
    "GALWAY", "HILO", "HURON", "ITHACA", "KODIAK", "LAREDO",
    "LEWISTON", "LODI", "LUBBOCK", "MACON", "MESA", "MOAB",
    "ODESSA", "OMAHA", "PROVO", "RALEIGH", "ROANOKE", "ROSWELL",
    "SPOKANE", "STOCKTON", "TOPEKA", "TRENTON", "TUCSON", "TULSA",
    "UTICA", "WACO", "WICHITA", "YUMA",
    # UK locations
    "AIRDRIE", "BATH", "BOLTON", "BUDE", "BURY", "DEAL", "DERRY",
    "DOVER", "ELGIN", "HULL", "HYTHE", "KELSO", "LEWES", "LUTON",
    "MORAY", "NAIRN", "OBAN", "PERTH", "POOLE", "RIPON", "ROSS",
    "TRURO", "WELLS", "WICK", "DERBY", "LEEDS", "NEWRY", "OMAGH",
    "STOKE", "TAUNTON", "YEOVIL",
    # African cities & regions
    "ACCRA", "ASMARA", "BAMAKO", "BANJUL", "BLANTYRE", "BRAZZA",
    "BUKAVU", "DAKAR", "DARES", "DODOMA", "ENTEBBE", "HARARE",
    "IBADAN", "KIGALI", "KINSHASA", "LAGOS", "LILONGWE", "LOME",
    "LUANDA", "LUSAKA", "MALABO", "MAPUTO", "MASERU", "MOMBASA",
    "MONROVIA", "MORONI", "NAIROBI", "NIAMEY", "NOUAKCHOTT",
    "OUAGADOUGOU", "PORTLOUIS", "PRAIA", "PRETORIA", "RABAT",
    "WINDHOEK", "YAMENA",
    # Additional
    "AIDA",  # city in Ethiopia
    "MORAY",  # region in Scotland
    "GREENVILLE",
]
locs.update(cities)

# Scottish regions
scottish = ["MORAY", "ANGUS", "ARRAN", "BUTE", "CAITHNESS", "DUNDEE",
            "DUNOON", "NAIRN", "ORKNEY", "PERTH", "SKYE", "STIRLING"]
locs.update(scottish)

# Regions and other locations
regions = [
    "ALSACE", "ARCTIC", "CRIMEA", "DEVON", "DORSET", "ESSEX",
    "KENT", "LAPLAND", "NORFOLK", "SAHARA", "SIBERIA", "SOMERSET",
    "SUFFOLK", "SURREY", "SUSSEX", "TYROL", "WALES", "WESSEX",
    "CONWAY", "CORNWALL", "CUMBRIA", "HIGHLANDS", "LOWLANDS",
    "MIDLANDS", "PENNINES", "YORKSHIRE",
    # Ancient/historical locations
    "TROY", "SPARTA", "THEBES", "CORINTH", "MYCENAE", "DELPHI",
    "POMPEII", "CARTHAGE", "BABYLON",
    "SHERWOOD", "NOTTINGHAM",
    # Landmarks as locations
    "EUREKA", "OLYMPIA",
    # US county/town names
    "NEWPORT", "NEWTOWN", "NEWMARKET", "NEWHAVEN", "NEWBERG",
    "TWIN", "REDWOOD",
]
locs.update(regions)

# Filter to 3-9 letters
locs = {l.upper() for l in locs if 3 <= len(l) <= 9}
print(f"Searching {len(locs)} location names...\n")

found = []
for loc in sorted(locs):
    results = find_any(loc)
    if results:
        results.sort(key=lambda x: x[1])
        best = results[0]
        dname, wc, known, info = best
        # For length n, allow at most n/3 wildcards (rounded up)
        n = len(loc)
        max_wc = (n + 2) // 3  # ceil(n/3)
        if n <= 3:
            max_wc = 0  # Exact match for 3-letter words
        elif n == 4:
            max_wc = 1
        elif n <= 6:
            max_wc = 2
        else:
            max_wc = 3

        if wc <= max_wc:
            pct = known / n * 100
            found.append((loc, n, dname, wc, pct, info))

found.sort(key=lambda x: (-x[4], -x[1]))

print("=== LOCATIONS FOUND ===\n")
for loc, n, dname, wc, pct, info in found:
    print(f"  {loc:20s} len={n} {dname:3s} wc={wc} ({pct:.0f}% known): {' '.join(info)}")

print(f"\nTotal: {len(found)}")
