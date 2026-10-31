"""Loads the source sheets, merges split entries, applies corrections and computes tiers."""
import csv, re, unicodedata
from pathlib import Path
from updates import UPDATES

SHEETS = Path(__file__).parent / "sheets"
TIERS = ["goat", "lenda", "estrela", "coadjuvante", "existe"]
SHEET_TIER = {"GOAT": "goat", "Lenda": "lenda", "Estrela": "estrela", "Coadjuvante": "coadjuvante", "Existe": "existe"}
FIELDS = ["m", "c", "l", "n", "k"]  # Mundial, continental, continental menor, liga, copa

UEFA = {"cpt": "Liga dos Campeões", "cen": "Champions League", "lpt": "Liga Europa", "len": "Europa League"}
CONMEBOL = {"cpt": "Libertadores", "cen": "Libertadores", "lpt": "Sul-Americana", "len": "Sudamericana"}

# gid = source tab. Competition labels fix copy-paste slips in the sheet headers
# (France "Copa da Itália", Belgium "Taça dos Países Baixos", Ecuador/Paraguay "Copa Colômbia").
COUNTRIES = [
    dict(id="br", pt="Brasil", en="Brazil", sp="brasil", se="brazil", flag="br", gid="1078701084", **CONMEBOL, n_pt="Brasileiro", n_en="Brasileirão", k_pt="Copa do Brasil", k_en="Copa do Brasil"),
    dict(id="ar", pt="Argentina", en="Argentina", sp="argentina", se="argentina", flag="ar", gid="468792258", **CONMEBOL, n_pt="1ª Divisão", n_en="Primera División", k_pt="Copa Argentina", k_en="Copa Argentina"),
    dict(id="es", pt="Espanha", en="Spain", sp="espanha", se="spain", flag="es", gid="435463999", **UEFA, n_pt="La Liga", n_en="La Liga", k_pt="Copa do Rei", k_en="Copa del Rey"),
    dict(id="it", pt="Itália", en="Italy", sp="italia", se="italy", flag="it", gid="56227883", **UEFA, n_pt="Serie A", n_en="Serie A", k_pt="Copa da Itália", k_en="Coppa Italia"),
    dict(id="en", pt="Inglaterra", en="England", sp="inglaterra", se="england", flag="gb-eng", gid="1264450179", **UEFA, n_pt="1ª Divisão", n_en="Top flight", k_pt="Copa da Inglaterra", k_en="FA Cup"),
    dict(id="de", pt="Alemanha", en="Germany", sp="alemanha", se="germany", flag="de", gid="697098087", **UEFA, n_pt="1ª Divisão", n_en="Top flight", k_pt="Copa da Alemanha", k_en="DFB-Pokal"),
    dict(id="fr", pt="França", en="France", sp="franca", se="france", flag="fr", gid="534598305", **UEFA, n_pt="1ª Divisão", n_en="Top flight", k_pt="Copa da França", k_en="Coupe de France"),
    dict(id="pt", pt="Portugal", en="Portugal", sp="portugal", se="portugal", flag="pt", gid="168833191", **UEFA, n_pt="1ª Divisão", n_en="Primeira Liga", k_pt="Taça de Portugal", k_en="Taça de Portugal"),
    dict(id="nl", pt="Holanda", en="Netherlands", sp="holanda", se="netherlands", flag="nl", gid="1421789206", **UEFA, n_pt="1ª Divisão", n_en="Top flight", k_pt="Taça dos Países Baixos", k_en="KNVB Cup"),
    dict(id="uy", pt="Uruguai", en="Uruguay", sp="uruguai", se="uruguay", flag="uy", gid="290964240", **CONMEBOL, n_pt="1ª Divisão", n_en="Primera División", k_pt="Torneio Intermedio / Copa Uruguai", k_en="Torneo Intermedio / Copa Uruguay"),
    dict(id="co", pt="Colômbia", en="Colombia", sp="colombia", se="colombia", flag="co", gid="1698875957", **CONMEBOL, n_pt="1ª Divisão", n_en="Categoría Primera A", k_pt="Copa Colômbia", k_en="Copa Colombia"),
    dict(id="py", pt="Paraguai", en="Paraguay", sp="paraguai", se="paraguay", flag="py", gid="769116173", **CONMEBOL, n_pt="1ª Divisão", n_en="Primera División", k_pt="Copa Paraguai", k_en="Copa Paraguay"),
    dict(id="ec", pt="Equador", en="Ecuador", sp="equador", se="ecuador", flag="ec", gid="272365176", **CONMEBOL, n_pt="1ª Divisão", n_en="Serie A", k_pt="Copa Equador", k_en="Copa Ecuador"),
    dict(id="sa", pt="Arábia Saudita", en="Saudi Arabia", sp="arabia-saudita", se="saudi-arabia", flag="sa", gid="1397508171", cpt="Liga dos Campeões AFC e Árabe", cen="AFC and Arab Champions League", lpt="Copa do Golfo", len="Gulf Club Champions Cup", n_pt="1ª Divisão", n_en="Saudi League", k_pt="Copa do Rei", k_en="King's Cup"),
    dict(id="be", pt="Bélgica", en="Belgium", sp="belgica", se="belgium", flag="be", gid="1646722981", **UEFA, n_pt="1ª Divisão", n_en="Top flight", k_pt="Copa da Bélgica", k_en="Belgian Cup"),
    dict(id="rs", pt="Sérvia", en="Serbia", sp="servia", se="serbia", flag="rs", gid="1023056021", **UEFA, n_pt="1ª Divisão", n_en="Top flight", k_pt="Copa da Sérvia", k_en="Serbian Cup"),
]

