"""Renders the favicon set and og-image.png with headless Edge. Run: python tools/icons.py"""
import struct, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
LOGO = (ROOT / "favicon.svg").read_text(encoding="utf-8")

OG = f'''<!doctype html><meta charset="utf-8"><style>
body {{ margin:0; width:1200px; height:630px; display:flex; align-items:center; gap:56px; padding:0 80px; box-sizing:border-box; overflow:hidden;
  background:linear-gradient(125deg,#14213D,#1B2C57 60%,#2B2470); color:#fff; font-family:"Segoe UI",system-ui,sans-serif; }}
svg {{ width:250px; flex:none; }} h1 {{ font-size:76px; line-height:1.03; margin:0; font-weight:900; }} b {{ color:#FFC94D; }}
p {{ font-size:30px; margin:26px 0 0; opacity:.9; }}</style>{LOGO}
<div><h1>Maiores Clubes <b>do Mundo</b></h1><p>GOATs, Lendas e Estrelas de 16 países, por títulos</p></div>'''


OG_EN = OG.replace("<h1>Maiores Clubes <b>do Mundo</b></h1>", "<h1>The World's <b>Biggest Clubs</b></h1>").replace("GOATs, Lendas e Estrelas de 16 países, por títulos", "GOATs, Legends and Stars from 16 countries, by titles")


OG_EN = OG.replace("<h1>Maiores Clubes <b>do Mundo</b></h1>", "<h1>The World's <b>Biggest Clubs</b></h1>").replace("GOATs, Lendas e Estrelas de 16 países, por títulos", "GOATs, Legends and Stars from 16 countries, by titles")


def shot(html, out, w, h):
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "p.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                        f"--user-data-dir={d}/profile", f"--screenshot={out}", f"--window-size={w},{h}", src.as_uri()],
                       check=True, capture_output=True, timeout=60)


def icon(size):
    return f'<!doctype html><style>html,body{{margin:0;background:transparent}}svg{{display:block;height:{size}px;width:{size}px}}</style>{LOGO}'


for name, size in [("icon-512.png", 512), ("icon-192.png", 192), ("apple-touch-icon.png", 180), ("_32.png", 32)]:
    shot(icon(size), ROOT / name, size, size)
shot(OG, ROOT / "og-image.png", 1200, 630)
shot(OG_EN, ROOT / "og-image-en.png", 1200, 630)
shot(OG_EN, ROOT / "og-image-en.png", 1200, 630)

# ICO wrapping the 32px PNG
png = (ROOT / "_32.png").read_bytes()
(ROOT / "favicon.ico").write_bytes(struct.pack("<HHH", 0, 1, 1) + struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(png), 22) + png)
(ROOT / "_32.png").unlink()
