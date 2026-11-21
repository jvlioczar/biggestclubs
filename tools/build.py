"""Generates every HTML page of the site (PT at the root, EN at /en/). Run: python tools/build.py"""
import json
from html import escape as e
from pathlib import Path
from clubs import load, slug, TIERS, FIELDS

ROOT = Path(__file__).parent.parent
SITE = "https://biggestclubs.biblioverse.org/"
VER = "2026-10-31-r7"
UPDATED = "2026-10-31"
CF_TOKEN = '1c9e4bc747a54ee391a2340dd39a858a'
CF_SNIPPET = f'''<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "{CF_TOKEN}"}}'></script><!-- End Cloudflare Web Analytics -->'''
COUNTRIES, CLUBS, _ = load()

T = {
    "pt": dict(
        html="pt-BR", og="pt_BR", site="Maiores Clubes do Mundo", short="Maiores Clubes do Mundo",
        title="Maiores Clubes do Mundo · Ranking por títulos de cada país",
        desc=f"{len(CLUBS)} clubes de {len(COUNTRIES)} países classificados por títulos mundiais, continentais e nacionais: GOATs, Lendas, Estrelas, Coadjuvantes e Presentes.",
        skip="Pular para o conteúdo", nav_rank="Ranking", nav_ct="Países", nav_nt="Seleções", wc_eyebrow="Copa do Mundo", wc_h="As maiores seleções", wc_p="Seleções masculinas por títulos de Copa do Mundo. No empate, vale o número de vices. A Alemanha inclui os títulos da Alemanha Ocidental.", wc_t="títulos", wc_t1="título", wc_ru="vices", wc_ru1="vice", wc_noru="Nenhum vice", wc_others="Finalistas sem título:", wc_src="Copa do Mundo", nav_crit="Critérios", nav_src="Fontes", menu="Menu", dark="Ativar modo escuro", sections="Seções", language="Idioma",
        eyebrow="O futebol mundial em títulos", h1='Os <span class="hl">maiores clubes</span><br>de futebol de cada país e<br><span class="hl">do mundo</span>',
        lead="Quem tem mais peso na história? Cada clube é classificado pelo que ganhou: Mundiais, títulos continentais, ligas e copas nacionais.",
        search="Busque um clube ou país…", search_l="Buscar", quick="Atalhos:", b_clubs="clubes", b_goats="GOATs", b_ct="países",
        tiers={"goat": "GOAT", "lenda": "Lenda", "estrela": "Estrela", "coadjuvante": "Coadjuvante", "existe": "Presente"},
        tiers_pl={"goat": "GOATs", "lenda": "Lendas", "estrela": "Estrelas", "coadjuvante": "Coadjuvantes", "existe": "Presentes"},
        rules={"goat": "Dois ou mais títulos entre Mundial e o principal torneio continental.", "lenda": "Um título entre Mundial e o principal torneio continental.", "estrela": "Dois ou mais títulos somando o continental menor, a liga nacional e a copa nacional.", "coadjuvante": "Um título do continental menor, da liga nacional ou da copa nacional.", "existe": "Clube tradicional da elite nacional, sem títulos expressivos."},
        top_eyebrow="O topo do mundo", top_h="Os três maiores clubes da história", top_p="Ordem definida por Mundiais, depois continentais, continentais menores, ligas e copas.", top_cta="Ver o ranking",
        ct_h="Os maiores clubes de cada país", ct_p="Países ordenados por número de GOATs e, em seguida, por ordem alfabética.", ct_clubs="clubes", ct_noneg="Nenhum GOAT", ct_top="Maior clube:",
        rk_h="Ranking mundial de clubes", all_ct="Todos os países", all_t="Todos os níveis", country="País", level="Nível",
        col_rank="Pos.", col_club="Clube", col_ct="País", col_tier="Nível", col_m="Mundial", col_c="Continental", col_l="Cont. menor", col_n="Liga", col_k="Copa", col_total="Total", col_fan="Torcida",
        count_one="clube", count_many="clubes", more="Mostrar todos", reset="Limpar filtros", empty="Nenhum clube encontrado. Tente outro nome ou limpe os filtros.",
        world_pos="no mundo", refs="Referências", back="Todos os países", prev="Anterior", next="Próximo",
        fan_note="Torcida: percentual estimado de torcedores no país, quando disponível.", fan_note_br="Torcida: percentual dos brasileiros que torcem para o clube nas pesquisas Ipsos-Ipec / O Globo (junho de 2025) e AtlasIntel / ge (2025). Clubes fora dessas pesquisas ficam sem número.",
        crit_title="Critérios", crit_page="Critérios do ranking", sort="Ordenar", crit_lead="Cada clube recebe um nível apenas pelos títulos que conquistou. Não há voto nem nota subjetiva.", crit_tiers="Os cinco níveis", crit_tie_h="Como funciona o desempate", crit_tie="Dentro de cada nível, vence quem tem mais títulos na ordem: Mundial, continental, continental menor, liga nacional e copa nacional.",
        crit_notes_h="Como ler os dados",
        crit_notes=["Cada continente usa suas próprias competições. Nos clubes sauditas, o principal título continental soma a Liga dos Campeões da AFC e a Liga dos Campeões Árabe, no mesmo nível de uma Libertadores ou de uma Liga dos Campeões da UEFA. Por isso o ranking mede o domínio em cada região, sem comparar a força das competições.", "Em \"Mundial\" entram os títulos mundiais de clubes reconhecidos nas referências do projeto, incluindo os da antiga Copa Intercontinental.", "Clubes que apareciam duas vezes, na lista da liga e na da copa, foram unificados e tiveram o nível recalculado.", "As contagens foram atualizadas em 31 de outubro de 2026 com as listas de campeões da Wikipedia. Só contam os troféus já registrados nessas listas."],
        src_title="Fontes", about_title="Sobre", about_page="Sobre o projeto", about_desc="O que é o Maiores Clubes do Mundo, como os clubes são classificados e outros projetos recomendados sobre esporte.", about_lead="Um ranking dos clubes de futebol pelo que realmente ganharam, país por país e no mundo.", about_body=["O Maiores Clubes do Mundo reúne clubes de 16 países e os classifica em cinco níveis, apenas pelos títulos conquistados: Mundiais, torneios continentais, ligas e copas nacionais.", "O site também traz as maiores seleções masculinas por títulos de Copa do Mundo. A discussão nunca acaba, e é justamente por isso que os critérios e as fontes ficam abertos para quem quiser conferir."], about_how="Como funciona", rec_h="Projetos recomendados", rec_p="Gostou? Conheça também:", src_page="Fontes dos títulos", intro_many="{n} clubes {c} estão neste ranking.", intro_one="1 clube {c} está neste ranking.", intro_top="Mais bem colocado: {x} ({r}º no mundo), com {s} títulos contados.", og_alt="Maiores Clubes do Mundo: clubes classificados por títulos", home_l="Início", src_lead="As contagens de títulos partem de um levantamento próprio, atualizado em 31 de outubro de 2026 com as listas de campeões da Wikipedia. Estas são as referências por país e competição.", src_world="Mundial", src_cont="Continentais",
        foot_upd="Última atualização:", foot_date="31 de outubro de 2026", foot_by="Projeto criado por", foot_special="Maiores Clubes do Mundo é um projeto especial do", foot_note="Levantamento em revisão contínua. Encontrou um título faltando? A discussão faz parte do futebol.",
        nf_title="Página não encontrada", nf_p="Essa página saiu de campo.", nf_cta="Voltar ao início",
        crit_desc="Como os clubes são classificados em GOAT, Lenda, Estrela, Coadjuvante e Presente, e como funciona o desempate.", src_desc="As referências usadas para contar os títulos de cada clube, por país e competição.",
        ct_desc="Os maiores clubes {c} por títulos: {n} clubes classificados, com Mundiais, títulos continentais, ligas e copas.", ct_h1="Os maiores clubes {c}",
    ),
    "en": dict(
        html="en", og="en_US", site="The World's Biggest Clubs", short="The World's Biggest Clubs",
        title="The World's Biggest Clubs · Ranked by titles, country by country",
        desc=f"{len(CLUBS)} clubs from {len(COUNTRIES)} countries ranked by world, continental and domestic titles: GOATs, Legends, Stars, Supporting clubs and Traditional clubs.",
        skip="Skip to content", nav_rank="Ranking", nav_ct="Countries", nav_nt="National teams", wc_eyebrow="World Cup", wc_h="The biggest national teams", wc_p="Men's national teams by World Cup titles. Ties are broken by runner-up finishes. Germany includes West Germany's titles.", wc_t="titles", wc_t1="title", wc_ru="runner-up finishes", wc_ru1="runner-up finish", wc_noru="No runner-up finishes", wc_others="Finalists without a title:", wc_src="World Cup", nav_crit="Criteria", nav_src="Sources", menu="Menu", dark="Turn on dark mode", sections="Sections", language="Language",
        eyebrow="World football in trophies", h1='The <span class="hl">biggest clubs</span><br>in football, in every<br>country and <span class="hl">the world</span>',
        lead="Who carries the most weight in history? Every club is ranked by what it won: world titles, continental trophies, domestic leagues and cups.",
        search="Search for a club or country…", search_l="Search", quick="Shortcuts:", b_clubs="clubs", b_goats="GOATs", b_ct="countries",
        tiers={"goat": "GOAT", "lenda": "Legend", "estrela": "Star", "coadjuvante": "Supporting", "existe": "Traditional"},
        tiers_pl={"goat": "GOATs", "lenda": "Legends", "estrela": "Stars", "coadjuvante": "Supporting", "existe": "Traditional"},
        rules={"goat": "Two or more titles across the world title and the top continental competition.", "lenda": "One title across the world title and the top continental competition.", "estrela": "Two or more titles across the second continental competition, the national league and the national cup.", "coadjuvante": "One title in the second continental competition, the national league or the national cup.", "existe": "A traditional top-flight club with no major titles."},
        top_eyebrow="Top of the world", top_h="The three biggest clubs in history", top_p="Order set by world titles, then continental titles, second-tier continental titles, leagues and cups.", top_cta="See the ranking",
        ct_h="The biggest clubs in each country", ct_p="Countries sorted by number of GOATs, then alphabetically.", ct_clubs="clubs", ct_noneg="No GOAT", ct_top="Biggest club:",
        rk_h="World club ranking", all_ct="All countries", all_t="All tiers", country="Country", level="Tier",
        col_rank="Rank", col_club="Club", col_ct="Country", col_tier="Tier", col_m="World", col_c="Continental", col_l="2nd cont.", col_n="League", col_k="Cup", col_total="Total", col_fan="Fans",
        count_one="club", count_many="clubs", more="Show all", reset="Clear filters", empty="No clubs found. Try another name or clear the filters.",
        world_pos="in the world", refs="References", back="All countries", prev="Previous", next="Next",
        fan_note="Fans: estimated share of supporters in the country, where available.", fan_note_br="Fans: share of Brazilians who support the club in the Ipsos-Ipec / O Globo (June 2025) and AtlasIntel / ge (2025) surveys. Clubs outside those surveys have no number.",
        crit_title="Criteria", crit_page="Ranking criteria", sort="Sort by", crit_lead="Each club gets a tier purely from the titles it has won. There are no votes or subjective scores.", crit_tiers="The five tiers", crit_tie_h="How ties are broken", crit_tie="Within each tier, the club with more titles comes first, in this order: world, continental, second-tier continental, national league and national cup.",
        crit_notes_h="How to read the data",
        crit_notes=["Each continent uses its own competitions. For Saudi clubs, the top continental count adds the AFC Champions League and the Arab Club Champions Cup, at the same level as a Libertadores or a UEFA Champions League, so the ranking measures dominance in each region without comparing the strength of the competitions.", "\"World\" covers the club world titles recognised in the project's references, including the former Intercontinental Cup.", "Clubs listed twice, once for the league and once for the cup, were merged and their tier recalculated.", "Counts were updated on October 31, 2026 from Wikipedia's lists of winners. Only trophies already recorded in those lists are counted."],
        src_title="Sources", about_title="About", about_page="About the project", about_desc="What The World's Biggest Clubs is, how clubs are ranked, and other recommended sports projects.", about_lead="A ranking of football clubs by what they have actually won, country by country and worldwide.", about_body=["The World's Biggest Clubs covers clubs from 16 countries and ranks them in five tiers, purely by the titles they have won: world titles, continental competitions, national leagues and cups.", "The site also lists the biggest men's national teams by World Cup titles. The debate never ends, which is exactly why the criteria and sources are open for anyone to check."], about_how="How it works", rec_h="Recommended projects", rec_p="Enjoyed this? Check out:", src_page="Title sources", intro_many="{n} clubs from {c} are in this ranking.", intro_one="1 club from {c} is in this ranking.", intro_top="Highest placed: {x} (#{r} in the world), with {s} counted titles.", og_alt="The World's Biggest Clubs: clubs ranked by titles", home_l="Home", src_lead="Title counts come from the project's own survey, updated on October 31, 2026 from Wikipedia's lists of winners. These are the references by country and competition.", src_world="World", src_cont="Continental",
        foot_upd="Last updated:", foot_date="October 31, 2026", foot_by="Project created by", foot_special="The World's Biggest Clubs is a special project of", foot_note="This survey is under continuous review. Spotted a missing trophy? Arguing about it is part of football.",
        nf_title="Page not found", nf_p="This page has left the pitch.", nf_cta="Back to home",
        crit_desc="How clubs are ranked as GOAT, Legend, Star, Supporting or Traditional, and how ties are broken.", src_desc="The references used to count each club's titles, by country and competition.",
        ct_desc="The biggest clubs in {c} by titles: {n} ranked clubs, with world titles, continental trophies, leagues and cups.", ct_h1="The biggest clubs in {c}",
    ),
}
PATHS = {"pt": dict(home="", about="sobre.html", crit="criterios.html", src="fontes.html", ct="paises/{s}.html"), "en": dict(home="en/", about="en/about.html", crit="en/criteria.html", src="en/sources.html", ct="en/countries/{s}.html")}
SLUG = {"pt": "sp", "en": "se"}
OGIMG = {"pt": "og-image.png", "en": "og-image-en.png"}

