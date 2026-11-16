#!/usr/bin/env python3
"""Episode 2 config. Run: python3 build.py (the shared engine in ../engine.py does the work)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from channel import FIG, YOU, CAST, ORGANS, SCENES, OUTFITS
from engine import build

TITLE = "5 Ordinary Habits That Can Turn Dangerous"
PDF = "Ordinary_Habits_Script_Beats_Prompts.pdf"
C = {'YOU': YOU, **CAST, **{k: ORGANS[k] for k in ('TOOTH', 'STOMACH', 'BRAIN', 'HEART')}}
SHORT = {'YOU': 'you', 'COWORKER': 'your coworker', 'DOCTOR': 'the doctor', 'RESEARCHER': 'the researcher', 'FRIEND': 'your friend', 'MUM': 'your mum',
         'TOOTH': 'Tooth', 'STOMACH': 'Stomach', 'BRAIN': 'Brain', 'HEART': 'Heart'}
# One ordinary day: pyjamas at the bathroom sink and in bed, suit for the workday, gym kit at dawn, weekend clothes for the social-life chapter.
DEFAULT_OUTFIT = 'work'
OUTFIT = {'bathroom': 'bed', 'bedroom': 'bed', 'bedroom_lamp': 'bed', 'gym': 'gym', 'livingroom': 'weekend', 'coffeeshop': 'weekend',
          'park': 'weekend', 'party': 'weekend', 'club': 'weekend', 'familykitchen': 'weekend'}
S = {**SCENES,
 'bathroom': ("a bright modern bathroom with a white sink, a large mirror, a toothbrush cup, a small wall clock and a sunny window", "bright morning sunlight, fresh tint"),
 'kitchen': ("a bright home kitchen in the morning with a small table, a plate of eggs and toast, a coffee mug, a wall clock and a sunny window", "bright morning daylight, warm tint"),
 'livingroom': ("a cosy modern living room with a soft sofa, cushions, a TV, a floor lamp, a coffee table and a fridge visible through the kitchen doorway", "soft warm daylight"),
 'gym': ("a bright gym at dawn with treadmills, dumbbells and big windows showing a pink sunrise", "fresh early-morning light, pink sunrise glow"),
 'car': ("inside a small car in evening traffic, with the steering wheel, dashboard and red tail lights ahead", "warm golden-hour evening light"),
 'lab': ("a bright modern university research office with desks, charts on the walls and a whiteboard", "bright even light, clean white"),
 'stairs': ("a bright office stairwell with big windows, a handrail and lift doors on the landing", "bright daylight"),
 'bedroom_lamp': ("a modern bedroom in the evening with a made bed, a bedside table, a phone charger and a warm bedside lamp", "warm lamplight, cosy amber tint"),
 'coffeeshop': ("a cosy neighbourhood café with wooden tables, warm pendant lights, plants and big windows", "warm daylight, soft amber tint"),
 'park': ("a leafy city park with a path, benches, a duck pond and tall trees", "bright daylight, fresh green tint"),
 'party': ("a lively house party in a bright living room with string lights, snacks on a table and groups of guests chatting", "warm party lighting with string-light glow"),
 'club': ("a bright community hall with long tables, board games, pottery wheels and friendly people", "bright even daylight, warm tint"),
 'familykitchen': ("a warm family kitchen with pots on the stove, chopped vegetables, family photos on the fridge and a sunny window", "warm daylight, homely tint"),
}
SHAKE_AT = ("So you scrub", "So, is your toothbrush", "Congratulations!", "You get hit", "Quit your job")
FADE_AT = ("It's a bright sunny", "Have you ever finished", "Are you sitting right now", "Maybe it's the news", "Think about the last time", "Now think about how your day")
LOCK = [("All people", FIG),
        ("You", "short tufty black curly hair; outfit fits the scenario: " + OUTFITS['bed'] + " at the bathroom sink and in bed, " + OUTFITS['work'] + " for the workday, "
         + OUTFITS['gym'] + " at the gym, " + OUTFITS['weekend'] + " for the social-life chapter"),
        ("Your coworker", CAST['COWORKER'].split('(', 1)[1].rstrip(')')),
        ("Your old friend", CAST['FRIEND'].split('(', 1)[1].rstrip(')')),
        ("Your mum", CAST['MUM'].split('(', 1)[1].rstrip(')')),
        ("Organ characters", "flat cartoon organs with thick dark-plum outlines, true natural colours, big white eyes, thin limbs and small brown shoes; Tooth wears a sailor cap, Stomach a chef's hat, Brain a headset; Heart has calm half-lidded eyes (full list in ../CHARACTER_SHEET.md)")]
build(globals())
