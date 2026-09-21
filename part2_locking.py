from manim import *
from toolkit import *


class Ch04_Spinlocks(Scene):
    def construct(self):
        title = section_title("Ch 04 — Spinlocks", "test-and-set · TTAS · backoff")
        self.play(Write(title))

        lock = LockIcon("spinlock").shift(UP * 1.0)
        ta = ThreadDot("A", THREAD_A).to_edge(LEFT, buff=1.5)
        tb = ThreadDot("B", THREAD_B).to_edge(LEFT, buff=1.5).shift(DOWN * 2)

        self.play(FadeIn(ta), FadeIn(tb), FadeIn(lock))

        # A acquires
        self.play(ta.animate.next_to(lock, LEFT, buff=1), lock.close_anim())
        self.wait(0.3)

        # B spins
        spin_text = Text("while (!CAS(lock, 0, 1));", font="Monospace",
                         font_size=24, color=RED).next_to(tb, RIGHT, buff=0.5)
        self.play(tb.animate.next_to(lock, DOWN, buff=1), FadeIn(spin_text))
        for _ in range(3):
            self.play(Indicate(lock.rect if hasattr(lock, "rect") else lock.body,
                               color=RED, scale_factor=1.1), run_time=0.4)

        # A releases
        self.play(lock.open_anim())
        self.play(tb.animate.next_to(lock, LEFT, buff=1), lock.close_anim(),
                  FadeOut(spin_text))
        self.wait(1)

        # TTAS / backoff note
        note = VGroup(
            Text("TTAS: test with a plain read, only CAS if free", font_size=22),
            Text("Backoff: pause between retries to reduce contention", font_size=22),
        ).arrange(DOWN).to_edge(DOWN, buff=0.8)
        self.play(Write(note))
        self.wait(2)


class Ch05_Mutexes(Scene):
    def construct(self):
        title = section_title("Ch 05 — Mutexes", "blocking locks · sleep/wakeup")
        self.play(Write(title))

        lock = LockIcon("mutex").shift(UP * 1.5)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 4 + UP * 0.5)
        tb = ThreadDot("B", THREAD_B).shift(LEFT * 4 + DOWN * 1.5)
        waitq = RoundedRectangle(width=2.0, height=1.2, corner_radius=0.15,
                                 color=GREY_C).shift(RIGHT * 4 + DOWN * 1.5)
        wait_t = Text("wait queue", font_size=20).next_to(waitq, UP, buff=0.1)

        self.play(FadeIn(ta), FadeIn(tb), FadeIn(lock), Create(waitq), Write(wait_t))

        self.play(ta.animate.next_to(lock, LEFT, buff=0.8), lock.close_anim())
        self.wait(0.2)
        # B blocks instead of spinning
        self.play(tb.animate.move_to(waitq.get_center()))
        self.wait(0.5)
        self.play(lock.open_anim())
        self.play(tb.animate.next_to(lock, LEFT, buff=0.8), lock.close_anim())
        self.wait(1)

        note = Text("No busy-waiting: blocked threads sleep in the kernel.",
                    font_size=22, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(note))
        self.wait(2)


class Ch06_RWLock(Scene):
    def construct(self):
        title = section_title("Ch 06 — Read-Write Locks",
                              "many readers OR one writer")
        self.play(Write(title))

        shared = SharedBox("resource", width=3.5).shift(DOWN * 1.5)
        readers = VGroup(*[ThreadDot(f"R{i}", THREAD_A) for i in range(3)]).arrange(RIGHT, buff=0.6).shift(UP * 0.5)
        writer = ThreadDot("W", THREAD_B).shift(UP * 0.5 + RIGHT * 3)

        self.play(Create(shared), FadeIn(readers), FadeIn(writer))

        # Readers enter together
        for r in readers:
            self.play(r.animate.next_to(shared, UP, buff=0.4), run_time=0.3)
        self.wait(0.7)
        for r in readers:
            self.play(r.animate.shift(UP * 1.5), run_time=0.25)

        # Writer waits, then exclusive
        self.play(writer.animate.next_to(shared, UP, buff=0.4))
        self.play(Indicate(writer, color=YELLOW))
        self.play(writer.animate.next_to(shared, DOWN, buff=0.4))
        self.wait(1.2)

        note = VGroup(
            Text("Readers: shared access — many at once", font_size=22, color=THREAD_A),
            Text("Writer: exclusive access — alone", font_size=22, color=THREAD_B),
        ).arrange(DOWN).to_edge(DOWN, buff=0.7)
        self.play(Write(note))
        self.wait(2)


class Ch07_Reentrant(Scene):
    def construct(self):
        title = section_title("Ch 07 — Reentrant / Recursive Locks",
                              "same thread may re-acquire")
        self.play(Write(title))

        lock = LockIcon("recursive").shift(UP * 1.5)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 4 + UP * 0.5)

        counter = SharedBox("owner count", "0", width=2.4, height=1.0).shift(RIGHT * 2 + DOWN * 1.5)

        self.play(FadeIn(ta), FadeIn(lock), Create(counter))
        self.play(ta.animate.next_to(lock, LEFT, buff=0.8), lock.close_anim(),
                  counter.set_value(1))
        self.wait(0.3)
        # Re-acquire (same thread)
        self.play(Indicate(ta, color=GREEN), counter.set_value(2))
        self.wait(0.3)
        # Release
        self.play(counter.set_value(1))
        self.play(counter.set_value(0), lock.open_anim())

        note = Text("Tracks owning thread + recursion depth; only owner may unlock.",
                    font_size=22, color=YELLOW).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(note))
        self.wait(2)