ICO = dict(
    menu='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    search='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    moon='<svg class="ico moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>',
    sun='<svg class="ico sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    go='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    back='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="m15 18-6-6 6-6"/></svg>',
)
LOGO = '<svg viewBox="0 0 40 46" aria-hidden="true"><path d="M20 2 37 8v14c0 11-7 18-17 22C10 40 3 33 3 22V8z" fill="var(--primary)"/><path d="M13 11h14v6c0 5-3 8-7 8s-7-3-7-8z" fill="#FFC94D"/><path d="M13 13H9c0 5 2 7 5 8M27 13h4c0 5-2 7-5 8" fill="none" stroke="#FFC94D" stroke-width="2.2" stroke-linecap="round"/><path d="M20 25v5" stroke="#FFC94D" stroke-width="3"/><rect x="14" y="30" width="12" height="3.5" rx="1.5" fill="#FFC94D"/></svg>'
TROPHY = '''<svg class="cup" viewBox="0 0 240 300">
  <g stroke="#1E1B2E" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">
    <path d="M64 56H26c0 52 18 78 54 88" fill="none" stroke-width="15"/><path d="M176 56h38c0 52-18 78-54 88" fill="none" stroke-width="15"/>
    <path d="M64 56H26c0 52 18 78 54 88" fill="none" stroke="#FFC94D" stroke-width="7"/><path d="M176 56h38c0 52-18 78-54 88" fill="none" stroke="#FFC94D" stroke-width="7"/>
    <path d="M60 26h120v76c0 50-26 78-60 78s-60-28-60-78z" fill="#FFC94D"/>
    <path d="M154 34h14v66c0 34-14 56-34 66 14-16 20-36 20-66z" fill="#E0A421" stroke="none"/>
    <path d="M106 178h28v44h-28z" fill="#E0A421"/><path d="M70 222h100l10 40H60z" fill="#5B3FD6"/><rect x="48" y="262" width="144" height="22" rx="7" fill="#1E1B2E"/>
    <g transform="translate(120 100)"><circle r="37" fill="#fff"/><path d="M0-15 14-5 9 12H-9L-14-5z" fill="#1E1B2E"/><path d="M0-15V-36M14-5 34-12M9 12l13 18M-9 12l-13 18M-14-5l-20-7" stroke-width="4"/></g>
  </g>
  <rect x="96" y="267" width="48" height="11" rx="3" fill="#FFC94D"/>
</svg>'''


