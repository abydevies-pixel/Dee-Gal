# Health Channel — Voice Cast

The narrator carries every episode. Now and then an organ speaks a line of its own. These lines should feel like the body briefly talking back, not a cartoon show.

## Rules

1. **The narrator comes first.** Organ lines are rare: usually 1–3 per episode, each one or two short sentences. The narrator sets them up ("Basically telling it,") and then carries on.
2. **Keep it subtle.** Each organ's voice differs from the narrator's through pitch, pace and attitude, never through silly voices, heavy accents, chipmunk pitching, robot effects or echo. A listener should notice the shift without it pulling them out of the story.
3. **One organ, one voice, forever.** Once a voice is set (the same voice actor, or the same TTS voice and settings), reuse it unchanged in every episode, and write its settings into the table below the first time it's recorded.
4. **Mark it in the script.** In `beats.json` a spoken line is `{"text": "...", "voice": "STOMACH"}` and gets its own beat. `build.py` then tags it in the beats list, the PDF, the timeline and `voiceover_script.txt`, so it can be recorded or generated separately and dropped back in.
5. **Show the speaker.** On a spoken beat the organ is on screen with its mouth open, mid-sentence.
6. **Lines stay accurate.** An organ never says anything the science doesn't support.

## Locking the voices (one voice per character, for the whole channel)

1. **Pick each voice once.** Choose one voice actor, or one text-to-speech voice, for the narrator, and one for each organ. Audition with the test lines below.
2. **Write the settings down** in the table: tool, voice name or ID, model, and any speed, pitch, stability or style values. Never change them between episodes.
3. **Keep a reference clip** of about 20–30 seconds for each voice in `health/voices/` (e.g. `narrator.mp3`, `stomach.mp3`). Before recording a new episode, listen to the clip, and with voice-cloning tools, use it as the source.
4. **Same chain every time.** Same microphone and room (or the same TTS settings) and the same post-processing: EQ, compression and loudness target, e.g. −14 LUFS for YouTube.
5. **The narrator is the anchor.** Organ voices are set relative to the narrator (slightly lower, quicker and so on), so if the narrator voice ever had to change, every organ would need re-auditioning. Avoid that.

### Audition lines

| Voice | Test line |
|---|---|
| NARRATOR | "It's lunchtime and you just had a wonderful meal. Except… your eyes are closing." |
| STOMACH | "Hey, food has arrived, we've got work to do." |
| BRAIN | "Okay. Alertness is dropping. Again. Who scheduled lunch at one o'clock?" |
| INTESTINES | "Nutrients in, nutrients sorted, nutrients out, next!" |
| PANCREAS | "Sugar is up. Releasing insulin. Everything's under control." |
| HEART | "Steady. I've got this. Seventy beats a minute." |
| LIVER | "Another one? Fine. I'll filter it." |
| LUNGS | "In… and out. Nice and slow." |
| KIDNEYS | "Clean-up crew, on it." |
| IMMUNE CELLS | "Intruder spotted. Squad, move." |
| TOOTH | "Gently, please. This enamel doesn't grow back." |

## Cast

| Voice | Direction | Personality | Tool / voice ID / settings (fill in once, never change) |
|---|---|---|---|
| **NARRATOR** | Warm, curious, conversational; medium pace; dry humour | A friend who's read the research | — |
| **STOMACH** | Slightly lower and rounder than the narrator; hearty and practical; unhurried, a little proud; like a busy kitchen manager announcing a delivery | Hard-working, food-focused, cheerfully bossy | — |
| **BRAIN** | Clear, slightly higher and quicker than the narrator; precise; a hint of overthinking | The control-room manager, always monitoring | — |
| **INTESTINES** | Mid pitch, quick and chatty; upbeat multitasker | Always busy sorting and absorbing | — |
| **PANCREAS** | Light, polite, measured, precise; like a careful accountant | Quietly keeps the sugar books balanced | — |
| **TOOTH** | Bright, clean, slightly prim; a touch higher than the narrator | Proud of its shine, easily sensitive | — |
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
