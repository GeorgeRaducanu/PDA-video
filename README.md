# PDA-video

# Concurrency & Synchronization — Manim Video Series

An educational, silent (no narration) Manim video series covering the
fundamentals of concurrency and synchronization, plus the classical and
non-classical synchronization problems.

Style: 3b1b-like — dark background, colored threads, animated shared state,
clean typography. Every chapter is a standalone Manim `Scene` and can be
rendered independently.

---

## Table of contents

1. [Project structure](#project-structure)
2. [Prerequisites](#prerequisites)
3. [Quick start](#quick-start)
4. [Rendering a single chapter](#rendering-a-single-chapter)
5. [Rendering everything](#rendering-everything)
6. [Full chapter list](#full-chapter-list)
7. [Quality presets](#quality-presets)
8. [Troubleshooting](#troubleshooting)
9. [Design conventions](#design-conventions)

---

## Project structure

```
PDA-video/
├── toolkit.py                # reusable visual components (no scenes)
├── part1_foundations.py      # Ch01–Ch03
├── part2_locking.py          # Ch04–Ch07
├── part3_coordination.py     # Ch08–Ch14
├── part4_classical.py        # Ch15–Ch19
├── part5_advanced.py         # Ch20–Ch34
├── render_all.py             # batch renderer (Python)
├── render_logs/              # auto-created; per-scene logs on failure
├── media/                    # auto-created by Manim; final MP4s here
└── README.md
```

The key rule: **`toolkit.py` contains no scenes**. Every `partN_*.py` file
imports from `toolkit` and defines only `Scene` subclasses.

---

## Prerequisites

### With Docker (recommended)

Use the provided Dockerfile / devcontainer. It ships with Manim, FFmpeg,
LaTeX, Pango, and all the fonts the series uses.

```dockerfile
FROM manimcommunity/manim:stable

USER root
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        fontconfig \
        fonts-dejavu \
        fonts-liberation2 \
        fonts-noto-core \
        xdg-utils \
        vlc && \
    fc-cache -fv && \
    rm -rf /var/lib/apt/lists/*

USER manimuser
```

If you use the devcontainer, open the folder in VS Code and choose
**Dev Containers: Reopen in Container**.

### Without Docker

You need:

- Python 3.11 or 3.12 (**avoid 3.14** — Manim 0.21 has known issues there)
- Manim Community Edition ≥ 0.18
- FFmpeg
- A LaTeX distribution (TeX Live or MiKTeX)
- Pango + at least one font family (DejaVu / Liberation / Noto)

```bash
pip install manim
```

Verify the install:

```bash
manim --version
fc-list | wc -l    # must be > 0
```

---

## Quick start

From the project root:

```bash
# Render one scene and preview it
manim -pql part2_locking.py Ch04_Spinlocks

# Render the whole series at draft quality
python render_all.py

# Render the whole series at 1080p60
MANIM_QUALITY=-pqh python render_all.py
```

Output lands in `media/videos/<file>/<quality>/<Scene>.mp4`.

---

## Rendering a single chapter

General form:

```bash
manim [quality] <part_file.py> <SceneName>
```

Examples:

```bash
manim -pql part1_foundations.py Ch01_IntroConcurrency
manim -pqh part4_classical.py Ch16_ProducerConsumer
manim -s   part5_advanced.py Ch34_FaneuilHall   # save last frame only
```

**Render every scene in one file** (Manim iterates them alphabetically):

```bash
manim -pql part4_classical.py
```

Manim flags you will actually use:

| Flag | Meaning |
|------|---------|
| `-p` | Preview the video after rendering |
| `-q l / m / h / k` | Quality: low / medium / high / 4K |
| `-s` | Save the last frame only (PNG) |
| `-o name` | Override output filename |
| `--disable_caching` | Ignore Manim's partial-movie cache |

---

## Rendering everything

`render_all.py` renders all 34 scenes across all 5 part files.

```bash
# Default: draft quality (-pql), warmup serial, then parallel
python render_all.py

# 1080p60 finals
MANIM_QUALITY=-pqh python render_all.py

# Skip scenes that already have an MP4
python render_all.py --skip-existing

# Override parallelism (default: min(4, cpu_count))
python render_all.py --jobs=8
```

### How it works

1. **Warmup phase** — the first scene renders serially with live output.
   This populates `__pycache__` and `media/` so the parallel phase does
   not race on shared files. If warmup fails, the script stops
   immediately and shows you why.
2. **Parallel phase** — the remaining scenes render with a capped job
   count (default `min(4, cpu_count)`). Each scene runs in its own
   subprocess, so they are fully isolated.
3. **Failure logs** — any scene that fails writes a full log to
   `render_logs/<file>.<Scene>.log`.

### Environment variables

| Variable | Default | Meaning |
|----------|---------|---------|
| `MANIM_QUALITY` | `-pql` | Quality preset used by `render_all.py` |

### CLI flags

| Flag | Meaning |
|------|---------|
| `--jobs=N` | Number of parallel render jobs |
| `--skip-existing` | Skip scenes whose MP4 already exists |

---

## Full chapter list

### PART I — Foundations

| # | Scene name | File | Topic |
|---|------------|------|-------|
| 01 | `Ch01_IntroConcurrency` | `part1_foundations.py` | Race conditions, critical section, atomicity |
| 02 | `Ch02_AtomicOps` | `part1_foundations.py` | CAS, test-and-set, memory ordering |
| 03 | `Ch03_Futex` | `part1_foundations.py` | Fast userspace mutex, kernel arbitration |

### PART II — Locking Primitives

| # | Scene name | File | Topic |
|---|------------|------|-------|
| 04 | `Ch04_Spinlocks` | `part2_locking.py` | TAS lock, TTAS, backoff |
| 05 | `Ch05_Mutexes` | `part2_locking.py` | Blocking locks, wait queues |
| 06 | `Ch06_RWLock` | `part2_locking.py` | Read-write locks |
| 07 | `Ch07_Reentrant` | `part2_locking.py` | Recursive locks, owner tracking |

### PART III — Coordination Primitives

| # | Scene name | File | Topic |
|---|------------|------|-------|
| 08 | `Ch08_ConditionVariables` | `part3_coordination.py` | wait / signal / broadcast, predicate loops |
| 09 | `Ch09_Monitors` | `part3_coordination.py` | Encapsulated state + implicit mutex |
| 10 | `Ch10_Semaphores` | `part3_coordination.py` | P/V operations, implementation |
| 11 | `Ch11_Rendezvous` | `part3_coordination.py` | Two-thread handshake |
| 12 | `Ch12_Barriers` | `part3_coordination.py` | Simple, reusable, sense-reversing, tree |
| 13 | `Ch13_Latches` | `part3_coordination.py` | CountDownLatch, once-flags |
| 14 | `Ch14_ThreadPool` | `part3_coordination.py` | Worker pool + task queue |

### PART IV — Classical Problems

| # | Scene name | File | Topic |
|---|------------|------|-------|
| 15 | `Ch15_SignalingMultiplex` | `part4_classical.py` | Basic signaling and multiplex patterns |
| 16 | `Ch16_ProducerConsumer` | `part4_classical.py` | Bounded buffer, semaphores vs CV |
| 17 | `Ch17_ReadersWriters` | `part4_classical.py` | Readers' priority, writers' priority, fair |
| 18 | `Ch18_DiningPhilosophers` | `part4_classical.py` | Deadlock, waiter, ordering, Chandy/Misra |
| 19 | `Ch19_NoStarveMutex` | `part4_classical.py` | Fairness, turnstile, FCFS |

### PART V — Advanced Problems

| # | Scene name | File | Topic |
|---|------------|------|-------|
| 20 | `Ch20_CigaretteSmokers` | `part5_advanced.py` | Agent + 3 smokers |
| 21 | `Ch21_RiverCrossing` | `part5_advanced.py` | Hacker/serf rules |
| 22 | `Ch22_RollerCoaster` | `part5_advanced.py` | Car waits for full load |
| 23 | `Ch23_MultiCarRollerCoaster` | `part5_advanced.py` | Multiple cars, global track lock |
| 24 | `Ch24_UnisexBathroom` | `part5_advanced.py` | One gender at a time, no starvation |
| 25 | `Ch25_BaboonCrossing` | `part5_advanced.py` | Directional rope, weight limit |
| 26 | `Ch26_ModusHall` | `part5_advanced.py` | Ratio constraints |
| 27 | `Ch27_ChildCare` | `part5_advanced.py` | Parents leave, children stay |
| 28 | `Ch28_SearchInsertDelete` | `part5_advanced.py` | Concurrent list operations |
| 29 | `Ch29_SushiBar` | `part5_advanced.py` | Seats and wasabi constraints |
| 30 | `Ch30_SantaClaus` | `part5_advanced.py` | Reindeer + elves synchronization |
| 31 | `Ch31_BuildingH2O` | `part5_advanced.py` | Two H + one O bond |
| 32 | `Ch32_RoomParty` | `part5_advanced.py` | Dean's rules |
| 33 | `Ch33_SenateBus` | `part5_advanced.py` | Bus boards all waiting riders |
| 34 | `Ch34_FaneuilHall` | `part5_advanced.py` | Immigrants & spectators, reversible decisions |

---

## Quality presets

| Flag | Resolution | FPS | Use case |
|------|------------|-----|----------|
| `-ql` | 854×480 | 15 | Fast preview during authoring |
| `-qm` | 1280×720 | 30 | Intermediate |
| `-qh` | 1920×1080 | 60 | Final publish |
| `-qk` | 3840×2160 | 60 | 4K |
| `-pql` etc. | same as above | | Add `-p` to preview after render |

Draft the whole series with `-pql`, publish with `-pqh`.

---

## Troubleshooting

### `ParseError: no element found: line 1, column 0` at first `Text()`

Pango is emitting an empty SVG because it cannot find a font.

```bash
fc-list | wc -l
```

If `0` (or the command is missing):

```bash
apt-get update && apt-get install -y \
    fontconfig fonts-dejavu fonts-liberation2 fonts-noto-core
fc-cache -fv
```

Then rebuild your Docker image / devcontainer so the fix is permanent.

### Random scene failures when rendering in parallel

You are running too many Manim processes on a cold cache. The default
`render_all.py` caps parallelism and warms up serially. If you overrode
`--jobs` and see failures, lower it back to 4.

### `ModuleNotFoundError: No module named 'toolkit'`

You ran `manim` from a directory other than the project root. Fix:

```bash
cd PDA-video
manim -pql part4_classical.py Ch16_ProducerConsumer
```

Or prepend the path:

```bash
PYTHONPATH=. manim -pql part4_classical.py Ch16_ProducerConsumer
```

### Python 3.14 issues

Manim 0.21 has known problems on Python 3.14 (Pango/SVG generation).
Use Python 3.11 or 3.12, or the official `manimcommunity/manim` image.

### Where did my MP4 go?

```
media/videos/<part_file_stem>/<quality_dir>/<SceneName>.mp4
```

For example:

```
media/videos/part4_classical/480p15/Ch16_ProducerConsumer.mp4
```

---

## Design conventions

Every scene in this series follows the same visual grammar. If you add
a new chapter, stick to these rules — consistency is what makes the
series feel coherent.

- **One color per thread.** Use the constants `THREAD_A`, `THREAD_B`, …
  from `toolkit.py`. Never invent new colors per scene.
- **Four recurring glyphs.** `SharedBox`, `LockIcon`, `SemaphoreCounter`,
  `CVBox`. Reuse them; do not invent new icons.
- **Every scene starts with `section_title(...)`.** That gives the whole
  series a consistent "chapter open" beat.
- **Bad → good pattern.** For problems that have a naive failing solution,
  always animate the failure first, then the fix. This is the single most
  memorable teaching pattern from 3b1b.
- **No narration.** All meaning must be carried by motion, color, and
  labels on the screen.
- **Class names match the chapter number.** `Ch16_ProducerConsumer`, not
  `ProducerConsumer`. This keeps alphabetical render order equal to
  chapter order.

### Adding a new chapter

1. Pick the right `partN_*.py` file.
2. Add a new class named `ChXX_<Topic>(Scene)`.
3. Import helpers with `from toolkit import *` (already at the top).
4. Start `construct()` with `section_title("Ch XX — Title", "subtitle")`.
5. Use `ThreadDot`, `SharedBox`, `LockIcon`, `SemaphoreCounter`, `CVBox`
   for all visuals.
6. Add the new class to the tables above.

---

## License / attribution

Problems and their canonical solutions follow the structure of
*The Little Book of Semaphores* by Allen B. Downey (Green Tea Press),
which is freely available at
<https://greenteapress.com/semaphores/LittleBookOfSemaphores.pdf>.
The course ordering also draws from the MobyLab Parallel & Distributed
course notes.