# Men's World Cup, checked 2026-10-31 against en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals
WORLD_CUP = [
    dict(pt="Brasil", en="Brazil", flag="br", won=[1958, 1962, 1970, 1994, 2002], lost=[1950, 1998]),
    dict(pt="Alemanha", en="Germany", flag="de", won=[1954, 1974, 1990, 2014], lost=[1966, 1982, 1986, 2002]),
    dict(pt="Itália", en="Italy", flag="it", won=[1934, 1938, 1982, 2006], lost=[1970, 1994]),
    dict(pt="Argentina", en="Argentina", flag="ar", won=[1978, 1986, 2022], lost=[1930, 1990, 2014, 2026]),
    dict(pt="França", en="France", flag="fr", won=[1998, 2018], lost=[2006, 2022]),
    dict(pt="Espanha", en="Spain", flag="es", won=[2010, 2026], lost=[]),
    dict(pt="Uruguai", en="Uruguay", flag="uy", won=[1930, 1950], lost=[]),
    dict(pt="Inglaterra", en="England", flag="gb-eng", won=[1966], lost=[]),
]
WC_OTHERS = {"pt": "Holanda (3 vices), Hungria (2), Tchecoslováquia (2), Croácia (1) e Suécia (1).", "en": "Netherlands (3 runner-up finishes), Czechoslovakia (2), Hungary (2), Croatia (1) and Sweden (1)."}
WC_REF = "en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals"


