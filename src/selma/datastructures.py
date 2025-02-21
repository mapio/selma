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
  WHITE,
  FadeIn,
  FadeOut,
)

from selma.animations import AnimationGroup


class MQueue:
  def __init__(self, width=10, height=1.1, scale=1):
    self.scale = scale
    self.queue = deque()
    rect = Rectangle(width=width, height=height, color=WHITE).scale(scale)
    self.trbl_sides = [
      Line(rect.get_corner(UL), rect.get_corner(UR)),
      Line(rect.get_corner(UR), rect.get_corner(DR)),
      Line(rect.get_corner(DR), rect.get_corner(DL)),
      Line(rect.get_corner(DL), rect.get_corner(UL)),
    ]
    self.rect = VGroup(self.trbl_sides)

  def enqueue(self, re) -> AnimationGroup:
    re.next_to(self.rect, LEFT)
    ag = AnimationGroup()
    ag.append(
      lambda: [FadeIn(re), self.trbl_sides[3].animate.set_opacity(0)],
      name='in',
      run_time=0.5,
    )
    self.queue.appendleft(re)
    buff = 0
    shift = []
    for e in self.queue:
      buff += e.width + 0.2 * self.scale
      shift.append(e.animate.next_to(self.rect, LEFT, buff=-buff))
    ag.append(shift, name='shift')
    ag.append(lambda: [self.trbl_sides[3].animate.set_opacity(1)], name='close')
    return ag

  def dequeue(self) -> AnimationGroup:
    e = self.queue.pop()
    ag = AnimationGroup()
    ag.append(
      lambda: [self.trbl_sides[1].animate.set_opacity(0)],
      name='out',
      run_time=0.5,
    )
    ag.append([e.animate.next_to(self.rect, RIGHT)])
    ag.append(
      lambda: [self.trbl_sides[1].animate.set_opacity(1), FadeOut(e)],
      name='close',
      run_time=0.5,
    )
    return ag


class MStack:
  def __init__(self, width=10, height=1.1, scale=1):
    self.scale = scale
    self.stack = deque()
    rect = Rectangle(width=width, height=height, color=WHITE).scale(scale)
    self.trbl_sides = [
      Line(rect.get_corner(UL), rect.get_corner(UR)),
      Line(rect.get_corner(UR), rect.get_corner(DR)),
      Line(rect.get_corner(DR), rect.get_corner(DL)),
      Line(rect.get_corner(DL), rect.get_corner(UL)),
    ]
    self.rect = VGroup(self.trbl_sides)

  def push(self, re) -> AnimationGroup:
    re.next_to(self.rect, RIGHT)
    ag = AnimationGroup()
    ag.append(
      lambda: [FadeIn(re), self.trbl_sides[1].animate.set_opacity(0)],
      name='in',
      run_time=0.5,
    )
    self.stack.append(re)
    buff = 0
    shift = []
    for e in self.stack:
      buff += e.width + 0.2 * self.scale
      shift.append(e.animate.next_to(self.rect, LEFT, buff=-buff))
    ag.append(shift, name='shift')
    ag.append(lambda: [self.trbl_sides[1].animate.set_opacity(2)], name='close')
    return ag

  def pop(self) -> AnimationGroup:
    e = self.stack.pop()
    ag = AnimationGroup()
    ag.append(
      lambda: [self.trbl_sides[1].animate.set_opacity(0)],
      name='out',
      run_time=0.5,
    )
    ag.append([e.animate.next_to(self.rect, RIGHT)])
    ag.append(
      lambda: [self.trbl_sides[1].animate.set_opacity(1), FadeOut(e)],
      name='close',
      run_time=0.5,
    )
    return ag
