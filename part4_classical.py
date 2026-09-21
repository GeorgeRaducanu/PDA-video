from manim import *
from toolkit import *


class Ch15_SignalingMultiplex(Scene):
    def construct(self):
        title = section_title("Ch 15 — Signaling & Multiplex", "basic building blocks")
        self.play(Write(title))

        # Signaling
        sem = SemaphoreCounter(0, "signal").shift(LEFT * 4)
        ta = ThreadDot("A", THREAD_A).shift(LEFT * 6 + DOWN * 2)
        tb = ThreadDot("B", THREAD_B).shift(LEFT * 2 + DOWN * 2)
        self.play(Create(sem), FadeIn(ta), FadeIn(tb))
        self.play(ta.animate.next_to(sem, LEFT, buff=0.5), sem.set_value(1))
        self.play(tb.animate.next_to(sem, RIGHT, buff=0.5), sem.set_value(0))
        self.wait(0.8)

        # Multiplex
        mux = SemaphoreCounter(3, "mux").shift(RIGHT * 4 + UP * 1)
        group = VGroup(*[ThreadDot(f"T{i}", c) for i, c in enumerate(
            [THREAD_A, THREAD_B, THREAD_C, THREAD_D])]).arrange(RIGHT, buff=0.4).shift(RIGHT * 4 + DOWN * 2)
        self.play(Create(mux), FadeIn(group))
        for i in range(4):
            t = group[i]
            target = 3 - min(i, 3)
            self.play(t.animate.shift(UP * 0.5), mux.set_value(target), run_time=0.3)
        note = Text("Multiplex: semaphore initialized to N allows N concurrent accesses.",
                    font_size=22, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note))
        self.wait(2)


class Ch16_ProducerConsumer(Scene):
    def construct(self):
        title = section_title("Ch 16 — Producer–Consumer",
                              "bounded buffer · semaphores vs CV")
        self.play(Write(title))

        buf = BufferQueue(5, 0.9).shift(UP * 0.5)
        prod = ThreadDot("P", THREAD_A).shift(LEFT * 5 + UP * 0.5)
        cons = ThreadDot("C", THREAD_B).shift(RIGHT * 5 + UP * 0.5)
        empty = SemaphoreCounter(5, "empty").shift(LEFT * 4 + DOWN * 2)
        full  = SemaphoreCounter(0, "full").shift(RIGHT * 4 + DOWN * 2)

        self.play(Create(buf), FadeIn(prod), FadeIn(cons),
                  Create(empty), Create(full))

        for i in range(3):
            item = buf.fill_slot(i, color=YELLOW, label=i)
            self.play(prod.animate.shift(RIGHT * 0.5), FadeIn(item),
                      empty.set_value(5 - i - 1), full.set_value(i + 1), run_time=0.4)
            self.play(prod.animate.shift(LEFT * 0.5), run_time=0.2)

        for i in range(2):
            item = buf.empty_slot(i)
            self.play(cons.animate.shift(LEFT * 0.5), FadeOut(item) if item else Wait(),
                      full.set_value(3 - i - 1), empty.set_value(2 + i + 1), run_time=0.4)
            self.play(cons.animate.shift(RIGHT * 0.5), run_time=0.2)

        # Correct order warning
        warn = Text("Wait on 'full' before 'empty' can deadlock — always decrement resources first.",
                    font_size=20, color=RED).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(warn))
        self.wait(2)


