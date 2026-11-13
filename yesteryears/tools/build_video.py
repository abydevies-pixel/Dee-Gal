#!/usr/bin/env python3
"""Assemble a Yesteryears episode from beat images + voiceover.

Usage:
  python3 build_video.py timeline EPISODE_DIR            # write timeline.json and timeline.csv (no captions)
  python3 build_video.py build EPISODE_DIR [--res 1920x1080] [--fps 30] [--draft]

EPISODE_DIR must contain beats.json and shots.txt. Optional:
  images/beat_001.png ... beat_377.png   (missing beats get a placeholder card)
  audio/voiceover.mp3 (or .wav/.m4a)     (beat durations are scaled to fit it)
  motion.json                            (overrides: {"40": "shake", "26": "fade"})

Motion types: push (slow push-in, default), pull (slow pull-out), pan (slow left-to-right),
shake (push-in plus a short impact shake), fade (fade up from black, for time jumps).
"""
import json, math, os, subprocess, sys, shutil, csv, glob

WPS = 2.4          # narration speed from the Style DNA
MIN_DUR = 1.2      # shortest beat on screen, seconds

IMPACT = {40, 43, 45, 49, 85, 120, 121, 179, 240, 276, 281, 291, 295}
TIMEJUMP = {12, 26, 36, 73, 119, 208, 219, 232, 301, 310, 332, 338, 366, 373}


def load(ep):
    beats = json.load(open(os.path.join(ep, "beats.json")))
    scenes = {}
    for line in open(os.path.join(ep, "shots.txt")):
        if line.strip():
            n, sc, cam, mood, act = line.rstrip("\n").split("|", 4)
            scenes[int(n)] = dict(scene=sc, cam=cam, mood=mood, action=act)
    over = {}
    mp = os.path.join(ep, "motion.json")
    if os.path.exists(mp):
        over = {int(k): v for k, v in json.load(open(mp)).items()}
    return beats, scenes, over


def audio_file(ep):
    for ext in ("mp3", "wav", "m4a", "aac"):
        p = os.path.join(ep, "audio", f"voiceover.{ext}")
        if os.path.exists(p):
            return p
    return None


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def motion_for(n, over):
    if n in over:
        return over[n]
    if n in IMPACT:
        return "shake"
    if n in TIMEJUMP:
        return "fade"
    return ["push", "push", "pan", "push", "pull"][n % 5]


def ts(sec, srt=True):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        s, ms = int(s) + 1, 0
    sep = "," if srt else "."
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}{sep}{ms:03d}"


