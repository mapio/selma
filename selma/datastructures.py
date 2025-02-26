from collections import deque

from manim import (
  Line,
  Rectangle,
  VGroup,
  RIGHT,
  LEFT,
  UL,
  UR,
  DR,
  DL,
  FadeIn,
  FadeOut,
  Animation,
  AnimationGroup,
  Succession,
)

from selma import FOREGROUND, BACKGROUND

class MQueue:
  def __init__(self, width=10, height=1.1, scale=1):
    self.scale = scale
    self.queue = deque()
    rect = Rectangle(width=width, height=height).scale(scale)
    self.trbl_sides = [
      Line(rect.get_corner(UL), rect.get_corner(UR), color=FOREGROUND),
      Line(rect.get_corner(UR), rect.get_corner(DR), color=FOREGROUND),
      Line(rect.get_corner(DR), rect.get_corner(DL), color=FOREGROUND),
      Line(rect.get_corner(DL), rect.get_corner(UL), color=FOREGROUND)
    ]
    self.rect = VGroup(self.trbl_sides)

  def enqueue(self, re) -> Animation:
    re.next_to(self.rect, LEFT)
    succ = [
      AnimationGroup(
        FadeIn(re), self.trbl_sides[3].animate.set_opacity(0), run_time=0.5
      )
    ]
    self.queue.appendleft(re)
    buff = 0
    shift = []
    for e in self.queue:
      buff += e.width + 0.2 * self.scale
      shift.append(e.animate.next_to(self.rect, LEFT, buff=-buff))
    succ.append(AnimationGroup(shift))
    succ.append(self.trbl_sides[3].animate.set_opacity(1))
    return Succession(succ)

  def dequeue(self) -> Animation:
    e = self.queue.pop()
    return Succession(
      AnimationGroup(self.trbl_sides[1].animate.set_opacity(0), run_time=0.5),
      e.animate.next_to(self.rect, RIGHT),
      AnimationGroup(
        self.trbl_sides[1].animate.set_opacity(1), FadeOut(e), run_time=0.5
      ),
    )


class MStack:
  def __init__(self, width=10, height=1.1, scale=1):
    self.scale = scale
    self.stack = deque()
    rect = Rectangle(width=width, height=height, color=FOREGROUND).scale(scale)
    self.trbl_sides = [
      Line(rect.get_corner(UL), rect.get_corner(UR)),
      Line(rect.get_corner(UR), rect.get_corner(DR)),
      Line(rect.get_corner(DR), rect.get_corner(DL)),
      Line(rect.get_corner(DL), rect.get_corner(UL)),
    ]
    self.rect = VGroup(self.trbl_sides)

  def push(self, re) -> Animation:
    re.next_to(self.rect, RIGHT)
    succ = [
      AnimationGroup(
        FadeIn(re), self.trbl_sides[1].animate.set_opacity(0), run_time=0.5
      )
    ]
    self.stack.append(re)
    buff = 0
    shift = []
    for e in self.stack:
      buff += e.width + 0.2 * self.scale
      shift.append(e.animate.next_to(self.rect, LEFT, buff=-buff))
    succ.append(AnimationGroup(shift))
    succ.append(self.trbl_sides[1].animate.set_opacity(2))
    return Succession(succ)

  def pop(self) -> Animation:
    e = self.stack.pop()
    return Succession(
      AnimationGroup(
        self.trbl_sides[1].animate.set_opacity(0),
        run_time=0.5,
      ),
      e.animate.next_to(self.rect, RIGHT),
      AnimationGroup(
        self.trbl_sides[1].animate.set_opacity(1), FadeOut(e), run_time=0.5
      ),
    )