RECOMMENDED = [
    dict(icon="⚽", name=dict(pt="Lendas do Futebol Brasileiro", en="Legends of Brazilian Football"), url=dict(pt="https://lendasdofutebolbrasileiro.biblioverse.org", en="https://lendasdofutebolbrasileiro.biblioverse.org"),
         pt="As seleções de todos os tempos da Seleção Brasileira e dos clubes do Brasil.", en="All-time squads of the Brazil national team and Brazilian clubs (in Portuguese)."),
    dict(icon="🐐", name=dict(pt="GOATs", en="GOATs"), url=dict(pt="https://goat.biblioverse.org", en="https://goat.biblioverse.org/en/"),
         pt="Os maiores atletas de todos os tempos em cada esporte.", en="The greatest athletes of all time in every sport."),
]


def rec_links(lang):
    return "".join(f'<a href="{r["url"][lang]}" target="_blank" rel="noopener"><span aria-hidden="true">{r["icon"]}</span> {r["name"][lang]}</a>' for r in RECOMMENDED)


def ordered(lang):
    """Countries by number of GOATs, then alphabetically."""
    return sorted(COUNTRIES, key=lambda ct: (-ct["counts"]["goat"], slug(ct[lang])))


def nations(lang):
    t = T[lang]
    cards = ""
    for i, n in enumerate(WORLD_CUP, 1):
        w, l = len(n["won"]), len(n["lost"])
        ru = (f'{l} {t["wc_ru1"] if l == 1 else t["wc_ru"]}' + " · " + ", ".join(map(str, n["lost"]))) if l else t["wc_noru"]
        stars = '<span class="stars" aria-hidden="true">' + "★" * w + "</span>"
        cards += f'<li class="nt"><span class="nt-pos">{i}</span><span class="fi fi-{n["flag"]} big" aria-hidden="true"></span><div class="nt-main"><h3>{n[lang]}</h3>{stars}<p class="nt-years">{", ".join(map(str, n["won"]))}</p><p class="nt-ru">{ru}</p></div><div class="nt-n"><strong>{w}</strong><span>{t["wc_t1"] if w == 1 else t["wc_t"]}</span></div></li>'
    return f'''<section class="wrap sec" id="selecoes" aria-labelledby="nt-h">
    <p class="eyebrow">{t["wc_eyebrow"]}</p><h2 id="nt-h">{t["wc_h"]}</h2><p class="sec-p">{t["wc_p"]}</p>
    <ol class="nt-grid">{cards}</ol>
    <p class="nt-others"><strong>{t["wc_others"]}</strong> {WC_OTHERS[lang]}</p>
  </section>'''


def fmt(n):
    return str(n) if n else '<span class="z">–</span>'


def flag(ct):
    return f'<span class="fi fi-{ct["flag"]}" aria-hidden="true"></span>'


def badge(t, tier):
    return f'<span class="tier t-{tier}">{t["tiers"][tier]}</span>'


def pct(v, lang):
    s = f"{v:.1f}%"
    return s.replace(".", ",") if lang == "pt" else s


def fan(c):
    return (f'{c["fan"]:.1f}'.rstrip("0").rstrip(".")) + "%" if c["fan"] else ""


def link(lang, key, base, s=None):
    return base + PATHS[lang][key].format(s=s)


