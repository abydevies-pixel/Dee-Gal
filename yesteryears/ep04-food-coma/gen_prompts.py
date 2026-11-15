import json, re
beats=json.load(open('beats.json'))
STYLE=("2D digital cartoon illustration in the big-head stick-figure style: oversized semi-realistic caricature heads with fine wrinkle and feature linework and flat skin tones, attached to minimal thick solid-black stick-figure bodies with no hands and no clothing volume; highly detailed hand-drawn present-day background with clean black ink outlines and flat muted colors; muted palette of soft teal, warm beige, mustard yellow, tomato red, lettuce green, slate grey and cream; deadpan light-comedy science-explainer tone; anatomy shown only as simple friendly cartoon diagrams, no realistic organs, no gore, blood or nudity; any on-screen words limited to the ones given in quotes; static 16:9 frame; bottom-right corner kept clear")
C={
'YOU':"you (mascot: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, bareheaded, a teal office lanyard at the neck, on a solid black stick body with no hands)",
'COWORKER':"your coworker (adult woman variant: a slimmer oval oversized head, dark brown hair parted in the middle and gathered into a bun tied with an oxblood ribbon, lashes, half-lidded deadpan eyes and tinted lips, a teal office lanyard at the neck, on a solid black stick body with no hands)",
'DOCTOR':"a friendly doctor, a middle-aged man with short grey hair, rectangular glasses, a white coat collar and a stethoscope at the neck, on a solid black stick body with no hands",
'RESEARCHER':"a researcher with a neat dark bob, round glasses and a white lab-coat collar, a clipboard balanced at the stick end of one arm, on a solid black stick body with no hands",
'MEN':"two volunteer test subjects, a lanky man with a thin moustache and a stocky bald man with a short beard, on solid black stick bodies with no hands",
'VAIDYA':"a traditional Ayurvedic physician, an elderly Indian man with a neat white beard, a sandalwood mark on the forehead and a white cotton shawl at the neck, on a solid black stick body with no hands",
'STOMACH':"Stomach, a cartoon pink J-shaped stomach character with a simple deadpan face, small dot eyes and thin black stick arms",
'BRAIN':"Brain, a cartoon pink brain character with half-lidded deadpan eyes and thin black stick arms",
'PANCREAS':"Pancreas, a cartoon pale-yellow leaf-shaped pancreas character with a calm face and thin black stick arms",
'GUT':"Intestines, a cartoon coiled pink intestine character with a busy, focused face and thin black stick arms",
}
S={
'cafe':("a bright modern office canteen with wooden tables, lunch trays, plates of rice and curry, glasses of water and large windows","flat even daylight, warm midday tint"),
'office':("a modern open-plan office with desks, a laptop, a monitor, a coffee mug, sticky notes, a potted plant and a wall clock","flat even ambient light, pale afternoon tint"),
'breakfast':("a small home kitchen in the morning with a table, toast, a cup of coffee and a sunlit window","flat even daylight, fresh morning tint"),
'body':("a simplified cartoon anatomy cutaway of the human torso on a plain cream background, showing the stomach, intestines and pancreas as flat friendly shapes","flat even light, clean cream tint"),
'brainhq':("the inside of your head drawn as a cozy control room with dials, levers, blinking screens and a big gauge labelled \"ALERTNESS\"","flat even ambient light, soft teal tint"),
'blood':("the inside of a cartoon blood vessel with round red blood cells and small sugar cubes drifting along","flat even ambient light, warm rosy tint"),
'graphic':("a plain cream infographic background with simple flat icons and thin black ink outlines","flat even light, clean cream tint"),
'clockgfx':("a large circular 24-hour clock graphic with a sun and a moon on its face, on a plain cream background","flat even light, clean cream tint"),
'lab':("a modern university nutrition research room with a long table, pizza boxes, a scale, clipboards and a whiteboard","flat even ambient light, cool clinical white tint"),
'ayurveda':("a traditional Indian courtyard with a brass oil lamp, a small cooking fire, brass vessels, herbs drying on a cloth and palm-leaf manuscripts","flat even daylight, warm saffron tint"),
'park':("a leafy city park path beside an office building, with benches and trees","flat even daylight, fresh green tint"),
'bedroom':("a dark modern bedroom at night with a rumpled bed, a glowing phone and a bedside clock","flat even ambient light, dim blue night tint with phone glow"),
'breakroom':("a quiet office break room with a soft grey couch, a cushion, a water cooler and a window with blinds","flat even ambient light, soft warm tint"),
'clinic':("a calm modern doctor's consulting room with a desk, a computer, an examination couch and a simple digestive-system poster","flat even ambient light, clean pale-blue tint"),
'phone':("a smartphone held in front of a softly blurred office background","flat even screen light, soft white tint"),
}
SHORT={'YOU':'you','COWORKER':'your coworker','DOCTOR':'the doctor','RESEARCHER':'the researcher','MEN':'the two men','VAIDYA':'an Ayurvedic physician',
'STOMACH':'Stomach','BRAIN':'Brain','PANCREAS':'Pancreas','GUT':'Intestines'}
CAM={'W':'Wide establishing shot, eye level','M':'Medium shot, eye level','C':'Close-up, eye level','ECU':'Extreme close-up','HA':'High-angle shot looking down','TD':'Top-down overhead shot','LA':'Low-angle shot looking up','POV':'First-person point-of-view shot','OTS':'Over-the-shoulder shot'}
rows=[]
for line in open('shots.txt'):
    if not line.strip(): continue
    n,sc,cam,mood,act=line.rstrip('\n').split('|',4)
    n=int(n)
    a=re.sub(r'^(top-down view of)\s+','',act)
    for k in C: a=a.replace('{'+k+'}',C[k])
    short=act
    for k in C: short=short.replace('{'+k+'}',SHORT[k])
    env,light=S[sc]
    prompt=f"{CAM[cam]} of {a}. Setting: {env}. Lighting: {light}. Mood: {mood}. Style: {STYLE}."
    rows.append(dict(n=n,seg=beats[n-1],prompt=prompt,cam=CAM[cam],light=light,mood=mood,action=short[0].upper()+short[1:]))
assert [r['n'] for r in rows]==list(range(1,len(beats)+1)), "mismatch"
json.dump(rows,open('prompts.json','w'),indent=1,ensure_ascii=False)
with open('image_prompts.md','w') as f:
    f.write(f"# Why Does Eating Make You Sleepy Instead of Giving You Energy? — Image Prompts\n\n{len(rows)} beats · ~3–5 s each · Visual Style Profile locked · Characters locked to the Yesteryears character sheets\n\n"
  "**Headwear rule:** present-day setting, so nobody wears a hat. You are always bareheaded with a teal office lanyard, which marks you as the same office worker in every scene.\n\n"
  "**Character lock**\n\n| Story role | Sheet |\n|---|---|\n| You | Mascot |\n| Your coworker | Adult woman variant |\n"
  "| Doctor, researcher, the two pizza volunteers, Ayurvedic physician, organ characters (Stomach, Brain, Pancreas, Intestines) | Not on a sheet (fixed descriptions) |\n\n")
    for r in rows:
        f.write(f"## Beat {r['n']}\n**[Script Segment]** \"{r['seg']}\"\n\n**Image Prompt:** {r['prompt']}\n\n- **Camera Angle:** {r['cam']}\n- **Lighting:** {r['light']}\n- **Mood:** {r['mood']}\n- **Action:** {r['action']}\n\n")
print(len(rows))
