"""Shared build engine for every health-channel episode.
An episode's build.py sets its config (title, scenes, outfits, extra characters, motion cues) and calls build(globals()).
Reads script.txt, beats.json and shots.txt from the episode folder; writes prompts.json, image_prompts.md, timeline.json,
timeline.csv, beats.txt, voiceover_script.txt and the PDF.
- A beat in beats.json is narration (a plain string) or a spoken line: {"text": "...", "voice": "STOMACH"} (voices in VOICES.md).
- In shots.txt, {YOU} uses the scene's outfit for this episode; {YOU:gym} forces an outfit from channel.OUTFITS."""
import json, re, csv, html, os, subprocess, tempfile
from channel import PEOPLE_STYLE, ORGAN_STYLE, style_for, OUTFITS
HERE = os.path.dirname(os.path.abspath(__file__))
WPS, MIN_DUR = 2.4, 1.2   # narration speed (words per second) and shortest beat on screen
CAM = {'W': 'Wide establishing shot, eye level', 'M': 'Medium shot, eye level', 'C': 'Close-up, eye level', 'ECU': 'Extreme close-up',
       'TD': 'Top-down overhead shot', 'OTS': 'Over-the-shoulder shot'}

def build(cfg):
    TITLE, PDF, C, SHORT, S, LOCK = cfg['TITLE'], cfg['PDF'], cfg['C'], cfg['SHORT'], cfg['S'], cfg['LOCK']
    OUTFIT, DEFAULT_OUTFIT, SHAKE_AT, FADE_AT = cfg['OUTFIT'], cfg['DEFAULT_OUTFIT'], cfg['SHAKE_AT'], cfg['FADE_AT']
    raw = json.load(open('beats.json'))
    beats = [x if isinstance(x, str) else x['text'] for x in raw]
    voices = ['NARRATOR' if isinstance(x, str) else x['voice'] for x in raw]
    VOICE_NOTE = {v.split('|')[1].strip().strip('*'): v.split('|')[2].strip() for v in open(os.path.join(HERE, 'VOICES.md')) if v.startswith('| **')}
    assert all(v in VOICE_NOTE for v in voices), 'a voice in beats.json is missing from ../VOICES.md'
    script = [p.strip() for p in open('script.txt').read().split('\n') if p.strip()]
    assert ' '.join(beats).split() == ' '.join(script).split(), "beats.json does not match script.txt"
    def find(t): return next(i for i, s in enumerate(beats, 1) if s.startswith(t))
    SHAKE = {find(t) for t in SHAKE_AT}
    FADE = {find(t) for t in FADE_AT}
    def motion(n): return "shake" if n in SHAKE else "fade" if n in FADE else ["push", "push", "pan", "push", "pull"][n % 5]

    rows, t = [], 0.0
    for line in open('shots.txt'):
        if not line.strip(): continue
        n, sc, cam, mood, act = line.rstrip('\n').split('|', 4); n = int(n)
        a = re.sub(r'^top-down view of\s+', '', act); short = act
        a = re.sub(r'\{YOU:(\w+)\}', lambda m: C['YOU'].replace('__OUTFIT__', OUTFITS[m.group(1)]), a); short = re.sub(r'\{YOU:\w+\}', '{YOU}', short)
        for k in C: a = a.replace('{' + k + '}', C[k].replace('__OUTFIT__', OUTFITS[OUTFIT.get(sc, DEFAULT_OUTFIT)])); short = short.replace('{' + k + '}', SHORT[k])
        env, light = S[sc]
        d = round(max(MIN_DUR, len(beats[n - 1].split()) / WPS), 3)
        rows.append(dict(n=n, seg=beats[n - 1], voice=voices[n - 1], start=round(t, 3), dur=d, motion=motion(n), scene=sc, image=f"images/beat_{n:03d}.png",
                         prompt=f"{CAM[cam]} of {a}. Setting: {env}. Lighting: {light}. Mood: {mood}. Style: {style_for(sc)}.",
                         cam=CAM[cam], light=light, mood=mood, action=short[0].upper() + short[1:]))
        t += d
    assert [r['n'] for r in rows] == list(range(1, len(beats) + 1)), "shots.txt and beats.json are out of step"

    def q(t): return t if t.startswith('"') else f'"{t}"'
    def tm(s): m, sec = divmod(s, 60); return f"{int(m):02d}:{sec:04.1f}"
    def ts(s): h, r = divmod(s, 3600); m, x = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{x:06.3f}"
    json.dump([{k: r[k] for k in ('n', 'seg', 'prompt', 'cam', 'light', 'mood', 'action')} for r in rows], open('prompts.json', 'w'), indent=1, ensure_ascii=False)
    json.dump([dict(beat=r['n'], start=r['start'], dur=r['dur'], text=r['seg'], voice=r['voice'], motion=r['motion'], scene=r['scene'], image=r['image']) for r in rows],
              open('timeline.json', 'w'), indent=1, ensure_ascii=False)
    with open('timeline.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(["beat", "start", "end", "duration_s", "voice", "motion", "scene", "image", "script_segment"])
        for r in rows: w.writerow([r['n'], ts(r['start']), ts(r['start'] + r['dur']), r['dur'], r['voice'], r['motion'], r['scene'], r['image'], r['seg']])
    with open('beats.txt', 'w') as f:
        f.write(f"{TITLE.upper()} - {len(rows)} BEATS\n\n" + "".join(f"{r['n']:03d}  [{tm(r['start'])}]  " + (f"[{r['voice']}] " if r['voice'] != 'NARRATOR' else '') + f"{r['seg']}\n" for r in rows))
    # Voiceover script: narration runs on; each character line is pulled out with its voice direction so it can be recorded or generated separately.
    with open('voiceover_script.txt', 'w') as f:
        f.write(f"{TITLE} - VOICEOVER SCRIPT\nNarration is the default voice. Character lines are marked; keep each character's voice exactly as defined in ../VOICES.md.\n\n")
        cur = []
        for r in rows:
            if r['voice'] == 'NARRATOR': cur.append(r['seg']); continue
            if cur: f.write('NARRATOR:\n' + ' '.join(cur) + '\n\n'); cur = []
            f.write(f"{r['voice']} (beat {r['n']:03d}) - {VOICE_NOTE[r['voice']]}\n{r['seg']}\n\n")
        if cur: f.write('NARRATOR:\n' + ' '.join(cur) + '\n')
    with open('image_prompts.md', 'w') as f:
        f.write(f"# {TITLE} — Image Prompts\n\n{len(rows)} beats · ~3–5 s each · one locked visual style · recurring characters described the same way in every prompt\n\n"
                f"**Visual style, people scenes:** {PEOPLE_STYLE}.\n\n**Visual style, inside-the-body scenes:** {ORGAN_STYLE}.\n\n**Character lock**\n\n| Character | Fixed description |\n|---|---|\n"
                + "".join(f"| {a} | {b} |\n" for a, b in LOCK) + "\n")
        for r in rows:
            f.write(f"## Beat {r['n']}\n**[Script Segment]**" + (f" **[{r['voice']} speaks]**" if r['voice'] != 'NARRATOR' else '') + f" {q(r['seg'])}\n\n**Image Prompt:** {r['prompt']}\n\n- **Camera Angle:** {r['cam']}\n"
                    f"- **Lighting:** {r['light']}\n- **Mood:** {r['mood']}\n- **Action:** {r['action']}\n\n")

    e = html.escape; words = sum(len(p.split()) for p in script)
    css = """@page{size:A4;margin:18mm 16mm}body{font-family:"DejaVu Sans",Arial,sans-serif;color:#1F2430;font-size:10pt;line-height:1.5}
    h1{color:#1E5B8C;font-size:28pt;margin:0;line-height:1.15}h2{color:#1E5B8C;font-size:17pt;border-bottom:2px solid #1E5B8C;padding-bottom:4px;margin-top:0;page-break-before:always}
    .cover{height:240mm;display:flex;flex-direction:column;justify-content:center}.meta{margin-top:30px;color:#444;font-size:11pt}
    .script p{margin:0 0 9px;font-size:10.5pt}table{border-collapse:collapse;width:100%;font-size:9.3pt}td,th{border-bottom:1px solid #DCE3EA;padding:4px 6px;vertical-align:top;text-align:left}
    th{background:#EAF2F8}td.n{width:34px;color:#1E5B8C;font-weight:bold}td.t{width:52px;color:#666}.beat{page-break-inside:avoid;border-top:1px solid #DCE3EA;padding:8px 0 6px}
    .bh{color:#1E5B8C;font-weight:bold;font-size:10.5pt}.seg{font-style:italic;margin:3px 0 5px}.pr{font-size:8.6pt;background:#F5F9FC;border-left:3px solid #1E5B8C;padding:5px 8px;margin:4px 0}
    .f{font-size:8.8pt;color:#333}.f b{color:#1E5B8C}"""
    h = [f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>',
         f'<div class="cover"><h1>{e(TITLE)}</h1><div class="meta">Script · {len(rows)} Beats · Image Prompts<br>{words:,} words · about {t/60:.1f} minutes at {WPS} words per second'
         '<br><br>Based on current research. Not medical advice.</div></div>',
         '<h2>1. Script</h2><div class="script">' + "".join(f"<p>{e(p)}</p>" for p in script) + "</div>",
         '<h2>2. Beats</h2><table><tr><th>#</th><th>Start</th><th>Script segment</th></tr>'
         + "".join(f'<tr><td class="n">{r["n"]:03d}</td><td class="t">{tm(r["start"])}</td><td>' + (f'<b>[{e(r["voice"])}]</b> ' if r['voice'] != 'NARRATOR' else '') + f'{e(r["seg"])}</td></tr>' for r in rows) + "</table>",
         f'<h2>3. Image Prompts</h2><p class="f"><b>Character lock:</b> ' + " · ".join(f"<b>{e(a)}:</b> {e(b)}" for a, b in LOCK) + "</p>"]
    for r in rows:
        h.append(f'<div class="beat"><div class="bh">Beat {r["n"]:03d} · {tm(r["start"])}</div><div class="seg">' + (f'<b>[{e(r["voice"])} speaks]</b> ' if r['voice'] != 'NARRATOR' else '') + f'{e(q(r["seg"]))}</div>'
                 f'<div class="pr"><b>Image Prompt:</b> {e(r["prompt"])}</div><div class="f"><b>Camera:</b> {e(r["cam"])} · <b>Lighting:</b> {e(r["light"])} · '
                 f'<b>Mood:</b> {e(r["mood"])}<br><b>Action:</b> {e(r["action"])}</div></div>')
    h.append("</body></html>")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False); tmp.write("".join(h)); tmp.close()
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://{tmp.name}');
    await p.pdf({{path:{json.dumps(os.path.abspath(PDF))},format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',
    footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#888">page <span class=pageNumber></span> of <span class=totalPages></span></div>',
    margin:{{top:'18mm',bottom:'18mm',left:'16mm',right:'16mm'}}}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True); os.unlink(tmp.name)
    print(f"{len(rows)} beats, {t/60:.1f} min; wrote prompts, timeline, beats.txt, voiceover_script.txt and {PDF}")