def page(lang, key, s_key, title, desc, body, nodes=(), cur=""):
    """s_key: the country dict on country pages. Base is the relative path back to the site root."""
    t = T[lang]
    s = s_key[SLUG[lang]] if s_key else None
    rel = PATHS[lang][key].format(s=s)
    base = "../" * rel.count("/")
    alt = "en" if lang == "pt" else "pt"
    alt_rel = PATHS[alt][key].format(s=s_key[SLUG[alt]] if s_key else None)
    pt_rel, en_rel = (rel, alt_rel) if lang == "pt" else (alt_rel, rel)
    def nav(cls=""):
        items = [(link(lang, "home", base) or "./") + "#ranking", t["nav_rank"], ""], [(link(lang, "home", base) or "./") + "#paises", t["nav_ct"], ""], [(link(lang, "home", base) or "./") + "#selecoes", t["nav_nt"], ""], [link(lang, "crit", base), t["nav_crit"], "crit"], [link(lang, "src", base), t["nav_src"], "src"], [link(lang, "about", base), t["about_title"], "about"]
        return "".join(f'<a href="{h}"{" aria-current=\"page\"" if cur and cur == c else ""}>{l}</a>' for h, l, c in items)
    home = link(lang, "home", base) or "./"
    pt_a, en_a = base + (pt_rel or "./") if pt_rel or base else "./", base + en_rel
    url = SITE + rel
    graph = [
        {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": T["pt"]["site"], "alternateName": T["en"]["site"], "inLanguage": ["pt-BR", "en"], "author": {"@id": SITE + "#author"}, "publisher": {"@id": SITE + "#author"}},
        {"@type": "Person", "@id": SITE + "#author", "name": "Julio Cesar Prava", "url": "https://linkedin.com/in/juliocesarprava"},
        {"@type": "CollectionPage" if key in ("home", "ct") else "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": t["html"], "isPartOf": {"@id": SITE + "#website"}, "primaryImageOfPage": SITE + OGIMG[lang], "dateModified": UPDATED},
    ]
    if key != "home":
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": t["home_l"], "item": SITE + PATHS[lang]["home"]},
            {"@type": "ListItem", "position": 2, "name": title.split(" · ")[0], "item": url}]})
    graph += list(nodes)
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>\n"
    html = f'''<!doctype html>
<html lang="{t["html"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="author" content="Julio Cesar Prava">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}{rel}">
<link rel="alternate" hreflang="pt-BR" href="{SITE}{pt_rel}">
<link rel="alternate" hreflang="en" href="{SITE}{en_rel}">
<link rel="alternate" hreflang="x-default" href="{SITE}{pt_rel}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(t["site"])}">
<meta property="og:locale" content="{t["og"]}">
<meta property="og:locale:alternate" content="{T[alt]["og"]}">
<meta property="og:url" content="{SITE}{rel}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}{OGIMG[lang]}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(t["og_alt"])}">
<meta name="twitter:image:alt" content="{e(t["og_alt"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}{OGIMG[lang]}">
<meta name="theme-color" content="#F3F2F8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0B1019" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{base}favicon.ico" sizes="32x32">
<link rel="icon" href="{base}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
{ld}<script>try {{ if (localStorage.getItem('bc-theme') === 'dark') document.documentElement.dataset.theme = 'dark'; }} catch (e) {{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link href="https://fonts.googleapis.com/css2?family=Gabarito:wght@700;800;900&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/css/flag-icons.min.css">
<script src="https://biblioverse.org/superbar.js" defer></script>
<link rel="stylesheet" href="{base}assets/styles.css?v={VER}">
</head>
<body>
<nav id="bvbar" class="bvbar" data-current="biggestclubs" data-offset="none" aria-label="BiblioVerse" style="position:relative;height:36px;z-index:9000;background:linear-gradient(90deg,#4f7cff,#7a5cff)"><a href="https://biblioverse.org" style="color:#fff;line-height:36px;padding:0 14px;font-weight:700;text-decoration:none;font-family:sans-serif">BiblioVerse</a></nav>
<a class="skip" href="#conteudo">{t["skip"]}</a>
<header class="topbar wrap">
  <a class="logo" href="{home}" aria-label="{e(t["site"])}">{LOGO}<span>{t["short"]}</span></a>
  <nav class="topnav" aria-label="{t["sections"]}">{nav()}</nav>
  <details class="mnav">
    <summary class="theme-btn" aria-label="{t["menu"]}">{ICO["menu"]}</summary>
    <nav class="mnav-list" aria-label="{t["sections"]}">{nav()}</nav>
  </details>
  <button class="theme-btn" id="theme" type="button" aria-label="{t["dark"]}" aria-pressed="false">{ICO["moon"]}{ICO["sun"]}</button>
  <nav class="lang" aria-label="{t["language"]}">
    <a{' class="on" aria-current="true"' if lang == "pt" else ""} href="{pt_a}" hreflang="pt-BR" lang="pt-BR">PT</a>
    <a{' class="on" aria-current="true"' if lang == "en" else ""} href="{en_a}" hreflang="en" lang="en">EN</a>
  </nav>
</header>
{body}
<footer class="wrap footer">
  <div class="foot-rec"><strong>{t["rec_p"]}</strong>{rec_links(lang)}</div>
  <p><strong>{t["foot_upd"]}</strong> <time datetime="{UPDATED}">{t["foot_date"]}</time> · <a href="{link(lang, "crit", base)}">{t["nav_crit"]}</a> · <a href="{link(lang, "src", base)}">{t["nav_src"]}</a> · <a href="{link(lang, "about", base)}">{t["about_title"]}</a></p>
  <p class="muted">{t["foot_note"]}</p>
  <p class="credit">{t["foot_by"]} <a href="https://linkedin.com/in/juliocesarprava" target="_blank" rel="noopener author">Julio Cesar Prava</a>. {t["foot_special"]} <a href="https://biblioverse.org" target="_blank" rel="noopener">BiblioVerse</a>.</p>
</footer>
<script src="{base}assets/app.js?v={VER}"></script>
{CF_SNIPPET}
</body>
</html>
'''
    out = ROOT / (rel or "index.html")
    if rel.endswith("/"):
        out = ROOT / rel / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8", newline="\n")


def in_country(lang, ct):
    """Country name with its preposition: "do Brasil", "da Argentina", "the Netherlands"."""
    if lang == "en":
        return "the Netherlands" if ct["id"] == "nl" else ct["en"]
    prep = {"br": "do", "uy": "do", "py": "do", "ec": "do", "pt": "de"}.get(ct["id"], "da")
    return f'{prep} {ct["pt"]}'


def ct_url(lang, ct, base):
    return base + PATHS[lang]["ct"].format(s=ct[SLUG[lang]])


def shy(label):
    """Soft hyphens so long competition names break cleanly in the narrow mobile columns."""
    for a, b in [("Continental", "Conti-nental"), ("Libertadores", "Liber-tadores"), ("Campeões", "Cam-peões"), ("Americana", "Ameri-cana"), ("Champions", "Cham-pions"), ("Sudamericana", "Suda-mericana"), ("Brasileir", "Brasi-leir"), ("División", "Divi-sión"), ("Intermedio", "Inter-medio"), ("Categoría", "Cate-goría")]:
        label = label.replace(a, b.replace("-", "­"))
    return label


