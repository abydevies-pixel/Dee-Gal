import json, re
beats=json.load(open('beats.json'))
STYLE=("2D digital cartoon illustration in the big-head stick-figure style: oversized semi-realistic caricature heads with fine wrinkle and feature linework and flat skin tones, attached to minimal thick solid-black stick-figure bodies with no hands and no clothing volume; highly detailed, period-accurate hand-drawn background with clean black ink outlines and flat muted colors; desaturated 1730s Prussian palette of Prussian blue, faded red, brass gold, stone grey, flour white, parchment beige and earth brown; deadpan dark-comedy tone; no gore, no visible wounds, blood or nudity; static 16:9 frame; bottom-right corner kept clear")
C={
'BABY':"you as a newborn baby, a tiny version of the boy variant with a tuft of messy brown hair and no cap",
'YOU5':"you at age 5 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a solid black stick body with no hands, noticeably taller than other children)",
'YOU10':"you at age 10 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a solid black stick body with no hands, noticeably taller than other children)",
'YOU14':"you at age 14 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a solid black stick body with no hands, noticeably taller than other children)",
'YOU':"you (mascot: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, __HAT__on a very tall solid black stick body with no hands, a head taller than everyone around him)",
'YOUCAP':"you in uniform (mascot: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, wearing the tall pointed brass-and-red grenadier cap of the Potsdam Giants, with a Prussian-blue collar and brass buttons at the neck, on a very tall solid black stick body with no hands, a head taller than everyone around him)",
'YOU28':"you at age 28 (mascot, worn down: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, heavier stubble and tired lines under the eyes, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, bareheaded, on a very tall solid black stick body with no hands, a head taller than everyone around him)",
'MOTHER':"your mother (adult woman variant: a slimmer oval oversized head, dark brown hair parted in the middle and gathered into a bun tied with an oxblood ribbon, lashes, half-lidded deadpan eyes and tinted lips, on a short solid black stick body with no hands)",
'FATHER':"your father, a short stocky miller with a round flour-dusted face, a bushy brown moustache and a bald patch, on a short solid black stick body with no hands",
'FATHEROLD':"your father, ten years older, a short stocky miller with a round lined face, a grey moustache and a bald head, on a short, slightly bent solid black stick body with no hands",
'SEAMUS':"Seamus, an Irish giant even taller than you, with flaming red hair, a crooked nose, freckles and a wide grin, on a very tall solid black stick body with no hands",
'KING':"King Frederick William I, a short heavy man with a puffy red face, small sharp eyes and a short powdered wig tied with a black ribbon, on a short stout solid black stick body with no hands",
'SERGEANT':"a short red-faced sergeant with a bristling black moustache and furious eyes, on a short solid black stick body with no hands",
'RECRUITER':"a friendly well-dressed recruiter with a smooth smile, a neat powdered wig and narrow watchful eyes, on a solid black stick body with no hands",
'CLERK':"a thin bespectacled clerk with ink-stained fingers drawn at the stick ends and a bored face, on a solid black stick body with no hands",
'OFFICER':"a Prussian officer with a powdered wig, a thin moustache and a gold-trimmed collar, on a solid black stick body with no hands",
'SHEPHERD':"a huge young shepherd from Hanover with shaggy blond hair and a frightened face, on a very tall solid black stick body with no hands",
'STUDENT':"a huge young student from Leipzig with neat dark hair, round spectacles and a panicked face, on a very tall solid black stick body with no hands",
'BLACKSMITH':"the village blacksmith, a burly man with a thick black beard and soot-smudged cheeks, on a stocky solid black stick body with no hands",
'OLDWOMAN':"an old townswoman (old woman variant: an oversized wrinkled head, a white ruffled linen mob cap with an oxblood band, grey hair in a bun, round spectacles, thick pale-grey brows and tinted lips, on a stooped solid black stick body with no hands)",
'FREDERICK':"the young Frederick the Great, a slim man with sharp features, large clear eyes and a powdered wig, on a solid black stick body with no hands",
'VISITORS':"present-day museum visitors with oversized heads and modern hairstyles, on solid black stick bodies with no hands",
}
S={
'mill_ext':("a stone watermill on a slow brown river in an 1710s Saxon village, with a turning wheel, flour sacks, a cart and green fields","flat even daylight, soft warm tint"),
'kitchen':("a low-beamed mill kitchen with a stone hearth, loaves of bread, flour sacks, a low wooden doorway and a small brass bell hanging above it","flat even ambient light, warm hearth-yellow tint"),
'village':("a small Saxon village square in the 1710s with half-timbered houses, a church, a well and villagers","flat even daylight, warm tint"),
'orchard':("an apple orchard beside the mill with tall trees heavy with red apples","flat even daylight, fresh green tint"),
'road':("a dirt country road in 1730s Saxony winding through fields and hedges toward the horizon","flat even daylight, soft overcast tint"),
'market':("a busy 1730s Saxon market town square with stalls, carts and merchants","flat even daylight, warm stone tint"),
'inn':("a dim 1730s country inn with wooden benches, beer mugs, a fireplace and smoke-darkened beams","flat even ambient light, warm firelight tint"),
'cart_road':("a rough wooden cart on a dark country road at night, lit by a single lantern","flat even ambient light, dim blue night tint with lantern glow"),
'palace':("a grand 1730s Prussian palace room with a throne, black eagle banners, paintings of soldiers and a polished floor","flat even ambient light, cool blue-grey tint"),
'potsdam':("a 1730s Potsdam street of orderly baroque houses, barracks and churches, with soldiers and townspeople","flat even daylight, cool stone-grey tint"),
'measure':("a plain 1730s army recruitment room in Potsdam with a long wooden measuring rod on the wall, a clerk's desk with a thick ledger and a table of food","flat even ambient light, pale grey tint"),
'mirror':("a barracks dressing room with a tall standing mirror and uniforms hanging on pegs","flat even ambient light, cool grey tint"),
'barracks':("a long 1730s Potsdam barracks room with rows of wooden bunks, a carved wooden beam above the door, small windows and a candle","flat even ambient light, dim warm candle tint"),
'parade':("a vast Potsdam parade ground in the 1730s with rows of giant soldiers in formation and the palace behind","flat even daylight, cool grey tint"),
'drill':("a bare Potsdam parade ground at dawn in the 1730s with packed earth, a drummer and barracks around the edges","flat even overcast daylight, cold grey tint"),
'easel':("a palace painting room in the 1730s with an easel, paints and unfinished portraits of tall soldiers","flat even ambient light, warm amber tint"),
'bedroom':("a 1730s royal bedroom with a large curtained bed, low doorways, a fireplace and portraits of soldiers on the walls","flat even ambient light, dim warm tint"),
'checkpoint':("a snowy roadside checkpoint in 1730s Prussia with a wooden barrier and a guard hut","flat even overcast daylight, cold white tint"),
'infirmary':("a plain 1730s army infirmary with narrow beds, rough blankets and whitewashed walls","flat even ambient light, pale cold tint"),
'graveyard':("a bleak snowy field outside the Potsdam city walls with bare trees and a fresh mound of earth","flat even overcast daylight, cold grey tint"),
'gallery':("a present-day palace gallery with polished floors, velvet ropes and large old painted portraits of giant soldiers in grenadier caps","flat even ambient light, soft museum-cream tint"),
}
OUTDOOR_CIV={'mill_ext','village','orchard','road','market','cart_road'}
def variant(k,sc):
    d=C[k]
    if k=='YOU': return d.replace('__HAT__',"wearing a worn brown felt cap, " if sc in OUTDOOR_CIV else "bareheaded, his messy brown hair fully visible, ")
    if k in('YOU5','YOU10','YOU14'):
        return d if sc in OUTDOOR_CIV else d.replace("a messy brown fringe under a flat grey tweed cap","messy brown hair with no cap").replace("boy variant:","boy variant, cap off indoors:")
    return d
