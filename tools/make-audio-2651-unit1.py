#!/usr/bin/env python3
"""Generate the demo voice narration for 2651 Unit 1 (ভাষা).

Reads tools/audio-2651-unit1-script.txt (sectioned by '## ' headers),
renders each section with Google TTS (gTTS, lang='bn'), inserts 0.6s of
silence between sections, and concatenates everything into
db/audio/2651-unit1-bhasha.mp3.

Why gTTS and not a neural voice: the VM's egress proxy breaks the
WebSocket upgrade that edge-tts (Microsoft neural voices) needs, and
gTTS over plain HTTPS works. The voice is therefore Google Translate
TTS -- clear, but synthetic, not a human voice. State that plainly.

Re-run: python3 tools/make-audio-2651-unit1.py
"""
import os
import subprocess
import sys
import time

from gtts import gTTS

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "tools", "audio-2651-unit1-script.txt")
OUT_DIR = os.path.join(REPO, "db", "audio")
TMP_DIR = "/tmp/audio-2651-unit1"
OUT_MP3 = os.path.join(OUT_DIR, "2651-unit1-bhasha.mp3")
SILENCE_SEC = 0.6


def parse_script(path):
    """Return [(title, text), ...] from '## ' sections."""
    sections = []
    title, lines = None, []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line.startswith("#") and not line.startswith("## "):
                continue
            if line.startswith("## "):
                if title is not None:
                    sections.append((title, " ".join(lines).strip()))
                title, lines = line[3:].strip(), []
            elif line:
                lines.append(line)
    if title is not None:
        sections.append((title, " ".join(lines).strip()))
    return [(t, x) for t, x in sections if x]


def tts(text, out_path, tries=3):
    for attempt in range(1, tries + 1):
        try:
            gTTS(text=text, lang="bn", slow=False).save(out_path)
            return True
        except Exception as e:  # noqa: BLE001 - retry transient TTS errors
            print(f"  attempt {attempt} failed: {e}", flush=True)
            time.sleep(2 * attempt)
    return False


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {r.stderr[:400]}")
    return r.stdout.strip()


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries",
                      "format=duration", "-of", "csv=p=0", path]))


def main():
    sections = parse_script(SCRIPT)
    print(f"{len(sections)} sections")
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)

    silence = os.path.join(TMP_DIR, "silence.mp3")
    run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i",
         f"anullsrc=r=24000:cl=mono", "-t", str(SILENCE_SEC),
         "-c:a", "libmp3lame", "-b:a", "96k", silence])

    parts = []
    total_chars = 0
    for i, (title, text) in enumerate(sections, 1):
        part = os.path.join(TMP_DIR, f"section-{i:02d}.mp3")
        print(f"[{i}/{len(sections)}] {title} ({len(text)} chars)", flush=True)
        if not tts(text, part):
            print(f"FAILED: section {i} ({title})")
            return 1
        total_chars += len(text)
        print(f"    -> {duration(part):.1f}s", flush=True)
        parts.append(part)
        if i < len(sections):
            parts.append(silence)

    concat_list = os.path.join(TMP_DIR, "concat.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", concat_list, "-c:a", "libmp3lame", "-b:a", "96k", OUT_MP3])

    d = duration(OUT_MP3)
    size = os.path.getsize(OUT_MP3)
    print(f"DONE: {OUT_MP3}")
    print(f"  sections: {len(sections)}, chars: {total_chars}")
    print(f"  duration: {d:.1f}s ({int(d // 60)}:{int(d % 60):02d}), size: {size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
