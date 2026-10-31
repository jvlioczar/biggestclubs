"""Checks every generated page: metadata, hreflang, JSON-LD, headings and internal links.
Run: python tools/audit.py [--external]  (--external also requests each reference URL)"""
import json, re, sys, time, urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent.parent
SITE = "https://biggestclubs.biblioverse.org/"
VOID = {"meta", "link", "br", "img", "input", "hr", "path", "circle", "rect", "ellipse", "g-skip"}
problems, titles, descs, external = [], Counter(), Counter(), set()


class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.ids = Counter(); self.heads = []; self.links = []; self.metas = {}; self.alts = {}; self.h1 = 0; self.errors = []; self.title = ""; self._t = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids[a["id"]] += 1
        if tag == "title": self._t = True
        if re.fullmatch(r"h[1-6]", tag): self.heads.append(int(tag[1]))
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: self.metas.setdefault(k, a.get("content"))
        if tag == "link" and a.get("rel") == "alternate": self.alts[a["hreflang"]] = a["href"]
        if tag == "link" and a.get("rel") == "canonical": self.metas["canonical"] = a["href"]
        if tag not in VOID and not tag == "svg" and not self.stack[-1:] == ["svg"]: self.stack.append(tag)
        elif tag == "svg": self.stack.append("svg")
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == "svg" and tag != "svg": return
        if tag in VOID: return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unbalanced </{tag}> open={self.stack[-3:]}")
            if tag in self.stack:
                while self.stack and self.stack[-1] != tag: self.stack.pop()
        if self.stack: self.stack.pop()
    def handle_data(self, d):
        if self._t: self.title += d; self._t = False


pages = sorted(p for p in ROOT.rglob("*.html") if "tools" not in p.parts)
for p in pages:
    rel = p.relative_to(ROOT).as_posix()
    text = p.read_text(encoding="utf-8")
    d = Page(); d.feed(text)
    say = lambda m: problems.append(f"{rel}: {m}")
    for e in d.errors: say(e)
    for i, n in d.ids.items():
        if n > 1: say(f"duplicate id {i}")
    if rel == "404.html":
        continue
    titles[d.title] += 1; descs[d.metas.get("description")] += 1
    if not 25 <= len(d.title) <= 65: say(f"title length {len(d.title)}: {d.title}")
    n = len(d.metas.get("description") or "")
    if not 70 <= n <= 165: say(f"description length {n}")
    if d.heads.count(1) != 1: say(f"{d.heads.count(1)} h1")
    for a, b in zip(d.heads, d.heads[1:]):
        if b > a + 1: say(f"heading skip h{a}->h{b}"); break
    want = SITE + ("" if rel == "index.html" else rel.replace("index.html", ""))
    if d.metas.get("canonical") != want: say(f"canonical {d.metas.get('canonical')} != {want}")
    if d.metas.get("og:url") != want: say("og:url differs from canonical")
    if set(d.alts) != {"pt-BR", "en", "x-default"}: say(f"hreflang set {sorted(d.alts)}")
    if want not in d.alts.values(): say("hreflang has no self reference")
    for k in ["og:title", "og:description", "og:image", "og:image:alt", "twitter:card"]:
        if not d.metas.get(k): say(f"missing {k}")
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        try: json.loads(block)
        except ValueError as ex: say(f"bad JSON-LD {ex}")
    if "ld+json" not in text: say("no JSON-LD")
    for h in d.links:
        if h.startswith("http"):
            if "wikipedia" in h: external.add(h)
            continue
        path, _, frag = h.partition("#")
        q = (p.parent / path.split("?")[0]).resolve() if path else p
        if q.is_dir(): q = q / "index.html"
        if not q.exists(): say(f"broken link {h}"); continue
        if frag and f'id="{frag}"' not in q.read_text(encoding="utf-8"): say(f"broken anchor {h}")
    for key in ("en", "pt-BR"):
        target = d.alts.get(key, "").replace(SITE, "") or "index.html"
        if target.endswith("/"): target += "index.html"
        t = ROOT / target
        if not t.exists(): say(f"hreflang target missing {target}")
        elif f'href="{want}"' not in t.read_text(encoding="utf-8"): say(f"hreflang not reciprocal with {target}")

for what, c in (("title", titles), ("description", descs)):
    for v, n in c.items():
        if n > 1: problems.append(f"duplicate {what} x{n}: {v}")

sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
locs = re.findall(r"<loc>(.*?)</loc>", sm)
real = {SITE + ("" if p.relative_to(ROOT).as_posix() == "index.html" else p.relative_to(ROOT).as_posix().replace("index.html", "")) for p in pages if p.name != "404.html"}
for u in real - set(locs): problems.append(f"sitemap missing {u}")
for u in set(locs) - real: problems.append(f"sitemap extra {u}")

if "--external" in sys.argv:
    for u in sorted(external):
        time.sleep(1.5)
        try:
            req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "biggestclubs-audit/1.0"})
            r = urllib.request.urlopen(req, timeout=30)
            if r.status != 200: problems.append(f"external {r.status} {u}")
        except Exception as ex:
            problems.append(f"external {ex} {u}")

print(f"{len(pages)} pages, {len(external)} external references")
print("\n".join(problems) or "no problems")