def row(t, lang, c, base, world=True, n=None, cols=None, fans=False):
    """One ranking row. On small screens each cell is labelled through data-l."""
    cols = cols or [t["col_m"], t["col_c"], t["col_l"], t["col_n"], t["col_k"]]
    ct = c["ct"]
    if world:
        sub = f'<a class="sub" href="{ct_url(lang, ct, base)}">{flag(ct)}{e(ct[lang])}</a>'
    else:
        sub = f'<span class="sub">#{c["rank"]} {t["world_pos"]}</span>'
    nums = "".join(f'<td class="num" data-l="{e(shy(l))}">{fmt(c[k])}</td>' for k, l in zip(FIELDS, cols))
    data = f'data-rank="{c["rank"]}" data-ct="{ct["id"]}" data-tier="{c["tier"]}" data-q="{e((c["name"] + " " + ct["pt"] + " " + ct["en"]).lower())}" data-total="{c["total"]}"' + "".join(f' data-{k}="{c[k]}"' for k in FIELDS) + f' data-name="{e(c["name"])}"'
    fan_txt = fan(c).replace(".", ",") if lang == "pt" else fan(c)
    if c.get("fans"):
        fan_txt = '<span class="fan2">' + "".join(f"<span>{s} <b>{pct(v, lang)}</b></span>" for s, v in zip(("Ipsos-Ipec", "AtlasIntel"), c["fans"]) if v is not None) + "</span>"
    fan_td = f'<td class="num fan" data-l="{t["col_fan"]}">{fan_txt or "<span class=\"z\">–</span>"}</td>' if fans else ""
    return f'<tr {data}><td class="pos">{n or c["rank"]}</td><td class="club"><strong>{e(c["name"])}</strong>{sub}</td><td class="tc">{badge(t, c["tier"])}</td>{nums}<td class="num tot" data-l="{t["col_total"]}">{c["total"]}</td>{fan_td}</tr>'


def table(t, rows, cols=None, fans=False, sortable=False):
    cols = cols or [t["col_m"], t["col_c"], t["col_l"], t["col_n"], t["col_k"]]
    def th(label, key, cls="num"):
        if sortable:
            return f'<th scope="col" class="{cls}" aria-sort="{"ascending" if key == "rank" else "none"}"><button type="button" data-sort="{key}">{label}</button></th>'
        return f'<th scope="col" class="{cls}">{label}</th>'
    head = th(t["col_rank"], "rank", "pos") + th(t["col_club"], "name", "club") + th(t["col_tier"], "tier", "tc") + "".join(th(l, k) for k, l in zip(FIELDS, cols)) + th(t["col_total"], "total")
    if fans:
        head += f'<th scope="col" class="num">{t["col_fan"]}</th>'
    return f'<div class="tbl"><table class="rank-t"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'


def tier_bar(ct):
    return '<span class="bar" aria-hidden="true">' + "".join(f'<i class="t-{t}" style="flex:{ct["counts"][t]}"></i>' for t in TIERS if ct["counts"][t]) + "</span>"


def home(lang):
    t = T[lang]
    base = "../" if lang == "en" else ""
    goats = sum(c["tier"] == "goat" for c in CLUBS)
    quick = "".join(f'<a href="{ct_url(lang, next(x for x in COUNTRIES if x["id"] == i), base)}">{flag(next(x for x in COUNTRIES if x["id"] == i))}{next(x for x in COUNTRIES if x["id"] == i)[lang]}</a>' for i in ["br", "ar", "es", "it", "en"])
    tier_cards = "".join(f'<button type="button" class="tcard t-{k}" data-tier-pick="{k}"><strong>{sum(c["tier"] == k for c in CLUBS)}</strong><span>{t["tiers_pl"][k]}</span><small>{t["rules"][k]}</small></button>' for k in TIERS)
    podium = ""
    for c in CLUBS[:3]:
        stats = "".join(f'<li><b>{c[k]}</b><span>{l}</span></li>' for k, l in zip(FIELDS, [t["col_m"], t["col_c"], t["col_l"], t["col_n"], t["col_k"]]))
        podium += f'<li class="pod"><span class="medal">{c["rank"]}</span><h3>{e(c["name"])}</h3><p>{flag(c["ct"])}{c["ct"][lang]}</p><ul class="pod-n">{stats}</ul></li>'
    cards = ""
    for ct in ordered(lang):
        gs = [c["name"] for c in ct["clubs"] if c["tier"] == "goat"]
        names = ("<b>" + str(len(gs)) + " " + (t["tiers_pl"]["goat"] if len(gs) != 1 else "GOAT") + ":</b> " + e(", ".join(gs))) if gs else f'<b>{t["ct_noneg"]}.</b> {t["ct_top"]} {e(ct["clubs"][0]["name"])}'
        cards += f'<a class="ct-card" href="{ct_url(lang, ct, base)}"><header><span class="fi fi-{ct["flag"]} big" aria-hidden="true"></span><h3>{ct[lang]}</h3><small>{len(ct["clubs"])} {t["ct_clubs"] if len(ct["clubs"]) != 1 else t["count_one"]}</small></header>{tier_bar(ct)}<p>{names}</p></a>'
    options = "".join(f'<option value="{ct["id"]}">{ct[lang]}</option>' for ct in sorted(COUNTRIES, key=lambda x: x[lang]))
    tier_opts = "".join(f'<option value="{k}">{t["tiers_pl"][k]}</option>' for k in TIERS)
    rows = [row(t, lang, c, base) for c in CLUBS]
    extra = [{"@type": "ItemList", "name": t["rk_h"], "numberOfItems": len(CLUBS), "itemListElement": [{"@type": "ListItem", "position": c["rank"], "name": c["name"]} for c in CLUBS[:10]]}]
    body = f'''<main id="conteudo">
  <section class="hero wrap">
    <div class="hero-card">
      <div class="hero-text">
        <p class="eyebrow">{t["eyebrow"]}</p>
        <h1>{t["h1"]}</h1>
        <p class="lead">{t["lead"]}</p>
        <label class="search big" for="q">{ICO["search"]}<input id="q" type="search" autocomplete="off" spellcheck="false" placeholder="{t["search"]}" aria-label="{t["search_l"]}"><kbd>/</kbd></label>
        <div class="quick"><span>{t["quick"]}</span>{quick}</div>
      </div>
      <div class="hero-art" aria-hidden="true">
        <div class="badge b1"><strong>{len(CLUBS)}</strong><span>{t["b_clubs"]}</span></div>
        <div class="badge b2"><strong>{goats}</strong><span>{t["b_goats"]}</span></div>
        <div class="badge b3"><strong>{len(COUNTRIES)}</strong><span>{t["b_ct"]}</span></div>
        {TROPHY}
      </div>
    </div>
  </section>
  <section class="wrap tcards" aria-label="{t["crit_tiers"]}">{tier_cards}</section>
  <section class="wrap top3" aria-labelledby="top-h">
    <div class="top3-head"><div><p class="eyebrow">{t["top_eyebrow"]}</p><h2 id="top-h">{t["top_h"]}</h2><p>{t["top_p"]}</p></div><a class="go" href="#ranking">{t["top_cta"]}{ICO["go"]}</a></div>
    <ol class="pods">{podium}</ol>
  </section>
  <section class="wrap sec" id="paises" aria-labelledby="ct-h">
    <h2 id="ct-h">{t["ct_h"]}</h2><p class="sec-p">{t["ct_p"]}</p>
    <div class="ct-grid">{cards}</div>
  </section>
  {nations(lang)}
  <section class="wrap sec" id="ranking" aria-labelledby="rk-h">
    <h2 id="rk-h">{t["rk_h"]}</h2>
    <div class="toolbar">
      <label class="search mini" for="q2">{ICO["search"]}<input id="q2" type="search" autocomplete="off" spellcheck="false" placeholder="{t["search"]}" aria-label="{t["search_l"]}"></label>
      <label class="select"><span class="sr">{t["country"]}</span><select id="fct"><option value="">{t["all_ct"]}</option>{options}</select></label>
      <label class="select"><span class="sr">{t["level"]}</span><select id="ftier"><option value="">{t["all_t"]}</option>{tier_opts}</select></label>
      <label class="select sort-m"><span class="sr">{t["sort"]}</span><select id="fsort"><option value="rank">{t["sort"]}: {t["col_rank"]}</option><option value="total">{t["col_total"]}</option><option value="m">{t["col_m"]}</option><option value="c">{t["col_c"]}</option><option value="n">{t["col_n"]}</option><option value="k">{t["col_k"]}</option><option value="name">{t["col_club"]}</option></select></label>
    </div>
    <div class="result-head"><p id="count" aria-live="polite" data-one="{t["count_one"]}" data-many="{t["count_many"]}"></p><button class="link-btn" id="reset" type="button" hidden>{t["reset"]}</button></div>
    {table(t, rows, sortable=True)}
    <p class="empty" id="empty" hidden>{t["empty"]}</p>
    <div class="more-wrap"><button class="more" id="more" type="button">{t["more"]}</button></div>
  </section>
</main>'''
    page(lang, "home", None, t["title"], t["desc"], body, extra)


