"""Title counts updated on 2026-10-31 against the English Wikipedia winners tables.
Applied over the source sheets. Clubs not listed keep the sheet values.
Saudi continental titles add the AFC Champions League to the Arab Club Champions Cup.
Fields: m world, c continental, l second continental, n league, k cup. "+" adds a club missing from the sheet."""

UPDATES = {
    "br": {"Flamengo": dict(c=4, n=8, k=5), "Palmeiras": dict(n=12), "Botafogo": dict(c=1, n=3), "Guarani": dict(n=1), "Corinthians": dict(k=4)},
    "ar": {"Vélez Sarsfield": dict(n=11), "Estudiantes": dict(n=7), "Rosario Central": dict(n=5), "Lanús": dict(l=2), "Racing": dict(l=1), "Porteño": dict(n=2), "Quilmes": dict(n=2), "Estudiantil Porteño": dict(n=2),
           "+Platense": dict(n=1), "+Belgrano": dict(n=1), "+Central Córdoba": dict(k=1), "+Independiente Rivadavia": dict(k=1)},
    "es": {"Real Madrid": dict(m=9), "Barcelona": dict(n=29, k=32), "Real Sociedad": dict(k=3), "Real Betis": dict(k=3), "Levante": dict(k=0)},
    "it": {"Inter de Milão": dict(n=21, k=10), "Napoli": dict(n=4), "Bologna": dict(k=3)},
    "en": {"Chelsea": dict(m=2), "Liverpool": dict(n=20), "Manchester United": dict(l=1), "Manchester City": dict(k=8), "Arsenal": dict(c=0, n=14), "Tottenham Hotspur": dict(c=0, l=3), "Leeds United": dict(c=0),
           "Aston Villa": dict(l=1), "Wolverhampton Wanderers": dict(l=0, k=4), "Fulham": dict(l=0), "West Ham United": dict(k=3), "+Crystal Palace": dict(k=1)},
    "de": {"Bayern Munich": dict(n=35, k=21), "VfB Stuttgart": dict(k=4)},
    "fr": {"Paris Saint-Germain": dict(m=1, c=2, n=14, k=16), "Lens": dict(k=1)},
    "pt": {"Porto": dict(n=31), "Sporting": dict(n=21, k=18), "+Torreense": dict(k=1)},
    "nl": {"PSV Eindhoven": dict(n=27), "AZ": dict(k=5), "RAP Amsterdam": dict(n=5), "HFC": dict(n=3), "Go Ahead": dict(k=1)},
    "uy": {"Peñarol": dict(n=52), "Nacional": dict(n=50)},
    "co": {"Atlético Nacional": dict(l=0, n=18, k=8), "Junior": dict(n=12), "Santa Fe": dict(n=10), "Deportivo Cali": dict(k=1)},
    "py": {"Olimpia": dict(n=48), "Cerro Porteño": dict(n=35), "Libertad": dict(n=26, k=3), "+General Caballero": dict(k=1)},
    "ec": {"LDU": dict(n=13), "Independiente del Valle": dict(n=2), "El Nacional": dict(k=2), "+Universidad Católica": dict(k=1)},
    "sa": {"Al-Hilal": dict(c=6, n=21), "Al-Shabab": dict(l=3), "Al-Ahli": dict(c=3, n=9), "Al-Nassr": dict(n=11), "Al-Ittihad": dict(c=3, n=14, k=10), "Al-Wehda": dict(n=1)},
    "be": {"Club Brugge": dict(n=20, k=12), "Union SG": dict(n=12, k=4)},
    "rs": {"Red Star Belgrade": dict(n=37, k=30)},
}
