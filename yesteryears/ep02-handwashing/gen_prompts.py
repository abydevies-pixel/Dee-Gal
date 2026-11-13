import json, re
beats=json.load(open('beats.json'))
STYLE=("2D digital cartoon illustration in the big-head stick-figure style: oversized semi-realistic caricature heads with fine wrinkle and feature linework and flat skin tones, attached to minimal thick solid-black stick-figure bodies with no hands and no clothing volume; highly detailed, period-accurate hand-drawn background with clean black ink outlines and flat muted colors; desaturated 1840s Habsburg palette of stone grey, cream, parchment beige, Habsburg ochre, slate blue, brick red, sage green and ink brown; deadpan dark-comedy tone; no gore, no visible wounds, blood or nudity; static 16:9 frame; bottom-right corner kept clear")
C={
'BABY':"you as a newborn baby, a tiny version of the boy variant with a tuft of messy brown hair and no cap",
'YOU6':"you at age 6 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands)",
'YOU9':"you at age 9 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands)",
'YOU12':"you at age 12 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands)",
'YOU19':"you at age 19 (mascot, younger and lankier: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, __HAT__on a solid black stick body with no hands)",
'YOU':"you, the young doctor (mascot: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, __HAT__on a solid black stick body with no hands)",
'YOU47':"you at age 47 (mascot, older: an oversized semi-realistic caricature head, thinning brown hair streaked with grey, four freckles on each cheek, greying stubble and deep tired lines under the eyes, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, bareheaded, on a solid black stick body with no hands)",
'MODERN':"a present-day person (mascot, modern day: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, bareheaded, on a solid black stick body with no hands)",
'FATHER':"your father, a careful prosperous grocer with neat grey side-whiskers, small round spectacles and a tidy side parting, on a solid black stick body with no hands",
'MOTHER':"your mother (adult woman variant: a slimmer oval oversized head, dark brown hair parted in the middle and gathered into a bun tied with an oxblood ribbon, lashes, half-lidded deadpan eyes and tinted lips, on a solid black stick body with no hands)",
'ANNA':"Anna, a 20-year-old laundress (adult woman variant, younger: light brown hair in a simple plait with no ribbon, freckles, lashes and half-lidded eyes, on a solid black stick body with no hands)",
'WIFE':"your wife (adult woman variant, fair-haired: light blonde hair parted in the middle and gathered into a bun tied with an oxblood ribbon, lashes and tinted lips, on a solid black stick body with no hands)",
'CHILDREN':"your two small children (a boy variant and a girl variant: rounder oversized heads, the boy in a flat grey tweed cap, the girl with auburn braids tied with oxblood bows, on short solid black stick bodies with no hands)",
'PORTER':"the hospital porter (old man variant: an oversized head with a bald, lined crown, white side tufts above the ears, thick white brows, white mutton-chop whiskers, round spectacles, forehead lines and crow's feet, on a stooped solid black stick body with no hands)",
'PRIEST':"the hospital priest, an elderly man with a lined kind face, white hair and a white clerical collar, on a solid black stick body with no hands",
'KLEIN':"Professor Johann Klein, a stiff older professor with a long narrow face, thin lips, slicked-back grey hair and a high starched collar, on a solid black stick body with no hands",
'KOLL':"Jakob Kolletschka, a cheerful forensic professor in his forties with a round face, rosy cheeks, a balding crown with dark side hair and a short dark beard, on a solid black stick body with no hands",
'STUDENT':"a careless young medical student with a smug face, slick dark hair and wispy side-whiskers, on a solid black stick body with no hands",
'COLLEAGUE':"an old colleague from Vienna, a polished senior doctor with a neat dark beard and a smooth confident face, on a solid black stick body with no hands",
'GUARDS':"two burly asylum attendants with blank square faces and cropped hair, on thick solid black stick bodies with no hands",
'LISTER':"surgeon Joseph Lister, a calm Victorian doctor with dark side-whiskers and a high collar, on a solid black stick body with no hands",
'PASTEUR':"chemist Louis Pasteur, a serious Frenchman with a full dark beard and a furrowed brow, on a solid black stick body with no hands",
}
S={
'buda':("a sloping cobbled street in 1820s Buda with pastel baroque houses, a grocery shopfront below, the castle hill and the Danube in the distance","flat even daylight, soft warm tint"),
'shop':("a prosperous 1820s grocery shop interior with coffee sacks, jars of dried fruit, brass scales and a polished wooden floor","flat even ambient light, warm honey tint"),
'home':("a comfortable middle-class Buda family home above a shop with a long dining table, wooden chairs, a tiled stove and lace curtains","flat even ambient light, warm cream tint"),
'vienna':("a grand 1830s Vienna street with baroque palaces, horse carriages and the spire of St Stephen's Cathedral","flat even daylight, pale stone-grey tint"),
'lecture':("a steep circular anatomy lecture theatre of the 1830s with tiered wooden benches, anatomical charts on the walls and a dissection table covered with a white sheet","flat even ambient light, pale grey-cream tint"),
'hospext':("the vast Vienna General Hospital in the 1840s with long ochre-yellow wings, many courtyards with trees, a chapel and a main gate","flat even daylight, pale ochre tint"),
'gate':("the main gate and entrance hall of the Vienna General Hospital in the 1840s with stone arches, a porter's booth and doors marked FIRST CLINIC and SECOND CLINIC","flat even daylight, cool stone-grey tint"),
'street':("a cobbled Vienna street outside the hospital walls in the 1840s with doorways, a parked carriage and a foundling home across the road","flat even overcast daylight, cool grey tint"),
'deadhouse':("the hospital morgue of the 1840s, a vaulted stone room with stone tables holding shapes under white sheets, lanterns and buckets","flat even ambient light, dim cold green-grey tint"),
'stairs':("a stone staircase leading from the morgue up to the maternity wards, with iron railings and whitewashed walls","flat even ambient light, cool grey tint"),
'ward1':("the First Clinic maternity ward in the 1840s: a long ward with rows of iron beds, grey blankets, wooden cradles, tall windows and whitewashed walls","flat even ambient light, pale cream-grey tint"),
'ward2':("the Second Clinic maternity ward in the 1840s: a long ward with rows of iron beds, wooden cradles and midwives in aprons, slightly brighter and tidier","flat even ambient light, soft warm cream tint"),
'office':("a young doctor's small hospital room in the 1840s with a wooden desk covered in ledgers, a candle, a narrow bed and a window onto a courtyard","flat even ambient light, warm candle-yellow tint"),
'corridor':("a long vaulted hospital corridor of the 1840s with whitewashed walls, arched windows and wooden doors","flat even ambient light, pale grey tint"),
'canal':("the Danube canal in Vienna at dusk in the 1840s with a tree-lined promenade, iron lamps, benches and barges","flat even ambient light, soft dusk lilac tint"),
'venice':("Venice in the 1840s with gondolas on a green canal, arched bridges and pastel palazzos","flat even daylight, warm golden tint"),
'basin':("the entrance to the First Clinic ward with a large white basin of chlorinated lime on a wooden stand, a hand-painted sign above and the ward visible beyond","flat even ambient light, pale clean cream tint"),
'university':("a grand 1840s university hall in Vienna with wood panelling, portraits of old professors and rows of seated senior doctors in dark frock coats","flat even ambient light, warm wood-brown tint"),
'pest_hosp':("a small, run-down 1850s hospital ward in Pest with peeling plaster, cracked windows and old iron beds","flat even ambient light, dusty ochre tint"),
'pest_home':("a modest 1850s Pest family apartment with a dining table, an armchair, bookshelves and piles of ledgers in a corner","flat even ambient light, warm lamp-yellow tint"),
'pest_river':("the Danube promenade in Pest in the 1850s with the new Chain Bridge, iron lamps and strolling families","flat even ambient light, soft dusk amber tint"),
'pest_street':("a busy cobbled street in 1850s Pest with shops, carriages and passers-by","flat even daylight, warm stone tint"),
'party':("an 1860s Pest drawing room party with chandeliers, guests holding glasses and a piano","flat even ambient light, warm golden tint"),
'desk_pest':("a cluttered 1860s study in Pest with a writing desk buried in letters, ink pots, ledgers, newspapers and a single lamp","flat even ambient light, dim lamp-yellow tint"),
'carriage':("the inside of a horse-drawn travelling carriage in the 1860s with padded benches and a small window showing a country road","flat even ambient light, muted brown tint"),
'asylum_ext':("the grim stone facade and tall iron gates of an 1860s Vienna asylum with barred windows and a gravel courtyard","flat even overcast daylight, cold grey tint"),
'asylum_cell':("a dark bare stone asylum cell of the 1860s with a narrow cot, a small barred window, a heavy door and a dusty washbasin","flat even ambient light, dim cold blue-grey tint"),
'cemetery':("a rainy 1860s cemetery with a fresh grave, a plain headstone and bare trees","flat even overcast daylight, wet grey tint"),
'lister':("a bright 1860s Scottish infirmary ward with iron beds, an operating table and a brass carbolic-acid sprayer","flat even daylight, clean pale tint"),
'pasteur':("an 1860s French chemistry laboratory with glass flasks, a brass microscope and wooden benches","flat even daylight, warm amber tint"),
'modern':("a clean present-day setting with white tiles, a steel sink and a mirror","flat even bright daylight, cool clean white tint"),
'uni_today':("a grand present-day university building in Budapest with columns and a carved name over the entrance","flat even daylight, soft blue-sky tint"),
}
BAD={165,166,167,266,267,268,269}  # grief, disgrace, exile: no hats
OUTDOOR={'buda','vienna','hospext','gate','street','canal','venice','pest_river','pest_street','asylum_ext','cemetery','uni_today'}
def variant(k,sc):
    d=C[k]; out=sc in OUTDOOR
    if k=='YOU': return d.replace('__HAT__',"wearing a plain black felt top hat suited to a gentleman doctor, " if out else "bareheaded, his messy brown hair fully visible, ")
    if k=='YOU19': return d.replace('__HAT__',"wearing a modest dark student's cap, " if out else "bareheaded, his messy brown hair fully visible, ")
    if k in('YOU6','YOU9','YOU12'):
        return d if out else d.replace("a messy brown fringe under a flat grey tweed cap","messy brown hair with no cap").replace("boy variant:","boy variant, cap off indoors:")
    return d
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
    for k in sorted(C,key=len,reverse=True): a=a.replace('{'+k+'}',variant(k,'office' if n in BAD else sc))
    short=act
    for k in C: short=short.replace('{'+k+'}',{'YOU':'you','YOU4':'you (age 4)','YOU7':'you (age 7)','YOU10':'you (age 10)','YOU16':'you (age 16)','BABY':'you as a baby','FATHER':'your father','MOTHER':'your mother','SILAS':'Silas','LISTON':'Liston','HS':'the house surgeon','NURSE':'the nurse','DRESSER':'a dresser','STUDENTS':'the students','CHURCHILL':'Churchill','YOU6':'you (age 6)','YOU9':'you (age 9)','YOU12':'you (age 12)','YOU19':'you (age 19)','YOU47':'you (age 47)','MODERN':'a present-day person','ANNA':'Anna','WIFE':'your wife','CHILDREN':'your children','PORTER':'the porter','PRIEST':'the priest','KLEIN':'Klein','KOLL':'Kolletschka','STUDENT':'the student','COLLEAGUE':'the colleague','GUARDS':'the attendants','LISTER':'Lister','PASTEUR':'Pasteur'}[k])
    env,light=S[sc]
    prompt=f"{CAM[cam]} of {a}. Setting: {env}. Lighting: {light}. Mood: {mood}. Style: {STYLE}."
    rows.append(dict(n=n,seg=beats[n-1],prompt=prompt,cam=CAM[cam],light=light,mood=mood,action=short[0].upper()+short[1:]))
