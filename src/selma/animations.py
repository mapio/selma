from typing import Callable

DEBUG = False


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
