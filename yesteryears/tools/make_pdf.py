#!/usr/bin/env python3
"""Build the script + beats + image prompts PDF for an episode.
Usage: python3 make_pdf.py EPISODE_DIR "Episode title" OUTPUT.pdf
Needs script.txt, timeline.json and prompts.json in EPISODE_DIR (and image_prompts.md for the rule notes)."""
import json, html, os, re, sys, subprocess, tempfile
ep, title, out = sys.argv[1], sys.argv[2], sys.argv[3]
rows = json.load(open(os.path.join(ep, "timeline.json")))
P = json.load(open(os.path.join(ep, "prompts.json")))
assert len(P) == len(rows)
script = [p.strip() for p in open(os.path.join(ep, "script.txt")).read().split("\n") if p.strip()]
words = sum(len(p.split()) for p in script)
md = open(os.path.join(ep, "image_prompts.md")).read()
rules = [l for l in md.split("\n") if l.startswith("**Headwear rule:**")]
lock = re.findall(r"^\| (?!Story role|---)(.+?) \| (.+?) \|$", md, re.M)
e = html.escape
def tm(s): m, sec = divmod(s, 60); return f"{int(m):02d}:{sec:04.1f}"
css = """@page{size:A4;margin:18mm 16mm}body{font-family:"DejaVu Serif",Georgia,serif;color:#1A1A1A;font-size:10.5pt;line-height:1.5}
h1{color:#4A0E0E;font-size:34pt;margin:0}h2{color:#4A0E0E;font-size:18pt;border-bottom:2px solid #4A0E0E;padding-bottom:4px;margin-top:0;page-break-before:always}
.cover{height:240mm;display:flex;flex-direction:column;justify-content:center}.sub{color:#555;font-size:14pt;margin-top:8px}.meta{margin-top:30px;color:#444;font-size:11pt}
.script p{margin:0 0 9px;font-size:11pt}table{border-collapse:collapse;width:100%;font-size:9.5pt}td,th{border-bottom:1px solid #DDD4C2;padding:4px 6px;vertical-align:top;text-align:left}
th{background:#F2E8D5}td.n{width:34px;color:#4A0E0E;font-weight:bold}td.t{width:52px;color:#666}.beat{page-break-inside:avoid;border-top:1px solid #CFC4B0;padding:8px 0 6px}
.bh{color:#4A0E0E;font-weight:bold;font-size:11pt}.seg{font-style:italic;margin:3px 0 5px}.pr{font-size:8.8pt;color:#2A2A2A;background:#FBF7EF;border-left:3px solid #4A0E0E;padding:5px 8px;margin:4px 0}
.f{font-size:9pt;color:#333}.f b{color:#4A0E0E}"""
h = [f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>']
h.append(f'<div class="cover"><h1>yesteryears</h1><div class="sub">{e(title)}</div><div class="meta">Script · {len(rows)} Beats · Image Prompts<br>'
         f'{words:,} words · about {sum(r["dur"] for r in rows)/60:.1f} minutes at 2.4 words per second<br><br>Based on real history. Some characters are composites.</div></div>')
h.append('<h2>1. Script</h2><div class="script">' + "".join(f"<p>{e(p)}</p>" for p in script) + "</div>")
h.append('<h2>2. Beats</h2><table><tr><th>#</th><th>Start</th><th>Script segment</th></tr>' + "".join(
    f'<tr><td class="n">{r["beat"]:03d}</td><td class="t">{tm(r["start"])}</td><td>{e(r["text"])}</td></tr>' for r in rows) + "</table>")
h.append('<h2>3. Image Prompts</h2><p class="f">' + "".join(f'<b>Headwear rule:</b> {e(r.split("**", 2)[2].strip())}<br>' for r in rules)
         + "<b>Character lock:</b> " + " · ".join(f"{e(a)} = {e(b)}" for a, b in lock) + "</p>")
for p, r in zip(P, rows):
    h.append(f'<div class="beat"><div class="bh">Beat {p["n"]:03d} · {tm(r["start"])}</div><div class="seg">"{e(p["seg"])}"</div>'
             f'<div class="pr"><b>Image Prompt:</b> {e(p["prompt"])}</div><div class="f"><b>Camera:</b> {e(p["cam"])} · <b>Lighting:</b> {e(p["light"])} · '
             f'<b>Mood:</b> {e(p["mood"])}<br><b>Action:</b> {e(p["action"])}</div></div>')
h.append("</body></html>")
tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False); tmp.write("".join(h)); tmp.close()
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{tmp.name}');
await p.pdf({{path:{json.dumps(os.path.abspath(out))},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#888">yesteryears · page <span class=pageNumber></span> of <span class=totalPages></span></div>',
margin:{{top:'18mm',bottom:'18mm',left:'16mm',right:'16mm'}}}});await b.close();}})();"""
subprocess.run(["node", "-e", js], check=True)
print("wrote", out)