assert [r['n'] for r in rows]==list(range(1,len(beats)+1)), "mismatch"
json.dump(rows,open('prompts.json','w'),indent=1)
with open('image_prompts.md','w') as f:
    f.write("# Why It Sucks to Wash Your Hands (in 1840s Vienna) — Image Prompts\n\n358 beats · ~3–5 s each · Visual Style Profile locked · Characters locked to the Yesteryears character sheets\n\n"
  "**Headwear rule:** headwear fits the character's class and the scene. Nobody wears a hat indoors, in bed, in hospital, in the asylum or in any bad scenario. Outdoors, the young doctor wears a plain gentleman's felt top hat (fits his class); as a student, a modest cap; as a boy, a tweed cap.\n\n"
  "**Character lock**\n\n| Story role | Sheet |\n|---|---|\n| You (19, young doctor, 47, present day) | Mascot |\n| You, age 6 / 9 / 12 | Boy variant |\n| Your mother | Adult woman variant |\n| Anna | Adult woman variant, younger (plait, no ribbon) |\n| Your wife | Adult woman variant, fair-haired |\n| Your children | Boy and girl variants |\n| Hospital porter | Old man variant |\n"
  "| Father, Klein, Kolletschka, priest, student, colleague, attendants, Lister, Pasteur | Not on a sheet (fixed descriptions) |\n\n")
    for r in rows:
        f.write(f"## Beat {r['n']}\n**[Script Segment]** \"{r['seg']}\"\n\n**Image Prompt:** {r['prompt']}\n\n- **Camera Angle:** {r['cam']}\n- **Lighting:** {r['light']}\n- **Mood:** {r['mood']}\n- **Action:** {r['action']}\n\n")
print(len(rows))
