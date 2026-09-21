from manim import *
from toolkit import *


def problem_header(name, tagline, invariants):
    title = section_title(name, tagline)
    inv = VGroup(*[Text(f"• {i}", font_size=20, color=GREY_A) for i in invariants]
                 ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
    return title, inv


class Ch20_CigaretteSmokers(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 20 — Cigarette Smokers",
            "agent supplies 2 of 3 ingredients; smoker holds the third",
            ["agent.signal two ingredients",
             "each smoker waits on its own semaphore",
             "finish → signal agent"])
        self.play(Write(title))

        table = SharedBox("table", width=3).shift(UP * 0.5)
        agent = ThreadDot("Agent", GREY_B).shift(LEFT * 5 + UP * 2)
        smokers = VGroup(*[ThreadDot(s, c) for s, c in
                          [("Tobacco", THREAD_A), ("Paper", THREAD_B), ("Match", THREAD_C)]
                          ]).arrange(RIGHT, buff=1.4).shift(DOWN * 2)

        self.play(FadeIn(agent), Create(table), FadeIn(smokers))
        self.play(agent.animate.next_to(table, LEFT, buff=0.6))
        self.play(Indicate(table.rect, color=YELLOW))
        self.play(Flash(smokers[0], color=YELLOW), smokers[0].animate.shift(UP * 0.5))
        self.play(Write(inv))
        self.wait(2)


class Ch21_RiverCrossing(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 21 — River Crossing",
            "boat rowers · hacker/serf rules",
            ["boat capacity = 4",
             "cannot mix unless full boat of 4",
             "barrier each trip"])
        self.play(Write(title))

        river = Rectangle(width=12, height=2, color=BLUE_E, fill_opacity=0.3)
        boat = RoundedRectangle(width=2, height=0.7, corner_radius=0.15, color=YELLOW).shift(DOWN * 0.5)
        hackers = VGroup(*[ThreadDot(f"H{i}", THREAD_A) for i in range(3)]).arrange(RIGHT, buff=0.4).to_edge(LEFT).shift(UP * 2)
        serfs = VGroup(*[ThreadDot(f"S{i}", THREAD_B) for i in range(3)]).arrange(RIGHT, buff=0.4).to_edge(LEFT).shift(DOWN * 2)

        self.play(Create(river), FadeIn(boat), FadeIn(hackers), FadeIn(serfs))
        # Full boat
        for i in range(2):
            self.play(hackers[i].animate.move_to(boat.get_center() + LEFT * 0.5 + RIGHT * i * 0.5),
                      run_time=0.3)
        for i in range(2):
            self.play(serfs[i].animate.move_to(boat.get_center() + RIGHT * 0.5 + RIGHT * i * 0.5 + DOWN * 0.001),
                      run_time=0.3)
        self.play(boat.animate.shift(RIGHT * 6), run_time=1.2)
        self.play(Write(inv))
        self.wait(1.5)


class Ch22_RollerCoaster(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 22 — Roller Coaster",
            "car waits for full load; riders wait for empty car",
            ["car capacity n",
             "allAboard + allAshore barriers",
             "load/unload mutual exclusion"])
        self.play(Write(title))

        car = RoundedRectangle(width=4, height=1, corner_radius=0.2, color=YELLOW).shift(DOWN * 0.5)
        track = Line(LEFT * 5 + DOWN * 2, RIGHT * 5 + DOWN * 2, color=GREY)
        riders = VGroup(*[ThreadDot(f"R{i}", THREAD_A) for i in range(4)]).arrange(RIGHT, buff=0.4).shift(UP * 2)
        self.play(Create(track), FadeIn(car), FadeIn(riders))
        for i, r in enumerate(riders):
            self.play(r.animate.move_to(car.get_center() + LEFT * 1.5 + RIGHT * i), run_time=0.3)
        self.play(car.animate.shift(RIGHT * 6), run_time=1.0)
        self.play(Write(inv))
        self.wait(1.5)


class Ch23_MultiCarRollerCoaster(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 23 — Multi-Car Roller Coaster",
            "several cars circulate simultaneously",
            ["per-car mutex + capacity",
             "global track mutex",
             "board/off barriers per car"])
        self.play(Write(title))
        track = Line(LEFT * 5 + DOWN * 2, RIGHT * 5 + DOWN * 2, color=GREY)
        cars = VGroup(*[RoundedRectangle(width=2, height=0.7, corner_radius=0.15, color=YELLOW)
                        .shift(LEFT * (3 - i * 2.5) + DOWN * 2 + UP * 0.4)
                        for i in range(3)])
        riders = VGroup(*[ThreadDot(f"R{i}", c) for i, c in enumerate(
            [THREAD_A, THREAD_B, THREAD_C, THREAD_D])]).arrange(RIGHT, buff=0.4).shift(UP * 2)
        self.play(Create(track), FadeIn(cars), FadeIn(riders))
        for i, r in enumerate(riders):
            self.play(r.animate.move_to(cars[i % 3].get_center()), run_time=0.3)
        self.play(cars.animate.shift(RIGHT * 2), run_time=1.0)
        self.play(Write(inv))
        self.wait(1.5)


class Ch24_UnisexBathroom(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 24 — Unisex Bathroom",
            "room occupied by one gender at a time; no starvation",
            ["count_{m|f}, mutex, empty",
             "turnstile for fairness",
             "first-in / last-out pattern"])
        self.play(Write(title))
        bath = RoundedRectangle(width=4, height=3, corner_radius=0.2, color=TEAL_C).shift(UP * 0.3)
        bath_t = Text("bathroom", color=TEAL_C, font_size=22).next_to(bath, UP, buff=0.1)
        men = VGroup(*[ThreadDot(f"M{i}", THREAD_A) for i in range(2)]).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=1)
        women = VGroup(*[ThreadDot(f"W{i}", THREAD_B) for i in range(2)]).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1)
        self.play(Create(bath), Write(bath_t), FadeIn(men), FadeIn(women))
        for idx, m in enumerate(men):
            self.play(m.animate.move_to(bath.get_center() + LEFT * 0.5 + UP * (0.5 - 0.5 * idx)),
                    run_time=0.35)
        self.wait(0.5)
        for idx, m in enumerate(men):
            self.play(m.animate.to_edge(LEFT, buff=1).shift(DOWN * (0.5 * idx)),
                    run_time=0.25)
        for idx, w in enumerate(women):
            self.play(w.animate.move_to(bath.get_center() + RIGHT * 0.5 + UP * (0.5 - 0.5 * idx)),
                    run_time=0.35)
        
        self.play(Write(inv))
        self.wait(1.5)