BAD={70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,100,231,232,233,246,247,248,249,250,251,252,253,254,255,256,309,310,311,312,313,314}
SHORT={'YOU':'you','YOUCAP':'you (in uniform)','YOU5':'you (age 5)','YOU10':'you (age 10)','YOU14':'you (age 14)','YOU28':'you (age 28)','BABY':'you as a baby','MOTHER':'your mother','FATHER':'your father','FATHEROLD':'your father','SEAMUS':'Seamus','KING':'the King','SERGEANT':'the sergeant','RECRUITER':'the recruiter','CLERK':'the clerk','OFFICER':'the officer','SHEPHERD':'the shepherd','STUDENT':'the student','BLACKSMITH':'the blacksmith','OLDWOMAN':'an old woman','FREDERICK':'Frederick','VISITORS':'visitors'}
CAM={'W':'Wide establishing shot, eye level','M':'Medium shot, eye level','C':'Close-up, eye level','ECU':'Extreme close-up','HA':'High-angle shot looking down','TD':'Top-down overhead shot','LA':'Low-angle shot looking up','POV':'First-person point-of-view shot','OTS':'Over-the-shoulder shot'}
fix={93:"dazed spiral eyes"}
rows=[]
for line in open('shots.txt'):
    if not line.strip(): continue
    n,sc,cam,mood,act=line.rstrip('\n').split('|',4)
    n=int(n)
    act=act.replace('with X-eyes for a moment','with dazed spiral eyes')
    import re
    a=re.sub(r'^(extreme close-up of|close-up of|high-angle view of|top-down view of|low-angle view of|wide view of|extreme detail on|a cutaway of)\s+','',act)
    for k in sorted(C,key=len,reverse=True): a=a.replace('{'+k+'}',variant(k,'indoor' if n in BAD else sc))
    short=act
    for k in C: short=short.replace('{'+k+'}',SHORT.get(k,k.lower()))
    env,light=S[sc]
    prompt=f"{CAM[cam]} of {a}. Setting: {env}. Lighting: {light}. Mood: {mood}. Style: {STYLE}."
    rows.append(dict(n=n,seg=beats[n-1],prompt=prompt,cam=CAM[cam],light=light,mood=mood,action=short[0].upper()+short[1:]))
