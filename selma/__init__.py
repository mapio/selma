from importlib.metadata import version
from logging import getLogger, WARNING
from pathlib import Path

from manim import BLACK, Scene, config

__version__ = version('selma')

FOREGROUND = BLACK
BACKGROUND = '#F0F1EB'

MANIM_WIDTH = 16
MANIM_HEIGHT = 9


def render_all(path, globals):
  Path(path).mkdir(exist_ok=True)
  config.quality = 'medium_quality'
  config.background_color = BACKGROUND
  config.media_dir = path
  getLogger('manim').setLevel(WARNING)
  for obj in globals:
    if isinstance(obj, type) and issubclass(obj, Scene) and obj is not Scene:
      print(obj.__name__)
      obj().render()
