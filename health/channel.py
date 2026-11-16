"""Channel-wide look and cast. Every episode's build.py imports this, so characters, styles and voices stay
identical across the whole channel. Change a character here and every episode picks it up on its next build.
Reference images: references/ (see CHARACTER_SHEET.md)."""

# ---- People scenes (reference: references/people-*.jpg) ----
PEOPLE_STYLE = (
    "bright 2D cartoon animation still with a soft, glossy, slightly 3D-rendered finish: chunky rounded characters with smooth deep matte-black skin and faces, "
    "large white oval eyes with black pupils, thick white eyebrows, white mouth lines (open mouths show a red tongue), rounded heads slightly large for the body, "
    "full arms, legs and dark rounded hands (never stick limbs), bold brightly coloured clothes with soft folds; clean outlines, soft gradient shading and gentle "
    "rim light; detailed cartoon backgrounds with depth; cheerful light channel palette of clean white, warm cream, fresh mint, sky blue, sunny yellow, coral and "
    "leaf green as the default; darker colours (dusk purple, night blue, warm window glow) used only where the scene itself calls for them, with the characters "
    "still clear; any organ that appears keeps its true natural colour; no gore, open wounds, blood splatter or nudity; light, curious, gently comic tone; "
    "any on-screen words limited to the ones given in quotes; static 16:9 frame; bottom-right corner kept clear")

# ---- Inside-the-body scenes (reference: references/organ-*.jpg) ----
ORGAN_STYLE = (
    "flat 2D vector cartoon animation still: clean flat colours with simple soft highlights and thick dark-plum outlines; organ characters with big round white "
    "eyes, dark pupils, expressive dark eyebrows, small expressive mouths and thin dark rubber-hose arms and legs with small rounded hands and small brown shoes; "
    "every organ in its true natural anatomical colour, never recoloured; bright, clear and friendly; no gore, open wounds, blood splatter or nudity; light, "
    "curious, gently comic tone; any on-screen words limited to the ones given in quotes; static 16:9 frame; bottom-right corner kept clear")
ORGAN_SCENES = {'body', 'blood', 'brainhq'}

FIG = ("a chunky rounded cartoon person with smooth deep matte-black skin and face, large white oval eyes with black pupils, thick white eyebrows "
       "and full arms, legs and dark rounded hands")

# The main character's face and hair never change; the outfit fits the scenario (each episode picks from OUTFITS or adds one).
YOU = f"you (the main character: {FIG}, short tufty black curly hair, __OUTFIT__)"
OUTFITS = {
    'work': "a formal work outfit: a fitted navy suit jacket and trousers, a crisp white shirt, a sky-blue tie and polished black shoes",
    'work_relaxed': "the formal work outfit with the suit jacket off and the tie loosened: crisp white shirt, sky-blue tie, navy trousers and black shoes",
    'bed': "plain sky-blue pyjamas",
    'gym': "a leaf-green T-shirt, black joggers and white trainers",
    'rain': "a sunny-yellow raincoat with the hood up, dark jeans and white trainers",
    'hospital': "a pale-blue patient gown and grey slippers",
    'weekend': "a coral T-shirt, blue jeans and white trainers",
}

CAST = {
    'COWORKER': f"your coworker ({FIG}, auburn hair in a high round bun, a tailored coral blazer over a crisp white blouse, slim grey trousers and black heels)",
    'DOCTOR': f"a friendly doctor ({FIG}, short grey hair, white rectangular glasses, a white coat over a sky-blue shirt and a silver stethoscope)",
    'RESEARCHER': f"a researcher ({FIG}, a neat dark-purple bob, round white glasses and a white lab coat, holding a clipboard)",
}

ORGAN = ("a flat cartoon organ character with a thick dark-plum outline, big round white eyes with dark pupils, expressive dark eyebrows, a small mouth and "
         "thin dark rubber-hose arms and legs with small rounded hands and small brown shoes")
ORGANS = {
    'STOMACH': f"Stomach ({ORGAN}: a plump J-shaped stomach in its natural soft peachy pink with pinker folds, a visible digestive-juice level with small bubbles "
               "in its lower half, and a small white chef's hat)",
    'BRAIN': f"Brain ({ORGAN}: a brain in its natural soft pinkish grey with clear folds, wearing a slim black headset with a small microphone)",
    'PANCREAS': f"Pancreas ({ORGAN}: a long, slightly lumpy pancreas in its natural pale creamy yellow-pink, with small round reading glasses and a pencil tucked behind it)",
    'GUT': f"Intestines ({ORGAN}: the coiled small intestine in its natural salmon pink framed by the large intestine in a slightly deeper dusty pink, wearing a small orange hard hat)",
    'HEART': f"Heart ({ORGAN}: a heart in its natural deep red with a short blue artery on top, calm half-lidded eyes)",
    'LIVER': f"Liver ({ORGAN}: a wedge-shaped liver in its natural reddish brown, droopy tired eyelids, holding a tiny white coffee mug)",
    'LUNGS': f"Lungs ({ORGAN}: a pair of lungs in their natural light pink with soft spongy texture, sharing one long sky-blue scarf)",
    'KIDNEYS': f"Kidneys ({ORGAN}: a pair of bean-shaped kidneys in their natural reddish brown, wearing small yellow rubber gloves)",
}

def style_for(scene):
    return ORGAN_STYLE if scene in ORGAN_SCENES else PEOPLE_STYLE
