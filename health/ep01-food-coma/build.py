#!/usr/bin/env python3
"""Build image prompts, timeline, beats list and PDF for this video.
Usage: python3 build.py            (run from this folder; needs script.txt, beats.json, shots.txt)
Writes prompts.json, image_prompts.md, timeline.json, timeline.csv, beats.txt, voiceover_script.txt and the PDF.
A beat in beats.json is either narration (a plain string) or a line spoken by a character: {"text": "...", "voice": "STOMACH"}.
Voices are defined in ../VOICES.md and must sound the same in every episode."""
import json, re, csv, html, os, subprocess, tempfile
TITLE = "Why Does Eating Make You Sleepy Instead of Giving You Energy?"
PDF = "Food_Coma_Script_Beats_Prompts.pdf"
WPS, MIN_DUR = 2.4, 1.2   # narration speed (words per second) and shortest beat on screen

STYLE = ("bright 2D cartoon animation still in a chunky, rounded character style: people with smooth solid matte-black skin and faces, large round white eyes "
         "with small black pupils, simple bold white brow and mouth lines for expression, rounded heads slightly large for the body, full proper arms, legs and "
         "mitten-like hands (never stick limbs), wearing bold, brightly coloured clothes with simple soft folds; thick clean outlines, soft gradient shading and "
         "gentle rim light giving a slightly glossy, 3D-like finish; detailed cartoon backgrounds with depth; cheerful light channel palette of clean white, warm cream, "
         "fresh mint, sky blue, sunny yellow, coral and leaf green as the default; darker colours used only where the scene itself calls for them, such as night "
         "or a dark room, with the characters still clear; organs and body parts always shown in their true natural anatomical colours in a clean, friendly "
         "medical-illustration look, never recoloured; no gore, open wounds, blood splatter or nudity; light, curious, gently comic tone; any on-screen words "
         "limited to the ones given in quotes; static 16:9 frame; bottom-right corner kept clear")
FIG = "a chunky rounded cartoon person with solid matte-black skin and face, big round white eyes with small black pupils and full arms, legs and hands"
C = {
 'YOU': f"you (the main character: {FIG}, short tufty black curly hair, __OUTFIT__)",
 'COWORKER': f"your coworker ({FIG}, auburn hair in a high round bun, a tailored coral blazer over a crisp white blouse, slim grey trousers and black heels)",
 'DOCTOR': f"a friendly doctor ({FIG}, short grey hair, white rectangular glasses, a white coat over a sky-blue shirt and a silver stethoscope)",
 'RESEARCHER': f"a researcher ({FIG}, a neat dark-purple bob, round white glasses and a white lab coat, holding a clipboard)",
 'MEN': f"two volunteer test subjects (each {FIG}): a lanky man with a thin grey moustache in a sky-blue T-shirt, and a stocky bald man with a short grey beard in a leaf-green T-shirt",
 'VAIDYA': f"a traditional Ayurvedic physician ({FIG}, a neat white beard, a small saffron mark on the forehead and a white cotton kurta with a cream shawl)",
 'STOMACH': "Stomach, a J-shaped stomach in its true natural colour, soft peachy pink with faint pinker folds, with big round white cartoon eyes, a simple mouth and little cartoon arms",
 'BRAIN': "Brain, a brain in its true natural colour, soft pinkish grey with clear folds, with big round white cartoon eyes and little cartoon arms",
 'PANCREAS': "Pancreas, a long, slightly lumpy pancreas in its true natural colour, pale creamy yellow-pink, with big round white cartoon eyes, a calm mouth and little cartoon arms",
 'GUT': "Intestines, the coiled small intestine in its true natural salmon pink framed by the large intestine in a slightly deeper dusty pink, with big round white cartoon eyes, a busy expression and little cartoon arms",
}
# The main character's look stays fixed (face, hair); the outfit fits the scenario. This episode is an office workday.
FORMAL = "a formal work outfit: a fitted navy suit jacket and trousers, a crisp white shirt, a sky-blue tie and polished black shoes"
OUTFIT = {'bedroom': "plain sky-blue pyjamas", 'breakroom': "the same formal work outfit with the suit jacket off and the tie loosened: crisp white shirt, sky-blue tie, navy trousers and black shoes"}
SHORT = {'YOU': 'you', 'COWORKER': 'your coworker', 'DOCTOR': 'the doctor', 'RESEARCHER': 'the researcher', 'MEN': 'the two men',
         'VAIDYA': 'an Ayurvedic physician', 'STOMACH': 'Stomach', 'BRAIN': 'Brain', 'PANCREAS': 'Pancreas', 'GUT': 'Intestines'}
