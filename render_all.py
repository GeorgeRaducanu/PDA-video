#!/usr/bin/env python3
"""
render_all.py — Render the entire concurrency video series, sequentially.

Just run:
    python render_all.py

Renders every Scene in every part file, one at a time, with live output.
No parallelism, no subprocess cache races, no corrupted SVGs.
Clears the text cache once at start; then runs each scene serially.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
MEDIA_DIR = PROJECT_DIR / "media" / "videos"
TEXT_CACHE_DIR = PROJECT_DIR / "media" / "texts"
LOG_DIR = PROJECT_DIR / "render_logs"
LOG_DIR.mkdir(exist_ok=True)

PART_FILES = [
    "part1_foundations.py",
    "part2_locking.py",
    "part3_coordination.py",
    "part4_classical.py",
    "part5_advanced.py",
]

QUALITY = os.environ.get("MANIM_QUALITY", "-pql")
SKIP_EXISTING = "--skip-existing" in sys.argv
KEEP_GOING = "--keep-going" in sys.argv

SCENE_RE = re.compile(r"^class\s+(Ch\d+_\w+)\s*\(\s*Scene\s*\)", re.MULTILINE)
QUALITY_DIR = {
    "-ql": "480p15", "-qm": "720p30", "-qh": "1080p60", "-qk": "2160p60",
    "-pql": "480p15", "-pqm": "720p30", "-pqh": "1080p60", "-pqk": "2160p60",
}


def scenes_in(path: Path) -> list[str]:
    return SCENE_RE.findall(path.read_text(encoding="utf-8"))


def already_rendered(part: Path, scene: str) -> bool:
    qdir = QUALITY_DIR.get(QUALITY, "480p15")
    return (MEDIA_DIR / part.stem / qdir / f"{scene}.mp4").exists()


def main() -> int:
    if shutil.which("manim") is None:
        print("manim not on PATH", file=sys.stderr)
        return 2

    files = [PROJECT_DIR / f for f in PART_FILES]
    files = [f for f in files if f.exists()]
    if not files:
        print("no part files found", file=sys.stderr)
        return 2

    # --- clear text cache once, before anything else -----------------------
    if TEXT_CACHE_DIR.exists():
        shutil.rmtree(TEXT_CACHE_DIR, ignore_errors=True)
        print(f"Cleared text cache: {TEXT_CACHE_DIR}")

    # --- build work list ---------------------------------------------------
    work: list[tuple[Path, str]] = []
    for f in files:
        for s in scenes_in(f):
            if SKIP_EXISTING and already_rendered(f, s):
                continue
            work.append((f, s))

    if not work:
        print("nothing to render.")
        return 0

    total = len(work)
    print(f"Rendering {total} scene(s) sequentially at quality {QUALITY}.")
    print(f"Logs → {LOG_DIR}\n")

    ok = fail = 0
    elapsed = 0.0

    for i, (part, scene) in enumerate(work, 1):
        name = f"{part.stem}.{scene}"
        log_path = LOG_DIR / f"{name}.log"
        cmd = ["manim", QUALITY, part.name, scene]

        print(f"[{i:>3}/{total}] {name} ... ", end="", flush=True)
        t0 = time.perf_counter()
        with open(log_path, "wb") as fh:
            rc = subprocess.call(cmd, cwd=PROJECT_DIR,
                                 stdout=fh, stderr=subprocess.STDOUT)
        dt = time.perf_counter() - t0
        elapsed += dt

        if rc == 0:
            ok += 1
            print(f"OK   {dt:6.1f}s")
        else:
            fail += 1
            print(f"ERR  {dt:6.1f}s   → {log_path.relative_to(PROJECT_DIR)}")
            if not KEEP_GOING:
                print("\nStopping at first failure. "
                      "Re-run with --keep-going to continue past errors.")
                break

    print(f"\nDone. {ok} ok, {fail} failed, {elapsed:.1f}s total.")
    if fail:
        print(f"Failed scene logs are in: {LOG_DIR}")
    print(f"Output: {MEDIA_DIR}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())