class Ch25_BaboonCrossing(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 25 — Baboon Crossing",
            "rope supports one direction + limited weight",
            ["mutex protects direction/counter",
             "wait on opposite-direction semaphore",
             "no starvation between groups"])
        self.play(Write(title))
        rope = Line(LEFT * 5 + DOWN * 0.5, RIGHT * 5 + DOWN * 0.5, color=YELLOW, stroke_width=4)
        left = VGroup(*[ThreadDot(f"L{i}", THREAD_A) for i in range(2)]).arrange(DOWN, buff=0.4).shift(LEFT * 6)
        right = VGroup(*[ThreadDot(f"R{i}", THREAD_B) for i in range(2)]).arrange(DOWN, buff=0.4).shift(RIGHT * 6)
        self.play(Create(rope), FadeIn(left), FadeIn(right))
        for l in left:
            self.play(l.animate.move_to(rope.get_start() + UP * 0.3), run_time=0.3)
            self.play(l.animate.move_to(rope.get_end() + DOWN * 0.3), run_time=0.6)
        self.play(Write(inv))
        self.wait(1.5)


class Ch26_ModusHall(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 26 — Modus Hall",
            "mixed use with ratio constraints",
            ["capacity + ratio invariant",
             "mutex + two CVs (mods/halls)",
             "no starvation between groups"])
        self.play(Write(title))
        hall = RoundedRectangle(width=6, height=3, corner_radius=0.2, color=THREAD_C).shift(UP * 0.3)
        mods = VGroup(*[ThreadDot(f"M{i}", THREAD_A) for i in range(3)]).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.7)
        halls = VGroup(*[ThreadDot(f"H{i}", THREAD_B) for i in range(3)]).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.7)
        self.play(Create(hall), FadeIn(mods), FadeIn(halls))
        self.play(mods.animate.move_to(hall.get_center() + LEFT * 1.5), run_time=0.6)
        self.play(halls.animate.move_to(hall.get_center() + RIGHT * 1.5), run_time=0.6)
        self.play(Write(inv))
        self.wait(1.5)