# The sheets merged league and cup winner lists, so one club can appear on two rows.
# alias -> canonical name; a repeated exact name merges on its own. Values take the max per column.
MERGE = {
    "ar": {"Arsenal": "Arsenal de Sarandí"},
    "nl": {"Sparta": "Sparta Rotterdam", "ADO": "ADO Den Haag", "HBS": "HBS Craeyenhout", "NAC": "NAC Breda", "HVV": "HVV Den Haag", "RAP": "RAP Amsterdam"},
    "be": {"Beveren": "KSK Beveren", "Racing Bruxelles": "Racing de Bruxelles", "Daring Bruxelles": "Daring de Bruxelles"},
    "sa": {"Al-Ettifaq": "Al-Ittifaq"},
}

# Facts corrected against the sheet: (country, club, field, value, why)
CORRECTIONS = [
    ("br", "Cruzeiro", "c", 2, "Libertadores de 1976 e 1997; a planilha trazia 1, contrariando a lista de GOATs do próprio levantamento"),
]

# Wrong or missing references in the sheets.
REF_FIX = {"ec": {4: "en.wikipedia.org/wiki/Ecuadorian_Serie_A"}, "es": {4: "en.wikipedia.org/wiki/List_of_Spanish_football_champions", 5: "en.wikipedia.org/wiki/Copa_del_Rey"}, "py": {5: "en.wikipedia.org/wiki/Copa_Paraguay"}, "es": {4: "en.wikipedia.org/wiki/List_of_Spanish_football_champions", 5: "en.wikipedia.org/wiki/Copa_del_Rey"}, "py": {5: "en.wikipedia.org/wiki/Copa_Paraguay"}, "sa": {2: "en.wikipedia.org/wiki/AFC_Champions_League_Elite / pt.wikipedia.org/wiki/Liga_dos_Campe%C3%B5es_%C3%81rabes"}}


def num(s):
    s = (s or "").strip().replace(",", ".")
    return float(s) if s else 0


