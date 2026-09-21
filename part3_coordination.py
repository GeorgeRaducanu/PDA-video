from manim import *
from toolkit import *


class Ch08_ConditionVariables(Scene):
    def construct(self):
        title = section_title("Ch 08 — Condition Variables",
                              "wait · signal · broadcast · predicate loops")
        self.play(Write(title))

        cv = CVBox("cond_var").shift(RIGHT * 3 + UP * 1)
        mutex = LockIcon("mutex").shift(LEFT * 3 + UP * 1)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 5 + DOWN * 1.5)
        tb = ThreadDot("B", THREAD_B).shift(RIGHT * 5 + DOWN * 1.5)

        self.play(FadeIn(cv), FadeIn(mutex), FadeIn(ta), FadeIn(tb))

        # A acquires mutex, waits on cv
        self.play(ta.animate.next_to(mutex, RIGHT, buff=0.6), mutex.close_anim())
        self.play(ta.animate.next_to(cv, LEFT, buff=0.8))
        wait_lbl = Text("wait()", color=YELLOW, font_size=22).next_to(ta, DOWN, buff=0.1)
        self.play(FadeIn(wait_lbl))
        self.wait(0.5)

        # B signals
        self.play(tb.animate.next_to(cv, RIGHT, buff=0.8))
        sig_lbl = Text("signal()", color=GREEN, font_size=22).next_to(tb, DOWN, buff=0.1)
        self.play(FadeIn(sig_lbl), Indicate(cv.rect, color=GREEN))
        self.play(FadeOut(wait_lbl))
        self.play(ta.animate.next_to(mutex, RIGHT, buff=0.6))
        self.wait(0.6)
        self.play(mutex.open_anim())

        # Predicate-loop note
        note = VGroup(
            Text("wait() must be inside a while(predicate) loop:", font_size=22),
            Text("  spurious wakeups; signal may be to the wrong thread", font_size=20,
                 color=GREY_B),
        ).arrange(DOWN).to_edge(DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(2)


class Ch09_Monitors(Scene):
    def construct(self):
        title = section_title("Ch 09 — Monitors",
                              "encapsulated shared state + implicit mutex + CVs")
        self.play(Write(title))

        monitor = RoundedRectangle(width=8, height=4, corner_radius=0.3, color=THREAD_C)
        m_t = Text("Monitor", color=THREAD_C, font_size=24).next_to(monitor, UP, buff=0.15)
        state = SharedBox("shared state", width=3, height=1).shift(UP * 0.8)
        method = VGroup(
            Text("method_1()", font="Monospace", font_size=22),
            Text("method_2()", font="Monospace", font_size=22),
            Text("method_3()", font="Monospace", font_size=22),
        ).arrange(RIGHT, buff=0.8).shift(DOWN * 1.0)
        cv = CVBox("cv").shift(DOWN * 2.3)

        self.play(Create(monitor), Write(m_t))
        self.play(Create(state), Write(method), FadeIn(cv))

        # Only one thread inside
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 6)
        tb = ThreadDot("B", THREAD_B).shift(LEFT * 6 + DOWN * 1.5)
        self.play(FadeIn(ta), FadeIn(tb))
        self.play(ta.animate.next_to(monitor, LEFT, buff=0.3))
        self.play(Indicate(monitor, color=THREAD_A), tb.animate.shift(RIGHT * 1.5))
        self.wait(1)
        self.play(ta.animate.shift(LEFT * 4), tb.animate.next_to(monitor, LEFT, buff=0.3))
        self.wait(1)

        note = Text("Implicit lock — one active thread at a time inside.",
                    font_size=22, color=YELLOW).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note))
        self.wait(2)


