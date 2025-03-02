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

from selma import FOREGROUND


class MQueue:
  def __init__(self, width=10, height=1.1, scale=1):
    self.scale = scale
    self.queue = deque()
    rect = Rectangle(width=width, height=height).scale(scale)
    self.trbl_sides = [
      Line(rect.get_corner(UL), rect.get_corner(UR), color=FOREGROUND),
      Line(rect.get_corner(UR), rect.get_corner(DR), color=FOREGROUND),
      Line(rect.get_corner(DR), rect.get_corner(DL), color=FOREGROUND),
      Line(rect.get_corner(DL), rect.get_corner(UL), color=FOREGROUND),
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
    rect = Rectangle(width=width, height=height).scale(scale)
    self.trbl_sides = [
      Line(rect.get_corner(UL), rect.get_corner(UR), color=FOREGROUND),
      Line(rect.get_corner(UR), rect.get_corner(DR), color=FOREGROUND),
      Line(rect.get_corner(DR), rect.get_corner(DL), color=FOREGROUND),
      Line(rect.get_corner(DL), rect.get_corner(UL), color=FOREGROUND),
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


class QBag:
  def __init__(self, width, scale):
    self.container = MQueue(width=width, scale=scale)

  def take(self):
    return self.container.dequeue()

  def give(self, n):
    return self.container.enqueue(n)

  def is_empty(self):
    return not self.container.queue

  def peek(self):
    return self.container.queue[-1][1].text


class SBag:
  def __init__(self, width, scale):
    self.container = MStack(width=width, scale=scale)

  def take(self):
    return self.container.pop()

  def give(self, n):
    return self.container.push(n)

  def is_empty(self):
    return not self.container.stack

  def peek(self):
    return self.container.stack[-1][1].text