def timeline(ep):
    beats, scenes, over = load(ep)
    raw = [max(MIN_DUR, len(b.split()) / WPS) for b in beats]
    a = audio_file(ep)
    scale = 1.0
    if a:
        scale = probe_duration(a) / sum(raw)
    t, rows = 0.0, []
    for i, (b, d) in enumerate(zip(beats, raw), 1):
        d = round(d * scale, 3)
        sc = scenes.get(i, {})
        rows.append(dict(beat=i, start=round(t, 3), dur=d, text=b, motion=motion_for(i, over),
                         scene=sc.get("scene", ""), action=sc.get("action", ""), image=f"images/beat_{i:03d}.png"))
        t += d
    json.dump(rows, open(os.path.join(ep, "timeline.json"), "w"), indent=1)
    with open(os.path.join(ep, "timeline.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["beat", "start", "end", "duration_s", "motion", "scene", "image", "script_segment"])
        for r in rows:
            w.writerow([r["beat"], ts(r["start"], False), ts(r["start"] + r["dur"], False), r["dur"],
                        r["motion"], r["scene"], r["image"], r["text"]])
    print(f"timeline: {len(rows)} beats, {t/60:.1f} min" + (f" (scaled to {os.path.basename(a)})" if a else " (estimated at 2.4 words/s)"))
    return rows


def placeholder(path, r, W, H):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (W, H), (242, 232, 213))
    d = ImageDraw.Draw(img)
    fdir = "/usr/share/fonts/truetype/dejavu/"
    big = ImageFont.truetype(fdir + "DejaVuSerif-Bold.ttf", int(H * 0.042))
    small = ImageFont.truetype(fdir + "DejaVuSerif.ttf", int(H * 0.03))
    d.rectangle([0, 0, W, int(H * 0.09)], fill=(74, 14, 14))
    d.text((int(W * 0.03), int(H * 0.02)), f"BEAT {r['beat']:03d}   ·   {r['scene'].upper()}   ·   {r['motion']}",
           font=small, fill=(242, 232, 213))
    import re
    label = re.sub(r"\{([A-Z0-9]+)\}", lambda m: m.group(1).lower(), r.get("action", ""))
    words, lines, cur = ("[" + label + "]").split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength(test, font=big) > W * 0.85:
            lines.append(cur); cur = w_
        else:
            cur = test
    lines.append(cur)
    y = H / 2 - len(lines) * big.size * 0.65
    for ln in lines:
        d.text(((W - d.textlength(ln, font=big)) / 2, y), ln, font=big, fill=(74, 14, 14))
        y += big.size * 1.3
    d.text((int(W * 0.03), int(H * 0.92)), "placeholder: replace with " + r["image"], font=small, fill=(120, 110, 95))
    img.save(path)


def vf_for(motion, dur, W, H, fps):
    n = max(1, int(round(dur * fps)))
    up = f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2}"
    center = "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    if motion == "pull":
        z = f"z='1.08-0.08*on/{n}'"
    else:
        z = f"z='1+0.07*on/{n}'"
    pos = center
    if motion == "pan":
        z = "z='1.08'"
        pos = f"x='(iw-iw/zoom)*on/{n}':y='ih/2-(ih/zoom/2)'"
    chain = f"{up},zoompan={z}:{pos}:d={n}:s={W}x{H}:fps={fps}"
    if motion == "shake":
        chain += (f",scale={int(W*1.04)}:{int(H*1.04)},"
                  f"crop={W}:{H}:x='(iw-ow)/2+if(lt(t,0.35),{W//90}*sin(t*90),0)':y='(ih-oh)/2+if(lt(t,0.35),{H//90}*cos(t*110),0)'")
    if motion == "fade":
        chain += ",fade=t=in:st=0:d=0.4"
    return chain + ",format=yuv420p"


def build(ep, res="1920x1080", fps=30, draft=False):
    W, H = map(int, res.lower().split("x"))
    rows = timeline(ep)
    out_dir = os.path.join(ep, "output")
    work = os.path.join(out_dir, "_clips")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    preset = ["-preset", "ultrafast", "-crf", "30"] if draft else ["-preset", "medium", "-crf", "18"]
    missing = 0
    with open(os.path.join(work, "list.txt"), "w") as lst:
        for r in rows:
            src = os.path.join(ep, r["image"])
            if not os.path.exists(src):
                missing += 1
                src = os.path.join(work, f"ph_{r['beat']:03d}.png")
                placeholder(src, r, W, H)
            clip = os.path.join(work, f"c_{r['beat']:03d}.mp4")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", src, "-t", f"{r['dur']:.3f}",
                            "-vf", vf_for(r["motion"], r["dur"], W, H, fps), "-r", str(fps),
                            "-c:v", "libx264", *preset, "-an", clip], check=True)
            lst.write(f"file '{os.path.abspath(clip)}'\n")
            if r["beat"] % 50 == 0:
                print(f"  rendered {r['beat']}/{len(rows)} beats")
    silent = os.path.join(work, "video.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(work, "list.txt"), "-c", "copy", silent], check=True)
    a = audio_file(ep)
    name = "animatic.mp4" if missing == len(rows) else ("draft.mp4" if draft else "episode.mp4")
    final = os.path.join(out_dir, name)
    if a:
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", a, "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
    else:
        shutil.move(silent, final)
    shutil.rmtree(work, ignore_errors=True)
    print(f"done: {final}  ({missing} of {len(rows)} beats used placeholders"
          + ("" if a else ", no voiceover found") + ")")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("timeline", "build"):
        print(__doc__); sys.exit(1)
    ep = sys.argv[2]
    if sys.argv[1] == "timeline":
        timeline(ep)
    else:
        args = sys.argv[3:]
        res = args[args.index("--res") + 1] if "--res" in args else "1920x1080"
        fps = int(args[args.index("--fps") + 1]) if "--fps" in args else 30
        build(ep, res, fps, "--draft" in args)