class Ch27_ChildCare(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 27 — Child Care",
            "parents arrive with children; center has finite capacity",
            ["mutex + capacity semaphore",
             "parents must leave (children stay)",
             "wait/tryToLeave protocol"])
        self.play(Write(title))
        center = RoundedRectangle(width=5, height=3, corner_radius=0.2, color=THREAD_C).shift(UP * 0.2)
        parents = VGroup(*[ThreadDot(f"P{i}", THREAD_A) for i in range(2)]).shift(LEFT * 6)
        children = VGroup(*[ThreadDot(f"c{i}", THREAD_B) for i in range(3)]).arrange(DOWN, buff=0.3).shift(RIGHT * 6)
        self.play(Create(center), FadeIn(parents), FadeIn(children))
        for p in parents:
            self.play(p.animate.move_to(center.get_center() + LEFT * 0.5), run_time=0.4)
            self.play(p.animate.shift(LEFT * 4), run_time=0.3)
        self.play(children.animate.move_to(center.get_center()), run_time=0.7)
        self.play(Write(inv))
        self.wait(1.5)


class Ch28_SearchInsertDelete(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 28 — Search-Insert-Delete",
            "concurrent list operations with different concurrency classes",
            ["search: no lock",
             "insert: exclusive vs inserters",
             "delete: exclusive vs everyone"])
        self.play(Write(title))
        lst = VGroup(*[Square(side_length=0.6, color=GREY_B) for _ in range(6)]
                     ).arrange(RIGHT, buff=0.05).shift(UP * 0.3)
        searchers = VGroup(*[ThreadDot(f"S{i}", THREAD_A) for i in range(3)]).arrange(RIGHT, buff=0.4).shift(UP * 2)
        mods = VGroup(*[ThreadDot(f"M{i}", THREAD_B) for i in range(2)]).arrange(RIGHT, buff=0.4).shift(DOWN * 2)
        self.play(Create(lst), FadeIn(searchers), FadeIn(mods))
        for s in searchers:
            self.play(s.animate.next_to(lst, UP, buff=0.3), run_time=0.3)
        self.play(Indicate(lst, color=THREAD_A))
        self.play(searchers.animate.shift(UP * 1.5), run_time=0.3)
        for m in mods:
            self.play(m.animate.next_to(lst, DOWN, buff=0.3), run_time=0.3)
        self.play(Write(inv))
        self.wait(1.5)


class Ch29_SushiBar(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 29 — Sushi Bar",
            "seats & wasabi ordering constraints",
            ["mustWait + mutex",
             "per-seat 'canEat' semaphores",
             "barrier of rice/soy/wasabi"])
        self.play(Write(title))
        bar = Line(LEFT * 5 + UP * 0.5, RIGHT * 5 + UP * 0.5, color=YELLOW)
        chef = ThreadDot("Chef", GREY_B).shift(LEFT * 6 + UP * 2)
        seats = VGroup(*[ThreadDot(f"C{i}", [THREAD_A, THREAD_B, THREAD_C, THREAD_D, THREAD_E][i])
                        for i in range(5)]).arrange(RIGHT, buff=0.6).shift(DOWN * 1.5)
        self.play(Create(bar), FadeIn(chef), FadeIn(seats))
        self.play(chef.animate.shift(RIGHT * 1), run_time=0.5)
        self.play(Indicate(seats, color=YELLOW))
        self.play(Write(inv))
        self.wait(1.5)


class Ch30_SantaClaus(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 30 — Santa Claus",
            "Santa sleeps until 9 reindeer OR 3 elves",
            ["mutex, santaSem, reindeerSem, elfTex",
             "reindeer group of 9, elves group of 3",
             "elves are released one at a time"])
        self.play(Write(title))
        santa = ThreadDot("Santa", THREAD_B).shift(LEFT * 5)
        reindeer = VGroup(*[ThreadDot(f"R{i}", THREAD_A) for i in range(4)]
                         ).arrange(DOWN, buff=0.3).shift(RIGHT * 1 + UP * 2)
        elves = VGroup(*[ThreadDot(f"E{i}", THREAD_C) for i in range(3)]
                      ).arrange(DOWN, buff=0.3).shift(RIGHT * 5 + DOWN * 1)
        self.play(FadeIn(santa), FadeIn(reindeer), FadeIn(elves))
        self.play(Indicate(santa, color=YELLOW))
        self.play(reindeer.animate.move_to(santa.get_center() + RIGHT * 1), run_time=0.7)
        self.play(Write(inv))
        self.wait(1.5)