class Ch10_Semaphores(Scene):
    def construct(self):
        title = section_title("Ch 10 — Semaphores", "wait (P) · signal (V)")
        self.play(Write(title))

        sem = SemaphoreCounter(value=2, label="S").shift(RIGHT * 3 + UP * 1)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 4 + UP * 2)
        tb = ThreadDot("B", THREAD_B).shift(LEFT * 4 + UP * 0.3)
        tc = ThreadDot("C", THREAD_C).shift(LEFT * 4 + DOWN * 1.4)

        self.play(Create(sem), FadeIn(ta), FadeIn(tb), FadeIn(tc))
        for t in (ta, tb):
            self.play(t.animate.next_to(sem, LEFT, buff=1), sem.set_value(2 if t is ta else 1))
        # C blocks
        self.play(tc.animate.next_to(sem, DOWN, buff=1), Indicate(sem.rect, color=RED))
        self.wait(0.5)
        # A signals
        self.play(ta.animate.shift(LEFT * 4), sem.set_value(2))
        self.play(tc.animate.next_to(sem, LEFT, buff=1), sem.set_value(1))
        self.wait(1)

        # Implementation using mutex + cv
        impl = VGroup(
            Text("Implementation:", font_size=24, color=YELLOW),
            Text("wait(S):  lock(m); while (S==0) cv_wait(cv); S--; unlock(m)", font="Monospace", font_size=20),
            Text("signal(S):lock(m); S++; cv_signal(cv); unlock(m)", font="Monospace", font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
        self.play(Write(impl))
        self.wait(2)


class Ch11_Rendezvous(Scene):
    def construct(self):
        title = section_title("Ch 11 — Rendezvous", "two threads wait for each other")
        self.play(Write(title))

        line = DashedLine(UP * 2 + LEFT * 3, UP * 2 + RIGHT * 3, color=YELLOW)
        lbl = Text("rendezvous point", font_size=22, color=YELLOW).next_to(line, UP, buff=0.15)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 4 + UP * 2)
        tb = ThreadDot("B", THREAD_B).shift(RIGHT * 4 + UP * 2)

        self.play(Create(line), Write(lbl), FadeIn(ta), FadeIn(tb))
        self.play(ta.animate.next_to(line, LEFT, buff=0.1))
        self.wait(0.7)
        self.play(tb.animate.next_to(line, RIGHT, buff=0.1))
        self.wait(0.5)
        self.play(Flash(line, color=YELLOW))
        self.play(ta.animate.shift(DOWN * 3 + RIGHT * 2),
                  tb.animate.shift(DOWN * 3 + LEFT * 2))
        self.wait(1)

        note = VGroup(
            Text("aArrived = Semaphore(0)", font="Monospace", font_size=22),
            Text("bArrived = Semaphore(0)", font="Monospace", font_size=22),
            Text("A: aArrived.signal(); bArrived.wait()", font="Monospace", font_size=22),
            Text("B: bArrived.signal(); aArrived.wait()", font="Monospace", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)


class Ch12_Barriers(Scene):
    def construct(self):
        title = section_title("Ch 12 — Barriers",
                              "simple · reusable · sense-reversing · tree")
        self.play(Write(title))

        # n threads arrive
        bar = Rectangle(width=8, height=0.3, color=YELLOW).shift(DOWN * 1)
        lbl = Text("barrier", font_size=22, color=YELLOW).next_to(bar, RIGHT, buff=0.2)
        threads = VGroup(*[ThreadDot(f"T{i}", [THREAD_A, THREAD_B, THREAD_C, THREAD_D][i])
                          for i in range(4)]).arrange(RIGHT, buff=1.2).shift(UP * 2)
        self.play(Create(bar), Write(lbl), FadeIn(threads))

        for i, t in enumerate(threads):
            self.play(t.animate.next_to(bar, UP, buff=0.4 + i * 0.001).shift(RIGHT * (i - 1.5) * 1.8),
                      run_time=0.35)
        self.wait(0.4)
        self.play(Flash(bar, color=YELLOW, line_length=1))
        for t in threads:
            self.play(t.animate.shift(DOWN * 3), run_time=0.25)

        note = VGroup(
            Text("Reusable: sense-reversing counter (flip phase each round)", font_size=22),
            Text("Tree barrier: O(log n) contention", font_size=22, color=YELLOW),
        ).arrange(DOWN).to_edge(DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(2)


class Ch13_Latches(Scene):
    def construct(self):
        title = section_title("Ch 13 — Latches & One-Shot Primitives",
                              "CountDownLatch · once-flags · CyclicBarrier")
        self.play(Write(title))

        latch = SemaphoreCounter(value=3, label="count").shift(UP * 0.5)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 4 + DOWN * 1.5)
        tb = ThreadDot("B", THREAD_B).shift(LEFT * 1.5 + DOWN * 1.5)
        tc = ThreadDot("C", THREAD_C).shift(RIGHT * 1.5 + DOWN * 1.5)
        waiter = ThreadDot("W", THREAD_D).shift(RIGHT * 4 + UP * 0.5)

        self.play(Create(latch), FadeIn(ta), FadeIn(tb), FadeIn(tc), FadeIn(waiter))
        self.play(waiter.animate.next_to(latch, RIGHT, buff=0.8), Indicate(waiter, color=YELLOW))
        for i, t in enumerate((ta, tb, tc)):
            self.play(t.animate.next_to(latch, DOWN, buff=0.8).shift(LEFT * (1 - i) * 1.5),
                      latch.set_value(3 - i - 1), run_time=0.4)
        self.play(Flash(latch, color=GREEN))
        self.play(waiter.animate.shift(UP * 1.5))
        self.wait(1)

        note = VGroup(
            Text("Latch: opened once, never reset (vs. CyclicBarrier: reusable)", font_size=22),
            Text("Once-flag: idempotent initialization", font_size=22, color=YELLOW),
        ).arrange(DOWN).to_edge(DOWN, buff=0.6)
        self.play(Write(note))
        self.wait(2)


class Ch14_ThreadPool(Scene):
    def construct(self):
        title = section_title("Ch 14 — Thread Pool Pattern",
                              "workers + blocking queue + graceful shutdown")
        self.play(Write(title))

        queue = BufferQueue(n_slots=5, slot_size=0.9).shift(UP * 2)
        q_lbl = Text("task queue", font_size=22).next_to(queue, UP, buff=0.2)
        workers = VGroup(*[ThreadDot(f"W{i}", c) for i, c in
                          enumerate([THREAD_A, THREAD_B, THREAD_C, THREAD_D])]).arrange(RIGHT, buff=0.6).shift(DOWN * 1.5)
        clients = VGroup(*[ThreadDot(f"C{i}", GREY_B) for i in range(2)]).arrange(RIGHT, buff=0.6).shift(UP * 4)

        self.play(Create(queue), Write(q_lbl), FadeIn(workers), FadeIn(clients))

        # Clients submit
        for i in range(3):
            item = queue.fill_slot(i, color=YELLOW)
            self.play(clients[0].animate.shift(DOWN * 0.5), FadeIn(item), run_time=0.3)
            self.play(clients[0].animate.shift(UP * 0.5), run_time=0.2)
        self.wait(0.5)

        # Workers consume
        for i, w in enumerate(workers[:3]):
            item = queue.empty_slot(i)
            self.play(w.animate.shift(UP * 1.5), FadeOut(item) if item else Wait(), run_time=0.3)
            self.play(w.animate.shift(DOWN * 1.5), run_time=0.25)

        note = VGroup(
            Text("Idle workers block on the queue's condition variable", font_size=22),
            Text("Bounds thread count → protects memory & CPU", font_size=22, color=YELLOW),
        ).arrange(DOWN).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(2)