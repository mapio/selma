#!/bin/bash

RESOLUTION=480p15
for script in ./animations/*.py; do
    name=$(basename $script .py)
    echo "Rendering $name..."
    manim -ql -a --hide-splash --progress_bar display --save_sections -v WARNING --media_dir manim $script 
    (
      cd manim/videos/$name/$RESOLUTION/sections/
      ls -1 *.mp4
    ) | sed 's/^/\t/'
done