def tier_of(c):
    high = c["m"] + c["c"]
    if high >= 2: return "goat"
    if high == 1: return "lenda"
    total = c["l"] + c["n"] + c["k"]
    if total >= 2: return "estrela"
    if total == 1: return "coadjuvante"
    return "existe"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def load():
    """Returns (countries, clubs, report). Clubs are in world ranking order, each with .rank."""
    clubs, report = [], []
    for ct in COUNTRIES:
        with open(SHEETS / f"{ct['gid']}.csv", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        ct["refs"] = []
        by = {}
        for r in rows[3:]:
            if r and r[0].startswith("Refer"):
                refs = [x.strip() for x in r[2:7]]
                for i, u in REF_FIX.get(ct["id"], {}).items():
                    refs[i - 1] = u
                ct["refs"] = refs
                continue
            if len(r) < 2 or not r[1].strip():
                continue
            name = r[1].strip()
            canon = MERGE.get(ct["id"], {}).get(name, name)
            vals = [int(num(x)) for x in r[2:7]]
            c = by.get(canon)
            if c is None:
                c = by[canon] = dict(name=canon, ct=ct, sheet=SHEET_TIER[r[0].strip()], fan=num(r[7]) if len(r) > 7 else 0, **dict(zip(FIELDS, vals)))
            else:
                report.append(f"merge {ct['id']}: {name} -> {canon}")
                for k, v in zip(FIELDS, vals):
                    c[k] = max(c[k], v)
                c["fan"] = max(c["fan"], num(r[7]) if len(r) > 7 else 0)
        for cid, name, field, val, why in CORRECTIONS:
            if cid == ct["id"]:
                by[name][field] = val
                report.append(f"fix {cid}: {name}.{field}={val} ({why})")
        for name, vals in UPDATES.get(ct["id"], {}).items():
            if name.startswith("+"):
                name = name[1:]
                by[name] = dict(name=name, ct=ct, sheet="new", fan=0, **{k: 0 for k in FIELDS})
            for field, val in vals.items():
                report.append(f"update {ct['id']}: {name}.{field} {by[name][field]} -> {val}")
                by[name][field] = val
        for c in by.values():
            c["tier"] = tier_of(c)
            c["total"] = sum(c[k] for k in FIELDS)
            c["slug"] = slug(c["name"])
            if c["tier"] != c["sheet"]:
                report.append(f"tier {ct['id']}: {c['name']} sheet={c['sheet']} computed={c['tier']} {[c[k] for k in FIELDS]}")
            clubs.append(c)
    clubs.sort(key=lambda c: (TIERS.index(c["tier"]), *[-c[k] for k in FIELDS], c["name"]))
    for i, c in enumerate(clubs, 1):
        c["rank"] = i
    for ct in COUNTRIES:
        ct["clubs"] = [c for c in clubs if c["ct"] is ct]
        ct["counts"] = {t: sum(c["tier"] == t for c in ct["clubs"]) for t in TIERS}
    order = sorted(COUNTRIES, key=lambda ct: [-ct["counts"][t] for t in TIERS])
    return order, clubs, report


def check_world(clubs):
    """Compares the merged data with the sheet's own all-clubs tab."""
    out, idx = [], {(c["ct"]["pt"], c["name"]): c for c in clubs}
    with open(SHEETS / "1017726082.csv", encoding="utf-8", newline="") as f:
        for r in list(csv.reader(f))[3:]:
            if len(r) < 8 or not r[2].strip():
                continue
            c = idx.get((r[0].strip(), r[2].strip()))
            vals = [int(num(x)) for x in r[3:8]]
            if c is None:
                out.append(f"world tab club not found: {r[0]} / {r[2]}")
            elif vals != [c[k] for k in FIELDS]:
                out.append(f"world tab differs: {c['name']} {vals} vs {[c[k] for k in FIELDS]}")
    return out


if __name__ == "__main__":
    order, clubs, report = load()
    print("\n".join(report + check_world(clubs)))
    print(len(clubs), "clubs;", {t: sum(c["tier"] == t for c in clubs) for t in TIERS})
    print([c["name"] for c in clubs[:12]])
