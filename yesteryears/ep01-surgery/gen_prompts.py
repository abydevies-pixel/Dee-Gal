import json
beats=json.load(open('beats.json'))
STYLE=("2D digital cartoon illustration in the big-head stick-figure style: oversized semi-realistic caricature heads with fine wrinkle and feature linework and flat skin tones, attached to minimal thick solid-black stick-figure bodies with no hands and no clothing volume; highly detailed, period-accurate hand-drawn background with clean black ink outlines and flat muted colors; desaturated 1840s London palette of soot grey, cream, parchment beige, brick red, Thames brown-green, tallow yellow and faded navy; deadpan dark-comedy tone; no gore, no visible wounds or blood; static 16:9 frame; bottom-right corner kept clear")
C={
'BABY':"you as a newborn baby, drawn as a tiny version of the boy variant without the cap: a rounder oversized head about half his total height, a tuft of messy brown hair, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands",
'YOU4':"you at age 4 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands)",
'YOU7':"you at age 7 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands)",
'YOU10':"you at age 10 (boy variant: a rounder oversized head about half his total height, a messy brown fringe under a flat grey tweed cap, freckles on both cheeks, half-lidded deadpan eyes and a gap tooth, on a short solid black stick body with no hands)",
'YOU16':"you at age 16 (mascot, younger and lankier: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, __HAT__on a solid black stick body with no hands)",
'YOU':"you, age 22 (mascot: an oversized semi-realistic caricature head, messy short brown hair with a spiky fringe, four freckles on each cheek, light stubble on the jaw, half-lidded deadpan eyes, a raised left eyebrow and a flat mouth, __HAT__on a solid black stick body with no hands)",
'FATHER':"your father, a broad-faced middle-aged cooper with heavy brows, a short grey-brown beard and a battered flat cap, on a solid black stick body with no hands",
'MOTHER':"your mother (adult woman variant: a slimmer oval oversized head, dark brown hair parted in the middle and gathered into a bun tied with an oxblood ribbon, lashes, half-lidded deadpan eyes and tinted lips, on a solid black stick body with no hands)",
'SILAS':"Silas (old man variant: an oversized head with a bald, lined crown, white side tufts above the ears, thick white brows, white mutton-chop whiskers, round spectacles, forehead lines and crow's feet, on a stooped solid black stick body with no hands)",
'SILASYOUNG':"Silas in 1805 as a young sailor (old man variant, 40 years younger: dark mutton-chop whiskers, a full head of dark hair, no spectacles and no wrinkles, on a solid black stick body with no hands)",
'NURSE':"the nurse (old woman variant: an oversized wrinkled head, a white ruffled linen mob cap with an oxblood band, grey hair in a bun, round spectacles, thick pale-grey brows and tinted lips, on a stooped solid black stick body with no hands)",
'LISTON':"surgeon Robert Liston, very tall with an extra-long solid black stick body with no hands, a large stern long-jawed head, dark side-whiskers, receding dark hair and heavy-lidded bored eyes",
'HS':"a young clean-shaven house surgeon with a boyish face, neat side-parted blond hair and small round spectacles, on a solid black stick body with no hands",
'DRESSER':"a nervous young medical student with a pale face, wispy side-whiskers and a high white collar, on a solid black stick body with no hands",
'STUDENTS':"bareheaded young medical students with oversized heads, side-whiskers and high collars on solid black stick bodies",
'CHURCHILL':"Frederick Churchill, a middle-aged butler with neatly combed grey hair, trim mutton chops and a dignified face, on a solid black stick body with no hands",
'BREWER':"a fat-cheeked wealthy brewery owner with a top hat, a monocle and a gold watch chain, on a solid black stick body with no hands",
}
S={
'river':("the Southwark riverbank at low tide in the 1820s, grey-brown mudflats, beached barges, smoking brewery chimneys and the dome of St Paul's across the Thames under a pale grey sky","flat even overcast daylight, cool grey tint"),
'home':("a cramped 1820s Southwark cooper's cottage with low smoke-darkened beams, stacked oak barrels and staves, a steaming wooden washtub, wet laundry on lines and a small window onto the Thames mudflats","flat even ambient light, warm tallow-yellow tint"),
'workshop':("a cooper's workshop in Southwark with half-built oak barrels, iron hoops, tools on the wall and oak shavings on the floor","flat even ambient light, warm amber tint"),
'bridge':("London Bridge in the 1830s with a wide granite roadway, stone balustrades, horse-drawn carts, crowds and ships on the Thames below","flat even daylight, soft pale-blue sky tint"),
'lane':("a narrow cobbled Southwark lane with soot-stained brick terraces, washing lines overhead, small shopfronts and a gas lamp","flat even ambient light, soft dusk amber tint"),
'billingsgate':("Billingsgate Fish Market before dawn in the 1840s, crowded cobbles, stacked wicker fish baskets, fishmongers' stalls, gas lamps and ship masts on the Thames behind","flat even ambient light, cool blue-grey pre-dawn tint with gas-lamp yellow accents"),
'docks':("the London Docks in autumn 1846 with tall brick warehouses, a wooden sailing ship's hull, a timber crane with hanging ropes and stacked wine crates and barrels on wet cobbles","flat even overcast daylight, damp grey tint"),
'cart':("a cobbled Victorian dockside street with a rough wooden handcart, warehouses and onlookers","flat even overcast daylight, damp grey tint"),
'hospext':("the grand classical stone front of University College Hospital in 1846 with columns, iron railings, stone steps and gas lamps at the gate","flat even ambient light, cool grey-blue evening tint"),
'brewerdoor':("the grand black front door of a Georgian townhouse with a brass knocker, stone steps, iron railings and a brewery chimney in the distance","flat even daylight, cool grey tint"),
'kitchen':("a poor cottage kitchen at night with a scrubbed wooden table, a single candle and barrels in the shadows","flat even ambient light, warm candle-yellow tint"),
'ward':("a long 1840s hospital ward with rows of iron-framed beds and grey wool blankets, whitewashed walls, tall sash windows, bare wooden floorboards, an iron stove and small shelves above each bed","flat even ambient daylight, pale cream-grey tint"),
'wardnight':("a long 1840s hospital ward at night with rows of iron-framed beds, whitewashed walls, tall dark windows and a single oil lamp","flat even ambient light, dim blue-grey night tint with a soft oil-lamp glow"),
'stairs':("a narrow stone staircase with an iron handrail winding up between whitewashed hospital walls","flat even ambient light, cool grey tint"),
'theatre':("a circular 1840s operating theatre with steep semicircular wooden standing tiers and rails rising to a glass skylight, a plain dark-stained wooden operating table with leather straps in the centre, a wooden box of sawdust beneath it and an instrument case on a side table","flat even skylight daylight, pale grey-cream tint"),
'trafalgar':("the cramped gun deck of an 1805 British wooden warship with black cannons, powder kegs, splintered timbers and drifting smoke","flat even ambient light, smoky grey-orange tint"),
'gibraltar':("the deck of a wooden sailing ship passing the Rock of Gibraltar on a calm sea","flat even daylight, clear pale-blue tint"),
'galley':("a cramped below-deck mess on an old sailing ship with a wooden table, tin mugs, ship's biscuits and a hanging lantern","flat even ambient light, warm lantern-yellow tint"),
'nelson':("the quarterdeck of an 1805 British ship of the line with tall masts, rigging and an open sea","flat even daylight, sea-grey tint"),
'dream':("a soft hazy dream version of London Bridge with an empty granite roadway, gulls and a glowing river","flat even ambient light, warm hazy golden tint"),
'boston':("the domed surgical amphitheatre of Massachusetts General Hospital in 1846 with tiered wooden seats and a central operating chair","flat even daylight, pale cream tint"),
'atlantic':("a three-masted sailing packet ship on the grey North Atlantic, rolling waves and a cloudy sky","flat even overcast daylight, cool sea-grey tint"),
'textbook':("an open antique medical textbook on a worn wooden desk with engraved illustrations and printed text","flat even ambient light, warm parchment tint"),
}

