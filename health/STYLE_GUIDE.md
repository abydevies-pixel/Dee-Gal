# Health Channel — Style Guide

A lifestyle and health explainer channel: everyday body questions, health myths and habits, told as a second-person "this is happening to you" story. Every episode follows this guide so the channel sounds and looks the same.

## 1. Narration style

**Voice.** Talk to one viewer as "you", in the present tense. Put them inside a familiar moment ("It's lunchtime and you just had a wonderful meal.") before any science. Sound like a curious, slightly cheeky friend who has read the research, not a lecturer.

**Rhythm.**
- Short lines with one idea each. Most sentences are 4–12 words.
- Use fragments and one-word beats for timing: "Except…", "Why?", "Another thing?", "Slow down."
- Ask a question often, then answer it in the next line.
- Each chapter ends on a question that pulls the viewer into the next one.

**Humour.** Use dry asides and exaggeration rooted in real life: "fighting for your life to stay awake at your desk", "No, you're not actually in a coma", "And yes, apparently eating pizza was part of the experiment." Make one light joke every 20–40 seconds. Never joke at the expense of anyone's body, weight or illness.

**Explaining science.**
- Give the technical term once, then translate it straight away: "Postprandial somnolence. Which simply means sleepiness after eating."
- Explain things by following the body step by step ("Okay, let's follow your lunch…") and let organs "talk" ("Hey, food has arrived, we've got work to do").
- Be honest about uncertainty: "Scientists are still studying…", "There's no single sleep button…", "may leave some people…".
- Mention studies in plain words ("Researchers had men eat pizza on two occasions…"). Don't quote statistics unless they're solid.
- Traditional and cultural views (Ayurveda and others) are welcome. Present them respectfully as "a different way of explaining it", never as proof.

**Myth-busting pattern.** Myth → "Heard that before?" → what's actually true → why the myth feels right.

**Talking organs.** Organs sometimes speak a short line in their own voice, for example the Stomach in episode 1. The narration stays a voiceover, and organ lines are rare, short and subtle. See `VOICES.md` for the rules and the fixed voice of each organ.

**Advice.** Give practical advice and don't ban foods: "You don't need to remove it. Just consider the portion." Always add a short safety line: when symptoms are frequent, severe or disrupt daily life, see a healthcare professional. The channel never diagnoses.

## 2. Episode structure (8–10 minutes, about 1,200–1,500 words at 2.4 words per second)

| Part | Length | Job |
|---|---|---|
| Hook | 30–45 s | A relatable "you" moment, then the twist, then the title question |
| Chapters (5–7) | 1–1.5 min each | Each one is a single idea and ends on a question |
| Myth chapter | early | Set up the popular explanation, then debunk it |
| Practical chapter | late | 4–6 simple changes, plus the "see a professional" line |
| Payoff | 30 s | Answer the title in one sentence, then add the good news |
| Call to action | 10 s | A personal question for the comments ("Which meal makes you the sleepiest?") |

## 3. Beats

- One beat is one image, about 3–5 seconds (roughly 4–12 words). Split long sentences at natural pauses.
- Section and chapter headings aren't narrated, so they aren't beats.
- Camera moves cycle through push-in, pan and pull-out. Use a shake on punchlines and myth-busts, and a fade at the start of a new chapter or scene.

## 4. Visual style

Characters, organs and both scene styles are defined once in `channel.py` and shown in `CHARACTER_SHEET.md`, together with the reference images in `references/`. Every episode uses them unchanged.

- **People scenes:** chunky rounded people with deep matte-black faces, white oval eyes, white brows and full limbs (never stick limbs). Glossy, slightly 3D finish. Bright channel colours by default; dark only when the scene calls for it.
- **Inside-the-body scenes** (body, blood vessel, brain control room): flat 2D vector with thick dark-plum outlines. Organ characters have big white eyes, thin rubber-hose limbs, small brown shoes and one accessory each. Organs are **always their true natural colours**.
- **Palette (channel theme):** clean white, warm cream, fresh mint, sky blue, sunny yellow, coral and leaf green. Episodes should feel bright overall. When a scene genuinely needs dark colours (night, a dark bedroom, rain at dusk, a gloomy beat), use them, keep the characters readable, and go back to the bright theme in the next scene.
- **Natural organ colours:** stomach soft peachy pink · small intestine salmon pink · large intestine dusty pink · pancreas pale creamy yellow-pink · liver reddish brown · brain soft pinkish grey · heart/muscle deep red · blood: red cells, arteries red, veins blue · lungs light pink · kidneys reddish brown · bones ivory · fat tissue pale yellow.
- **Main character:** the face and short curly black hair never change, and the outfit fits the scenario (list in `channel.py` / `CHARACTER_SHEET.md`).
- **Recurring devices:** a glowing body outline on light blue, a pink tissue background with a blood-vessel pipe, a "brain control room" with labelled gauges, a 24-hour clock, simple line graphs, and a red "MYTH" stamp.
- **Never:** gore, open wounds, blood splatter, nudity, or shaming body imagery.
- **Framing:** 16:9, bottom-right corner kept clear for the channel watermark, and only the words given in quotes appear on screen.

## 5. Voices

One narrator voice for the whole channel, and one fixed voice per organ. See `VOICES.md` for the cast, how to lock each voice, and audition lines.