assert [r['n'] for r in rows]==list(range(1,len(beats)+1)), "mismatch"
json.dump(rows,open('prompts.json','w'),indent=1)
with open('image_prompts.md','w') as f:
    f.write("# Why It Sucks to Be Tall (in 1730s Prussia) — Image Prompts\n\n333 beats · ~3–5 s each · Visual Style Profile locked · Characters locked to the Yesteryears character sheets\n\n"
  "**Headwear rule:** headwear fits the character's class and the scene. Nobody wears a hat indoors or in any bad scenario (kidnapping, punishment, the gauntlet, the walk home). Outdoors as a poor miller's son, you wear a worn felt cap; as a boy, a tweed cap. The tall grenadier cap appears only on parade and in the uniform-fitting scenes, because the script calls for it. In the King's bedroom the giants carry their caps under their arms.\n\n"
  "**Character lock**\n\n| Story role | Sheet |\n|---|---|\n| You (18 and 28) | Mascot, drawn very tall |\n| You, age 5 / 10 / 14 | Boy variant |\n| Your mother | Adult woman variant |\n| Old townswoman | Old woman variant |\n"
  "| Father, Seamus, the King, sergeant, recruiter, clerk, officer, shepherd, student, blacksmith, Frederick, visitors | Not on a sheet (fixed descriptions) |\n\n")
    for r in rows:
        f.write(f"## Beat {r['n']}\n**[Script Segment]** \"{r['seg']}\"\n\n**Image Prompt:** {r['prompt']}\n\n- **Camera Angle:** {r['cam']}\n- **Lighting:** {r['light']}\n- **Mood:** {r['mood']}\n- **Action:** {r['action']}\n\n")
print(len(rows))