OUTDOOR={'river','bridge','lane','billingsgate','docks','cart','hospext','brewerdoor','dream'}
HATCL="__HAT__"
def variant(k,sc):
    d=C[k]
    out=sc in OUTDOOR
    if k in('YOU','YOU16'):
        return d.replace(HATCL,"wearing a worn grey tweed flat cap, " if out else "bareheaded, his messy brown hair fully visible, ")
    if k in('YOU4','YOU7','YOU10'):
        return d if out else d.replace("a messy brown fringe under a flat grey tweed cap","messy brown hair with no cap").replace("boy variant:","boy variant, cap off indoors:")
    if k=='FATHER' and sc in('ward','wardnight','kitchen','stairs','theatre'):
        return d.replace(" and a battered flat cap","").replace("short grey-brown beard","short grey-brown beard, bareheaded")
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
    for k in sorted(C,key=len,reverse=True): a=a.replace('{'+k+'}',variant(k,sc))
    short=act
    for k in C: short=short.replace('{'+k+'}',{'YOU':'you','YOU4':'you (age 4)','YOU7':'you (age 7)','YOU10':'you (age 10)','YOU16':'you (age 16)','BABY':'you as a baby','FATHER':'your father','MOTHER':'your mother','SILAS':'Silas','LISTON':'Liston','HS':'the house surgeon','NURSE':'the nurse','DRESSER':'a dresser','STUDENTS':'the students','CHURCHILL':'Churchill','BREWER':'the brewery owner','SILASYOUNG':'young Silas'}[k])
    env,light=S[sc]
    prompt=f"{CAM[cam]} of {a}. Setting: {env}. Lighting: {light}. Mood: {mood}. Style: {STYLE}."
    rows.append(dict(n=n,seg=beats[n-1],prompt=prompt,cam=CAM[cam],light=light,mood=mood,action=short[0].upper()+short[1:]))