S = {
 'cafe': ("a bright modern office canteen with wooden tables, lunch trays, plates of rice and curry, glasses of water and large windows", "soft midday daylight, warm tint"),
 'office': ("a modern open-plan office with desks, a laptop, a monitor, a coffee mug, sticky notes, a potted plant and a wall clock", "soft even daylight, pale afternoon tint"),
 'breakfast': ("a small home kitchen in the morning with a table, toast, a cup of coffee and a sunlit window", "bright morning daylight, fresh tint"),
 'body': ("a clean anatomy cutaway of the human torso on a bright white background, organs in their true natural colours: peachy-pink stomach, salmon-pink small intestine, dusty-pink large intestine, pale creamy-yellow pancreas, reddish-brown liver, red and blue blood vessels", "bright even light, clean white"),
 'brainhq': ("the inside of your head drawn as a bright, tidy control room with white walls, dials, levers, blinking screens and a big gauge labelled \"ALERTNESS\"", "bright even light, fresh sky-blue tint"),
 'blood': ("the inside of a blood vessel with smooth, light-pink-to-red walls in their natural colour, natural red disc-shaped blood cells and small white sugar cubes drifting along", "bright even light, clear rosy tint"),
 'graphic': ("a clean white infographic background with simple flat icons in bright colours", "bright even light, clean white"),
 'clockgfx': ("a large circular 24-hour clock graphic with a sun and a moon on its face, on a clean white background", "bright even light, clean white"),
 'lab': ("a bright modern university nutrition research room with a long table, pizza boxes, a scale, clipboards and a whiteboard", "bright even light, clean white"),
 'ayurveda': ("a traditional Indian courtyard with a brass oil lamp, a small cooking fire, brass vessels, herbs drying on a cloth and palm-leaf manuscripts", "warm daylight, saffron tint"),
 'park': ("a leafy city park path beside an office building, with benches and trees", "bright daylight, fresh green tint"),
 'bedroom': ("a dark modern bedroom at night with a rumpled bed, a glowing phone and a bedside clock", "dark blue night light with a bright phone glow on the face"),
 'breakroom': ("a quiet office break room with a soft grey couch, a cushion, a water cooler and a window with blinds", "soft warm ambient light"),
 'clinic': ("a calm modern doctor's consulting room with a desk, a computer, an examination couch and a simple digestive-system poster", "soft even light, clean pale-blue tint"),
 'phone': ("a smartphone held in front of a softly blurred office background", "soft screen glow, white tint"),
}
CAM = {'W': 'Wide establishing shot, eye level', 'M': 'Medium shot, eye level', 'C': 'Close-up, eye level', 'ECU': 'Extreme close-up',
       'TD': 'Top-down overhead shot', 'OTS': 'Over-the-shoulder shot'}

raw = json.load(open('beats.json'))
beats = [x if isinstance(x, str) else x['text'] for x in raw]
voices = ['NARRATOR' if isinstance(x, str) else x['voice'] for x in raw]
VOICE_NOTE = {v.split('|')[1].strip().strip('*'): v.split('|')[2].strip() for v in open('../VOICES.md') if v.startswith('| **')}
assert all(v in VOICE_NOTE for v in voices), 'a voice in beats.json is missing from ../VOICES.md'
script = [p.strip() for p in open('script.txt').read().split('\n') if p.strip()]
assert ' '.join(beats).split() == ' '.join(script).split(), "beats.json does not match script.txt"
def find(t): return next(i for i, s in enumerate(beats, 1) if s.startswith(t))
SHAKE = {find(t) for t in ("slipped a sleeping pill", "and that's why you feel sleepy", "But neither of these", "right when your body", "It's how much you eat")}
FADE = {find(t) for t in ("Okay, let's follow", "Think about your usual day", "Researchers actually", "Interestingly, people", "Maybe you've been sleeping", "So, why does eating")}
def motion(n): return "shake" if n in SHAKE else "fade" if n in FADE else ["push", "push", "pan", "push", "pull"][n % 5]

rows, t = [], 0.0
for line in open('shots.txt'):
    if not line.strip(): continue
    n, sc, cam, mood, act = line.rstrip('\n').split('|', 4); n = int(n)
    a = re.sub(r'^top-down view of\s+', '', act); short = act
    for k in C: a = a.replace('{' + k + '}', C[k].replace('__OUTFIT__', OUTFIT.get(sc, FORMAL))); short = short.replace('{' + k + '}', SHORT[k])
    env, light = S[sc]
    d = round(max(MIN_DUR, len(beats[n - 1].split()) / WPS), 3)
    rows.append(dict(n=n, seg=beats[n - 1], voice=voices[n - 1], start=round(t, 3), dur=d, motion=motion(n), scene=sc, image=f"images/beat_{n:03d}.png",
                     prompt=f"{CAM[cam]} of {a}. Setting: {env}. Lighting: {light}. Mood: {mood}. Style: {STYLE}.",
                     cam=CAM[cam], light=light, mood=mood, action=short[0].upper() + short[1:]))
    t += d
assert [r['n'] for r in rows] == list(range(1, len(beats) + 1)), "shots.txt and beats.json are out of step"

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
LOCK = [("All people", FIG), ("You", "short tufty black curly hair; outfit fits the scenario: " + FORMAL + " at work, " + OUTFIT['bedroom'] + " in bed, jacket off and tie loosened for the break-room nap"), ("Your coworker", C['COWORKER'].split('(', 1)[1].rstrip(')')),
        ("Organ characters", "Stomach, Brain, Pancreas and Intestines: true natural organ colours, big round white cartoon eyes and little arms")]
with open('image_prompts.md', 'w') as f:
    f.write(f"# {TITLE} — Image Prompts\n\n{len(rows)} beats · ~3–5 s each · one locked visual style · recurring characters described the same way in every prompt\n\n"
            f"**Visual style:** {STYLE}.\n\n**Character lock**\n\n| Character | Fixed description |\n|---|---|\n"
            + "".join(f"| {a} | {b} |\n" for a, b in LOCK) + "\n")
    for r in rows:
        f.write(f"## Beat {r['n']}\n**[Script Segment]**" + (f" **[{r['voice']} speaks]**" if r['voice'] != 'NARRATOR' else '') + f" \"{r['seg']}\"\n\n**Image Prompt:** {r['prompt']}\n\n- **Camera Angle:** {r['cam']}\n"
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
    h.append(f'<div class="beat"><div class="bh">Beat {r["n"]:03d} · {tm(r["start"])}</div><div class="seg">' + (f'<b>[{e(r["voice"])} speaks]</b> ' if r['voice'] != 'NARRATOR' else '') + f'"{e(r["seg"])}"</div>'
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
