#!/usr/bin/env python3
"""Episode 1 config. Run: python3 build.py (the shared engine in ../engine.py does the work)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from channel import FIG, YOU, CAST, ORGANS, SCENES, OUTFITS
from engine import build

TITLE = "Why Does Eating Make You Sleepy Instead of Giving You Energy?"
PDF = "Food_Coma_Script_Beats_Prompts.pdf"
C = {'YOU': YOU, **CAST,
 'MEN': f"two volunteer test subjects (each {FIG}): a lanky man with a thin grey moustache in a sky-blue T-shirt, and a stocky bald man with a short grey beard in a leaf-green T-shirt",
 'VAIDYA': f"a traditional Ayurvedic physician ({FIG}, a neat white beard, a small saffron mark on the forehead and a white cotton kurta with a cream shawl)",
 **{k: ORGANS[k] for k in ('STOMACH', 'BRAIN', 'PANCREAS', 'GUT')}}
SHORT = {'YOU': 'you', 'COWORKER': 'your coworker', 'DOCTOR': 'the doctor', 'RESEARCHER': 'the researcher', 'FRIEND': 'your friend', 'MUM': 'your mum', 'MEN': 'the two men',
         'VAIDYA': 'an Ayurvedic physician', 'STOMACH': 'Stomach', 'BRAIN': 'Brain', 'PANCREAS': 'Pancreas', 'GUT': 'Intestines'}
# An office workday: work outfit everywhere except bed and the break-room nap.
DEFAULT_OUTFIT = 'work'
OUTFIT = {'bedroom': 'bed', 'breakroom': 'work_relaxed'}
S = {**SCENES,
 'cafe': ("a bright modern office canteen with wooden tables, lunch trays, plates of rice and curry, glasses of water and large windows", "soft midday daylight, warm tint"),
 'breakfast': ("a small home kitchen in the morning with a table, toast, a cup of coffee and a sunlit window", "bright morning daylight, fresh tint"),
 'lab': ("a bright modern university nutrition research room with a long table, pizza boxes, a scale, clipboards and a whiteboard", "bright even light, clean white"),
 'ayurveda': ("a traditional Indian courtyard with a brass oil lamp, a small cooking fire, brass vessels, herbs drying on a cloth and palm-leaf manuscripts", "warm daylight, saffron tint"),
 'park': ("a leafy city park path beside an office building, with benches and trees", "bright daylight, fresh green tint"),
 'breakroom': ("a quiet office break room with a soft grey couch, a cushion, a water cooler and a window with blinds", "soft warm ambient light"),
 'clinic': ("a calm modern doctor's consulting room with a desk, a computer, an examination couch and a simple digestive-system poster", "soft even light, clean pale-blue tint"),
}
SHAKE_AT = ("slipped a sleeping pill", "and that's why you feel sleepy", "But neither of these", "right when your body", "It's how much you eat")
FADE_AT = ("Okay, let's follow", "Think about your usual day", "Researchers actually", "Interestingly, people", "Maybe you've been sleeping", "So, why does eating")
LOCK = [("All people", FIG), ("You", "short tufty black curly hair; outfit fits the scenario: " + OUTFITS['work'] + " at work, " + OUTFITS['bed'] + " in bed, jacket off and tie loosened for the break-room nap"),
        ("Your coworker", C['COWORKER'].split('(', 1)[1].rstrip(')')),
        ("Organ characters", "flat cartoon organs with thick dark-plum outlines, true natural colours, big white eyes, thin limbs and small brown shoes; Stomach wears a chef's hat, Brain a headset, Pancreas reading glasses, Intestines a hard hat (full list in ../CHARACTER_SHEET.md)")]
build(globals())