def country(lang, i, ct, order):
    t = T[lang]
    base = "../../" if lang == "en" else "../"
    cols = [t["col_m"], ct["c" + lang], ct["l" + lang], ct["n_" + lang], ct["k_" + lang]]
    fans = any(c["fan"] for c in ct["clubs"])
    n = 0
    groups = ""
    for k in TIERS:
        rows = []
        for c in ct["clubs"]:
            if c["tier"] == k:
                n += 1
                rows.append(row(t, lang, c, base, world=False, n=n, cols=cols, fans=fans))
        if rows:
            groups += f'<section class="group"><h2><span class="dot t-{k}"></span>{t["tiers_pl"][k]} <small>{len(rows)}</small></h2><p class="sec-p">{t["rules"][k]}</p>{table(t, rows, cols, fans)}</section>'
    prev_c, next_c = order[i - 1], order[(i + 1) % len(order)]
    home_u = (base + PATHS[lang]["home"]) or "./"
    stats = "".join(f'<span class="stat t-{k}"><b>{ct["counts"][k]}</b>{t["tiers"][k] if ct["counts"][k] == 1 else t["tiers_pl"][k]}</span>' for k in TIERS if ct["counts"][k])
    refs = ref_links(ct, t)
    top = ct["clubs"][0]
    n_c = len(ct["clubs"])
    intro = (t["intro_one"] if n_c == 1 else t["intro_many"]).format(n=n_c, c=in_country(lang, ct).replace("in ", "") if lang == "en" else in_country(lang, ct)) + " " + t["intro_top"].format(x=e(top["name"]), r=top["rank"], s=top["total"])
    note = f'<p class="muted note">{t["fan_note_br" if ct["id"] == "br" else "fan_note"]}</p>' if fans else ""
    h1 = t["ct_h1"].format(c=in_country(lang, ct))
    body = f'''<main class="wrap page" id="conteudo">
  <a class="crumb" href="{home_u}#paises">{ICO["back"]}{t["back"]}</a>
  <header class="ct-head">
    <span class="fi fi-{ct["flag"]} huge" aria-hidden="true"></span>
    <div><h1>{e(h1)}</h1><div class="stats">{stats}</div><p class="ct-intro">{intro}</p></div>
  </header>
  {groups}{note}
  <section class="group"><h2>{t["refs"]}</h2><ul class="refs">{refs}</ul></section>
  <nav class="pager" aria-label="{t["nav_ct"]}">
    <a href="{ct_url(lang, prev_c, base)}">{ICO["back"]}{flag(prev_c)}{prev_c[lang]}</a>
    <a href="{ct_url(lang, next_c, base)}">{flag(next_c)}{next_c[lang]}{ICO["go"]}</a>
  </nav>
</main>'''
    title = h1 + " · " + t["short"]
    nodes = [{"@type": "ItemList", "name": h1, "numberOfItems": n_c, "itemListElement": [{"@type": "ListItem", "position": i, "name": c["name"]} for i, c in enumerate(ct["clubs"][:10], 1)]}]
    page(lang, "ct", ct, title, t["ct_desc"].format(c=in_country(lang, ct), n=n_c), body, nodes)


FAN_REFS = [("Ipsos-Ipec / O Globo", "www.cnnbrasil.com.br/esportes/futebol/pesquisa-revela-ranking-das-maiores-torcidas-do-brasil-em-2025-veja/"),
            ("AtlasIntel / ge", "www.itatiaia.com.br/esportes/futebol/futebol-nacional/nova-pesquisa-aponta-maiores-torcidas-do-brasil-em-2025-veja-ranking/")]