class Ch31_BuildingH2O(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 31 — Building H₂O",
            "two H + one O must bond; groups never mix",
            ["H waits, O waits, mutex",
             "H and O enter with different barriers",
             "release groups atomically"])
        self.play(Write(title))
        center = ORIGIN + DOWN * 0.5
        h_atoms = VGroup(*[ThreadDot("H", THREAD_A) for _ in range(4)]).arrange(RIGHT, buff=0.5).shift(UP * 2)
        o_atoms = VGroup(*[ThreadDot("O", THREAD_B) for _ in range(2)]).arrange(RIGHT, buff=0.5).shift(DOWN * 2)
        molecule = VGroup(ThreadDot("H", THREAD_A).move_to(center + LEFT * 0.5 + UP * 0.3),
                          ThreadDot("H", THREAD_A).move_to(center + RIGHT * 0.5 + UP * 0.3),
                          ThreadDot("O", THREAD_B).move_to(center + DOWN * 0.4))
        self.play(FadeIn(h_atoms), FadeIn(o_atoms))
        self.play(FadeIn(molecule), Flash(molecule, color=YELLOW))
        self.play(Write(inv))
        self.wait(1.5)


class Ch32_RoomParty(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 32 — Room Party",
            "Dean's rules on party attendance",
            ["mutex + capacity",
             "rules for entry/exit are state-dependent",
             "no starvation / liveness"])
        self.play(Write(title))
        room = RoundedRectangle(width=6, height=3, corner_radius=0.2, color=THREAD_C)
        students = VGroup(*[ThreadDot(f"S{i}", THREAD_A) for i in range(4)]
                         ).arrange(RIGHT, buff=0.4).shift(DOWN * 2)
        dean = ThreadDot("Dean", THREAD_B).shift(UP * 3)
        self.play(Create(room), FadeIn(students), FadeIn(dean))
        self.play(students[:2].animate.move_to(room.get_center() + LEFT * 1), run_time=0.6)
        self.play(Indicate(dean, color=YELLOW))
        self.play(Write(inv))
        self.wait(1.5)


class Ch33_SenateBus(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 33 — Senate Bus",
            "bus arrives, boards all waiting riders, then departs",
            ["mutex + riders counter",
             "bus semaphore, allAboard semaphore",
             "bound on bus waiting"])
        self.play(Write(title))
        stop = RoundedRectangle(width=5, height=0.6, corner_radius=0.1, color=GREY_B).shift(UP * 1)
        bus = RoundedRectangle(width=3, height=1.2, corner_radius=0.2, color=YELLOW).shift(LEFT * 6 + DOWN * 1.5)
        riders = VGroup(*[ThreadDot(f"R{i}", THREAD_A) for i in range(5)]
                       ).arrange(RIGHT, buff=0.3).shift(UP * 2.5)
        self.play(Create(stop), FadeIn(bus), FadeIn(riders))
        for i, r in enumerate(riders):
            self.play(r.animate.move_to(stop.get_center() + RIGHT * (i - 2) * 0.5), run_time=0.25)
        self.play(bus.animate.move_to(stop.get_center() + DOWN * 1.2), run_time=0.7)
        self.play(riders.animate.move_to(bus.get_center()), run_time=0.6)
        self.play(bus.animate.shift(RIGHT * 8), run_time=1.0)
        self.play(Write(inv))
        self.wait(1.5)


class Ch34_FaneuilHall(Scene):
    def construct(self):
        title, inv = problem_header(
            "Ch 34 — Faneuil Hall",
            "immigrants & spectators, reversible decisions",
            ["mutex + two counters",
             "spectators may enter when immigrants leave",
             "decisions can flip only when empty"])
        self.play(Write(title))
        hall = RoundedRectangle(width=6, height=3, corner_radius=0.2, color=THREAD_C).shift(UP * 0.3)
        immigrants = VGroup(*[ThreadDot(f"I{i}", THREAD_A) for i in range(3)]).arrange(DOWN, buff=0.3).to_edge(LEFT)
        spectators = VGroup(*[ThreadDot(f"S{i}", THREAD_B) for i in range(3)]).arrange(DOWN, buff=0.3).to_edge(RIGHT)
        judge = ThreadDot("Judge", YELLOW_C).shift(UP * 3)
        self.play(Create(hall), FadeIn(immigrants), FadeIn(spectators), FadeIn(judge))
        self.play(immigrants.animate.move_to(hall.get_center() + LEFT * 1), run_time=0.7)
        self.play(Indicate(judge, color=YELLOW))
        self.play(spectators.animate.move_to(hall.get_center() + RIGHT * 1), run_time=0.7)
        self.play(Write(inv))
        self.wait(2)