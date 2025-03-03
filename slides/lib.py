import glob
import warnings

from IPython.display import HTML, Markdown, display

from selma import BACKGROUND

BASENAME = './media/gen'


def search_file(prefix, ext):
  files = glob.glob(f'{BASENAME}/{prefix}*.{ext}')
  if len(files) == 0:
    raise FileNotFoundError(f"No match found for '{prefix}*.{ext}'")
  elif len(files) > 1:
    warnings.warn(f"Multiple files matched '{prefix}*.{ext}', returning the first one")
  return files[0]


def md(text):
  display(Markdown(text))


def img(name, title=None, width='800px', height='450px'):
  if title:
    md(f'## {title}')
  path = search_file(name, 'png')
  display(
    # ruff: noqa: E501
    HTML(f"""<div style="display: flex; justify-content: center; align-items: center; margin: 0; padding: 0; background-color: {BACKGROUND};">
<img src="{path}" style="width: {width}; height: {height};" alt="Image not found">
</div>""")
  )


def anim(name, title=None, width='800px', height='450px'):
  if title:
    md(f'## {title}')
  path = search_file(name, 'mp4')
  display(
    # ruff: noqa: E501
    HTML(f"""<div style="display: flex; justify-content: center; align-items: center; margin: 0; padding: 0; background-color: {BACKGROUND};">
<video style="width: {width}; height: {height};" controls <source src="{path}" type="video/mp4">IL tuo browser non supporta i video.</video>
</div>""")
  )
