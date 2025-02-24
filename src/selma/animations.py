from inspect import isfunction
from typing import Callable

DEBUG = False


def islambda(l):
  return isinstance(l, Callable) and l.__name__ == '<lambda>' and isfunction(l)


class AnimationStep:
  def __init__(
    self, name: str = None, animations: list | Callable = None, run_time: float = 1
  ):
    self.name = name
    self._animations = animations
    self.run_time = run_time

  def animations(self):
    if isinstance(self._animations, Callable):
      return self._animations()
    return self._animations

  def __repr__(self):
    return f'{self.name=} {self._animations=} {self.run_time=}'


class AnimationGroup:
  def __init__(self):
    self.steps = []

  def append(self, animations: list | Callable, name: str = None, run_time: float = 1):
    self.steps.append(
      AnimationStep(name=name, animations=animations, run_time=run_time)
    )

  def play(self, scene):
    for step in self.steps:
      if DEBUG and step.name:
        print(step.name)
      scene.play(*step.animations(), run_time=step.run_time)

  def __repr__(self):
    return f'{self.steps=}'


# class AnimationStep:
#   pass

# class PlayStep(AnimationStep):
#   def __init__(self, *animations : list, run_time: float = 1):
#     self.run_time = run_time
#     self.animations = animations
#   def merge(self, other: 'PlayStep'):
#     self.animations += other.animations
#     self.run_time = max(self.run_time, other.run_time)

# class AddStep(AnimationStep):
#   def __init__(self, *mobjects : list):
#     self.mobjects = mobjects

# class WaitStep(AnimationStep):
#   def __init__(self, wait_time: float):
#     self.wait_time = wait_time