assert [r['n'] for r in rows]==list(range(1,len(beats)+1)), "mismatch"
json.dump(rows,open('prompts.json','w'),indent=1)
with open('image_prompts.md','w') as f:
    f.write("# Why It Sucks to Need Surgery (Before Anesthesia) — Image Prompts (v2)\n\n377 beats · ~3–5 s each · Visual Style Profile locked · Characters locked to the Yesteryears character sheets\n\n"
  "**Headwear rule:** headwear always fits the character's class and the scene. No expensive hats on poor characters, and nobody wears a hat indoors, in bed, in hospital or on the operating table.\n\n**Character lock**\n\n| Story role | Sheet |\n|---|---|\n| You, age 22 (and 16) | Mascot: worn flat cap outdoors, bareheaded indoors (no top hat) |\n| You, age 4 / 7 / 10 | Boy variant: tweed cap outdoors, cap off indoors |\n| Your mother | Adult woman variant |\n| Silas | Old man variant |\n| The nurse | Old woman variant |\n"
  "| Father, Liston, house surgeon, dresser, students, Churchill, brewery owner | Not on a sheet yet (descriptions unchanged) |\n\n")
    for r in rows:
        f.write(f"## Beat {r['n']}\n**[Script Segment]** \"{r['seg']}\"\n\n**Image Prompt:** {r['prompt']}\n\n- **Camera Angle:** {r['cam']}\n- **Lighting:** {r['light']}\n- **Mood:** {r['mood']}\n- **Action:** {r['action']}\n\n")
print(len(rows)); print(open('image_prompts.md').read()[:2500])