def ref_url(u):
    u = u.strip().split(" / ")[0].replace("https://", "")
    if u.startswith("wikipedia.org"):
        u = "en." + u
    return "https://" + u


def ref_links(ct, t):
    labels = [t["col_m"], t["col_c"], t["col_l"], t["col_n"], t["col_k"]]
    out = ""
    for l, u in zip(labels, ct["refs"]):
        if u:
            for part in u.split(" / "):
                out += f'<li><span>{l}</span> <a href="{e(ref_url(part))}" target="_blank" rel="noopener">{e(part.strip().replace("https://", ""))}</a></li>'
    if ct["id"] == "br":
        for name, u in FAN_REFS:
            out += f'<li><span>{t["col_fan"]}</span> <a href="https://{u}" target="_blank" rel="noopener">{name}</a></li>'
    return out


def criteria(lang):
    t = T[lang]
    items = "".join(f'<li>{badge(t, k)}<p>{t["rules"][k]}</p></li>' for k in TIERS)
    notes = "".join(f"<li>{n}</li>" for n in t["crit_notes"])
    body = f'''<main class="wrap page" id="conteudo">
  <header class="page-head"><p class="eyebrow">{t["site"]}</p><h1>{t["crit_title"]}</h1><p class="lead">{t["crit_lead"]}</p></header>
  <h2 class="h">{t["crit_tiers"]}</h2>
  <ul class="tiers-list">{items}</ul>
  <div class="prose"><h2>{t["crit_tie_h"]}</h2><p>{t["crit_tie"]}</p><h2>{t["crit_notes_h"]}</h2><ul>{notes}</ul></div>
</main>'''
    page(lang, "crit", None, f'{t["crit_page"]} · {t["short"]}', t["crit_desc"], body, cur="crit")


def about(lang):
    t = T[lang]
    base = "../" if lang == "en" else ""
    paras = "".join(f"<p>{p}</p>" for p in t["about_body"])
    cards = "".join(f'<a class="rec-card" href="{r["url"][lang]}" target="_blank" rel="noopener"><span class="rec-ico" aria-hidden="true">{r["icon"]}</span><span><strong>{r["name"][lang]}</strong><small>{r[lang]}</small></span></a>' for r in RECOMMENDED)
    body = f'''<main class="wrap page" id="conteudo">
  <header class="page-head"><p class="eyebrow">{e(t["site"])}</p><h1>{t["about_page"]}</h1><p class="lead">{t["about_lead"]}</p></header>
  <div class="prose">{paras}<h2>{t["about_how"]}</h2><p><a href="{link(lang, "crit", base)}">{t["crit_page"]}</a> · <a href="{link(lang, "src", base)}">{t["src_page"]}</a></p></div>
  <section><h2 class="h">{t["rec_h"]}</h2><div class="rec-grid">{cards}</div></section>
</main>'''
    page(lang, "about", None, f'{t["about_page"]} · {t["short"]}', t["about_desc"], body, cur="about")


def sources(lang):
    t = T[lang]
    base = "../" if lang == "en" else ""
    cards = f'<section class="src-card"><h2>{t["wc_src"]}</h2><ul class="refs"><li><a href="https://{WC_REF}" target="_blank" rel="noopener">{WC_REF}</a></li></ul></section>'
    for ct in ordered(lang):
        cards += f'<section class="src-card"><h2><a href="{ct_url(lang, ct, base)}">{flag(ct)}{ct[lang]}</a></h2><ul class="refs">{ref_links(ct, t)}</ul></section>'
    body = f'''<main class="wrap page" id="conteudo">
  <header class="page-head"><p class="eyebrow">{t["site"]}</p><h1>{t["src_title"]}</h1><p class="lead">{t["src_lead"]}</p></header>
  <div class="src-grid">{cards}</div>
</main>'''
    page(lang, "src", None, f'{t["src_page"]} · {t["short"]}', t["src_desc"], body, cur="src")


def extras():
    pairs = [(PATHS["pt"][k], PATHS["en"][k]) for k in ("home", "about", "crit", "src")] + [(PATHS["pt"]["ct"].format(s=ct["sp"]), PATHS["en"]["ct"].format(s=ct["se"])) for ct in COUNTRIES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    for pt_u, en_u in pairs:
        for u in (pt_u, en_u):
            sm += f'  <url><loc>{SITE}{u}</loc><lastmod>{UPDATED}</lastmod><xhtml:link rel="alternate" hreflang="pt-BR" href="{SITE}{pt_u}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}{en_u}"/></url>\n'
    sm += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm, encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8", newline="\n")
    (ROOT / "CNAME").write_text("biggestclubs.biblioverse.org\n", encoding="utf-8", newline="\n")
    t, en = T["pt"], T["en"]
    manifest = dict(name=t["site"], short_name="Maiores Clubes", description=t["desc"], lang="pt-BR", start_url="/", display="standalone", background_color="#F3F2F8", theme_color="#0B7A43", icons=[dict(src="/icon-192.png", sizes="192x192", type="image/png"), dict(src="/icon-512.png", sizes="512x512", type="image/png")])
    (ROOT / "site.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    (ROOT / "404.html").write_text(f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{t["nf_title"]} · {t["short"]}</title><meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/styles.css?v={VER}"></head>
<body><main class="wrap nf"><h1>404</h1><p class="lead">{t["nf_p"]}<br>{en["nf_p"]}</p><p><a class="go" href="/">{t["nf_cta"]}</a> <a class="go" href="/en/">{en["nf_cta"]}</a></p></main>{CF_SNIPPET}</body></html>
''', encoding="utf-8", newline="\n")


for lang in T:
    home(lang)
    criteria(lang)
    sources(lang)
    about(lang)
    order = ordered(lang)
    for i, ct in enumerate(order):
        country(lang, i, ct, order)
extras()
print("built", len(CLUBS), "clubs,", 2 * (len(COUNTRIES) + 3), "pages")
