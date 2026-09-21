from manim import *
from toolkit import *


class Ch01_IntroConcurrency(Scene):
    def construct(self):
        title = section_title("Ch 01 — Introduction to Concurrency",
                              "race conditions · critical section · atomicity")
        self.play(Write(title))

        # Two threads stepping through the same code
        code = VGroup(
            Text("x = x + 1", font="Monospace", font_size=28),
            Text("x = x + 1", font="Monospace", font_size=28),
        ).arrange(DOWN, buff=1.2).shift(RIGHT * 2)

        ta = ThreadDot("A", THREAD_A).move_to(LEFT * 4 + UP * 1)
        tb = ThreadDot("B", THREAD_B).move_to(LEFT * 4 + DOWN * 1)
        shared = SharedBox("x", "0", width=2.2).move_to(RIGHT * 2.5 + DOWN * 2.5)

        self.play(FadeIn(ta), FadeIn(tb), Create(shared))

        # Interleaved read-modify-write
        for t, col in [(ta, THREAD_A), (tb, THREAD_B)]:
            self.play(t.animate.next_to(code[0] if t is ta else code[1],
                                        LEFT, buff=0.5),
                      Indicate(shared.rect, color=col, scale_factor=1.05))
        self.play(shared.set_value(1), run_time=0.4)
        self.play(Indicate(shared.rect, color=HILITE))
        self.wait(0.3)

        # Emphasize lost update
        lost = Text("lost update!", color=RED, font_size=30).next_to(shared, RIGHT)
        self.play(FadeIn(lost, shift=LEFT))
        self.wait(1.5)
        self.play(FadeOut(VGroup(ta, tb, code, shared, lost, title)))

        # Recap card
        recap = VGroup(
            Text("Critical section: code that must run atomically", font_size=26),
            Text("Race condition: result depends on interleaving", font_size=26),
            Text("Atomicity: indivisible unit of execution", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP * 0.3)
        self.play(Write(recap))
        self.wait(2)


class Ch02_AtomicOps(Scene):
    def construct(self):
        title = section_title("Ch 02 — Atomic Operations & Memory Ordering",
                              "CAS · test-and-set · fetch-and-add · barriers")
        self.play(Write(title))

        # Show CAS as a single indivisible action
        cas = VGroup(
            Text("CAS(addr, expected, new):", font="Monospace", font_size=28),
            Text("  atomically: if *addr == expected: *addr = new", font="Monospace", font_size=24),
            Text("  return success/failure", font="Monospace", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT).shift(UP * 0.5)
        self.play(Write(cas))

        # Visualize a CAS loop
        loop_box = RoundedRectangle(width=6, height=1.2, corner_radius=0.15,
                                    color=THREAD_A).shift(DOWN * 1.5)
        loop_txt = Text("while not CAS(x, old, old+1): old = x", font="Monospace",
                        font_size=22).move_to(loop_box)
        self.play(Create(loop_box), Write(loop_txt))
        self.play(Indicate(loop_box, color=HILITE))

        self.wait(1)
        self.play(FadeOut(VGroup(cas, loop_box, loop_txt, title)))

        # Memory ordering
        ordering = VGroup(
            Text("Memory ordering matters:", font_size=30, color=YELLOW),
            Text("x = 1        // may be reordered", font="Monospace", font_size=24),
            Text("flag = true  // by the CPU or compiler", font="Monospace", font_size=24),
            Text("→ use acquire/release fences", font_size=24, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(Write(ordering))
        self.wait(2)


class Ch03_Futex(Scene):
    def construct(self):
        title = section_title("Ch 03 — Futex & the Kernel's Role",
                              "fast userspace mutex — the foundation of blocking locks")
        self.play(Write(title))

        # Fast path vs slow path
        user = RoundedRectangle(width=5, height=2.2, corner_radius=0.2,
                                color=THREAD_A).shift(LEFT * 3 + UP * 0.2)
        kern = RoundedRectangle(width=5, height=2.2, corner_radius=0.2,
                                color=THREAD_B).shift(RIGHT * 3 + UP * 0.2)
        user_t = Text("Userspace", color=THREAD_A, font_size=24).next_to(user, UP, buff=0.15)
        kern_t = Text("Kernel", color=THREAD_B, font_size=24).next_to(kern, UP, buff=0.15)

        fast = Text("CAS on futex word → success", font_size=22).move_to(user)
        slow = Text("FUTEX_WAIT → sleep", font_size=22).move_to(kern)

        self.play(Create(user), Create(kern), Write(user_t), Write(kern_t))
        self.play(Write(fast))
        arrow = Arrow(user.get_right(), kern.get_left(), color=YELLOW)
        self.play(GrowArrow(arrow), Write(slow))
        self.wait(1)

        note = Text("Fast path: no syscall. Slow path: kernel arbitrates.",
                    font_size=22, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(note))
        self.wait(2)