# Health Channel — Voice Cast

The narrator carries every episode. Now and then an organ speaks a line of its own. These lines should feel like the body briefly talking back, not a cartoon show.

## Rules

1. **The narrator comes first.** Organ lines are rare: usually 1–3 per episode, each one or two short sentences. The narrator sets them up ("Basically telling it,") and then carries on.
2. **Keep it subtle.** Each organ's voice differs from the narrator's through pitch, pace and attitude, never through silly voices, heavy accents, chipmunk pitching, robot effects or echo. A listener should notice the shift without it pulling them out of the story.
3. **One organ, one voice, forever.** Once a voice is set (the same voice actor, or the same TTS voice and settings), reuse it unchanged in every episode, and write its settings into the table below the first time it's recorded.
4. **Mark it in the script.** In `beats.json` a spoken line is `{"text": "...", "voice": "STOMACH"}` and gets its own beat. `build.py` then tags it in the beats list, the PDF, the timeline and `voiceover_script.txt`, so it can be recorded or generated separately and dropped back in.
5. **Show the speaker.** On a spoken beat the organ is on screen with its mouth open, mid-sentence.
6. **Lines stay accurate.** An organ never says anything the science doesn't support.

## Cast

| Voice | Direction | Personality | Recording / TTS settings (fill in once set) |
|---|---|---|---|
| **NARRATOR** | Warm, curious, conversational; medium pace; dry humour | A friend who's read the research | — |
| **STOMACH** | Slightly lower and rounder than the narrator; hearty and practical; unhurried, a little proud; like a busy kitchen manager announcing a delivery | Hard-working, food-focused, cheerfully bossy | — |
| **BRAIN** | Clear, slightly higher and quicker than the narrator; precise; a hint of overthinking | The control-room manager, always monitoring | — |
| **INTESTINES** | Mid pitch, quick and chatty; upbeat multitasker | Always busy sorting and absorbing | — |
| **PANCREAS** | Light, polite, measured, precise; like a careful accountant | Quietly keeps the sugar books balanced | — |
| **HEART** | Deep, steady, calm, even rhythm; reassuring | Reliable, never rushes | — |
| **LIVER** | Low-mid, slow, dry and a little weary; unflappable | The overworked filter that has seen it all | — |
| **LUNGS** | Soft, airy, unhurried; gentle breaths between phrases (natural, not exaggerated) | Calm and patient | — |
| **KIDNEYS** | Brisk, tidy, matter-of-fact | Neat cleaners who like order | — |
| **IMMUNE CELLS** | Crisp, alert, team-like; short sentences | A small security squad | — |

New organs or characters get a row here before their first line is written.

## Used so far

| Episode | Voice | Line |
|---|---|---|
| ep01 Food Coma | STOMACH | "Hey, food has arrived, we've got work to do." |
