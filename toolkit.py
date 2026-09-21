"""
toolkit.py — Reusable visual components for the concurrency video series.

Design notes
------------
- Typography: Inter (falls back to Noto Sans if not installed) for body.
  JetBrains Mono (falls back to Noto Sans Mono) for code / monospace.
- Titles use MEDIUM weight (500), not BOLD (700) — cleaner, less shouty.
- Auto-clears media/texts/ on import so a corrupted SVG from a previous
  parallel render never crashes a fresh run.
- No Scene subclasses live here. Every partN_*.py does
  `from toolkit import *` and defines only Scene subclasses.

Install extra fonts for best results:
    apt-get install -y fonts-inter fonts-jetbrains-mono
If they're missing, Pango silently falls back to Noto Sans / Noto Sans Mono,
which are already present via fonts-noto-core.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from manim import *

# ---------------------------------------------------------------------------
# Cache hygiene — runs before any Text() is constructed
# ---------------------------------------------------------------------------
if os.environ.get("MANIM_NO_CACHE_CLEAR") != "1":
    for base in (Path.cwd(), Path(__file__).resolve().parent):
        cache = base / "media" / "texts"
        if cache.exists():
            shutil.rmtree(cache, ignore_errors=True)


# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONT      = "Inter"
MONO_FONT = "JetBrains Mono"

# Weights — MEDIUM reads clean; SEMIBOLD used for emphasis only.
W_TITLE = "MEDIUM"
W_BODY  = "NORMAL"
W_EMPH  = "SEMIBOLD"

# Sizes
SZ_TITLE    = 44
SZ_SUBTITLE = 22
SZ_BODY     = 24
SZ_LABEL    = 22
SZ_SMALL    = 20
SZ_TINY     = 18
SZ_COUNTER  = 32


def T(text, *, size=None, font_size=None,
      weight=W_BODY, color=WHITE, mono=False, **kw):
    """Shorthand for Text() with the project's typography defaults.

    Accepts `size=` (project convention) or `font_size=` (Manim convention).
    Pass `mono=True` for the monospace family.
    """
    if size is None:
        size = font_size if font_size is not None else SZ_BODY
    return Text(
        text,
        font=MONO_FONT if mono else FONT,
        font_size=size,
        weight=weight,
        color=color,
        **kw,
    )


# ---------------------------------------------------------------------------
# Palette — one fixed color per thread, reused across all chapters
# ---------------------------------------------------------------------------
THREAD_A = BLUE_C
THREAD_B = RED_C
THREAD_C = GREEN_C
THREAD_D = YELLOW_C
THREAD_E = PURPLE_C

SHARED_C = GREY_B
LOCK_C   = ORANGE
SEM_C    = PURPLE_A
CV_C     = TEAL_C
BUFFER_C = GREY_D
HILITE   = YELLOW


# ---------------------------------------------------------------------------
# Visual primitives
# ---------------------------------------------------------------------------
class ThreadDot(VGroup):
    """A colored circle with a short label — visual stand-in for a thread."""

    def __init__(self, label, color, radius=0.32, **kwargs):
        super().__init__(**kwargs)
        circle = Circle(radius=radius, color=color, fill_opacity=0.85,
                        stroke_width=1.5)
        txt = T(label, size=SZ_LABEL, weight=W_EMPH, color=WHITE).move_to(circle)
        self.circle, self.label_mob = circle, txt
        self.add(circle, txt)


class SharedBox(VGroup):
    """A box representing shared state / a shared resource."""

    def __init__(self, label="shared", value="", width=2.6, height=1.0,
                 color=SHARED_C, **kwargs):
        super().__init__(**kwargs)
        rect = RoundedRectangle(corner_radius=0.15, width=width, height=height,
                                color=color, stroke_width=1.5, fill_opacity=0.12)
        name = T(label, size=SZ_LABEL, weight=W_TITLE).move_to(
            rect.get_center() + UP * 0.18)
        self.value_text = T(str(value), size=SZ_BODY, weight=W_EMPH,
                            color=HILITE).move_to(rect.get_center() + DOWN * 0.18)
        self.rect, self.name = rect, name
        self.add(rect, name, self.value_text)

    def set_value(self, value):
        new = T(str(value), size=SZ_BODY, weight=W_EMPH,
                color=HILITE).move_to(self.value_text)
        return Transform(self.value_text, new)


class LockIcon(VGroup):
    """A padlock that can be open or closed via .open_anim() / .close_anim()."""

    def __init__(self, label="mutex", **kwargs):
        super().__init__(**kwargs)
        body = RoundedRectangle(corner_radius=0.08, width=0.60, height=0.50,
                                color=LOCK_C, fill_opacity=0.35,
                                stroke_width=1.5).shift(DOWN * 0.15)
        shackle = Arc(radius=0.19, start_angle=0, angle=PI,
                      color=LOCK_C, stroke_width=2).shift(UP * 0.10)
        txt = T(label, size=SZ_TINY, weight=W_BODY,
                color=LOCK_C).next_to(body, DOWN, buff=0.12)
        self.body, self.shackle = body, shackle
        self.add(body, shackle, txt)

    def open_anim(self):
        return self.shackle.animate.shift(RIGHT * 0.16 + UP * 0.06).rotate(-PI / 6)

    def close_anim(self):
        return self.shackle.animate.shift(LEFT * 0.16 + DOWN * 0.06).rotate(PI / 6)


class SemaphoreCounter(VGroup):
    """Semaphore visualised as a counter box with a live integer value."""

    def __init__(self, value=1, label="sem", **kwargs):
        super().__init__(**kwargs)
        rect = RoundedRectangle(corner_radius=0.12, width=1.2, height=0.95,
                                color=SEM_C, fill_opacity=0.22, stroke_width=1.5)
        name = T(label, size=SZ_TINY, weight=W_TITLE,
                 color=SEM_C).next_to(rect, UP, buff=0.10)
        self.value_text = T(str(value), size=SZ_COUNTER, weight=W_EMPH,
                            color=WHITE).move_to(rect)
        self.rect = rect
        self.add(rect, name, self.value_text)

    def set_value(self, value):
        new = T(str(value), size=SZ_COUNTER, weight=W_EMPH,
                color=WHITE).move_to(self.value_text)
        return Transform(self.value_text, new)


class CVBox(VGroup):
    """A labelled box representing a condition variable."""

    def __init__(self, label="cond_var", **kwargs):
        super().__init__(**kwargs)
        rect = RoundedRectangle(corner_radius=0.12, width=2.0, height=0.8,
                                color=CV_C, fill_opacity=0.20, stroke_width=1.5)
        name = T(label, size=SZ_SMALL, weight=W_TITLE, color=CV_C).move_to(rect)
        self.rect = rect
        self.add(rect, name)


class BufferQueue(VGroup):
    """A row of slots for producer/consumer style problems."""

    def __init__(self, n_slots=5, slot_size=0.7, **kwargs):
        super().__init__(**kwargs)
        self.n_slots = n_slots
        self.slots = VGroup(*[
            Square(side_length=slot_size, color=GREY_B, stroke_width=1.5)
            for _ in range(n_slots)
        ]).arrange(RIGHT, buff=0.05)
        self.contents = [None] * n_slots
        self.add(self.slots)

    def fill_slot(self, idx, color=GREEN_C, label=None):
        slot = self.slots[idx]
        item = Square(side_length=slot.side_length * 0.8, color=color,
                      fill_opacity=0.85).move_to(slot)
        if label is not None:
            item = VGroup(item, T(str(label), size=SZ_TINY).move_to(slot))
        self.contents[idx] = item
        return item

    def empty_slot(self, idx):
        item = self.contents[idx]
        self.contents[idx] = None
        return item


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------
def section_title(text, subtitle=None):
    """Standard chapter-open header: title + optional subtitle at the top."""
    title = T(text, size=SZ_TITLE, weight=W_TITLE, color=WHITE)
    group = VGroup(title)
    if subtitle:
        sub = T(subtitle, size=SZ_SUBTITLE, weight=W_BODY, color=GREY_B)
        sub.next_to(title, DOWN, buff=0.25)
        group.add(sub)
    group.to_edge(UP, buff=0.7)
    return group


def thread_strip(labels_colors, x=-5.2, y_top=2.0, gap=0.9):
    """A vertical strip of ThreadDots — useful for a 'cast of threads' intro."""
    dots = VGroup()
    for i, (lbl, col) in enumerate(labels_colors):
        dots.add(ThreadDot(lbl, col).move_to([x, y_top - i * gap, 0]))
    return dots


def problem_header(name, tagline, invariants):
    """Common header used by every advanced problem scene.

    Returns (title_group, invariant_group). Add both to the scene:
        title, inv = problem_header(...)
        self.play(Write(title))
        ...
        self.play(Write(inv))
    """
    title = section_title(name, tagline)
    inv = VGroup(*[
        T(f"• {i}", size=SZ_SMALL, color=GREY_A) for i in invariants
    ]).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
    return title, inv