class Ch17_ReadersWriters(Scene):
    def construct(self):
        title = section_title("Ch 17 — Readers–Writers",
                              "readers' priority · writers' priority · fair")
        self.play(Write(title))

        shared = SharedBox("data", width=3).shift(DOWN * 0.5)
        readers = VGroup(*[ThreadDot(f"R{i}", THREAD_A) for i in range(3)]).arrange(RIGHT, buff=0.5).shift(UP * 2)
        writer = ThreadDot("W", THREAD_B).shift(UP * 3.5 + RIGHT * 3)

        self.play(Create(shared), FadeIn(readers), FadeIn(writer))

        # R/W locks visualization
        rw = VGroup(
            Text("read_count = 0", font="Monospace", font_size=22, color=THREAD_A),
            Text("write_locked = false", font="Monospace", font_size=22, color=THREAD_B),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DL, buff=0.7)
        self.play(Write(rw))

        # Multiple readers in
        for r in readers:
            self.play(r.animate.next_to(shared, UP, buff=0.3), run_time=0.25)
        self.wait(0.5)
        # Last reader leaves → writer wakes
        for r in readers:
            self.play(r.animate.shift(UP * 2), run_time=0.2)
        self.play(writer.animate.next_to(shared, UP, buff=0.3), Indicate(shared.rect, color=THREAD_B))

        note = VGroup(
            Text("Readers' priority: writers may starve", font_size=22, color=YELLOW),
            Text("Writers' priority: turnstile semaphore adds fairness", font_size=22, color=GREEN),
        ).arrange(DOWN).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(2)


class Ch18_DiningPhilosophers(Scene):
    def construct(self):
        title = section_title("Ch 18 — Dining Philosophers",
                              "naive deadlock · waiter · ordering · Chandy/Misra")
        self.play(Write(title))

        center = DOWN * 0.5
        table = Circle(radius=1.2, color=GREY_B).move_to(center)
        philosophers = VGroup()
        forks = VGroup()
        import math
        for i in range(5):
            a = i * 2 * PI / 5 + PI / 2
            px, py = 2.2 * math.cos(a), 2.2 * math.sin(a)
            philosophers.add(ThreadDot(f"P{i}", [THREAD_A, THREAD_B, THREAD_C,
                                                  THREAD_D, THREAD_E][i]).move_to(center + [px, py, 0]))
            fa = a + PI / 5
            fx, fy = 1.4 * math.cos(fa), 1.4 * math.sin(fa)
            forks.add(Line(center + [fx * 0.6, fy * 0.6, 0], center + [fx, fy, 0],
                           color=LOCK_C, stroke_width=4))

        self.play(Create(table), FadeIn(philosophers), Create(forks))

        # Naive: everyone grabs left fork
        for i, p in enumerate(philosophers):
            self.play(Indicate(forks[i], color=RED), run_time=0.2)
        deadlock = Text("DEADLOCK", color=RED, font_size=36).move_to(center)
        self.play(Flash(center, color=RED, line_length=1), Write(deadlock))
        self.wait(0.7)
        self.play(FadeOut(deadlock))

        # Fix: waiter / resource ordering
        fix = VGroup(
            Text("Fix 1: resource ordering (grab lower index first)", font_size=22),
            Text("Fix 2: waiter (semaphore limits concurrent grabbers to 4)", font_size=22),
            Text("Fix 3: Chandy/Misra (dirty/clean tokens)", font_size=22, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)
        self.play(Write(fix))
        self.wait(2)


class Ch19_NoStarveMutex(Scene):
    def construct(self):
        title = section_title("Ch 19 — No-Starve Mutex", "fairness guarantees")
        self.play(Write(title))

        mutex = LockIcon("mutex").shift(LEFT * 3 + UP * 1)
        room_empty = SemaphoreCounter(1, "room_empty").shift(RIGHT * 3 + UP * 1)
        turnstile  = SemaphoreCounter(0, "turnstile").shift(RIGHT * 3 + DOWN * 1.5)

        threads = VGroup(*[ThreadDot(f"T{i}", c) for i, c in
                          enumerate([THREAD_A, THREAD_B, THREAD_C])]).arrange(DOWN, buff=0.7).shift(LEFT * 6 + DOWN * 1)
        self.play(FadeIn(mutex), FadeIn(room_empty), FadeIn(turnstile), FadeIn(threads))

        for idx, t in enumerate(threads):
            self.play(t.animate.next_to(turnstile, DOWN, buff=0.8).shift(RIGHT * idx * 1.2),
                    run_time=0.3)
        self.play(Indicate(turnstile, color=YELLOW))

        note = VGroup(
            Text("turnstile forces FCFS ordering — no starvation", font_size=22, color=YELLOW),
            Text("room_empty serializes critical section", font_size=22),
        ).arrange(DOWN).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)