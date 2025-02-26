#!/bin/bash

#RESOLUTION=720p30
RESOLUTION=480p15
cd ./slides/animations
for script in *.py; do
    name=$(basename $script .py)
    echo "Rendering $name..."
    manim -ql -a --hide-splash --progress_bar display --save_sections -v WARNING $script 
    (
      cd media/videos/$name/$RESOLUTION/sections/
      ls -1 *.mp4
    ) | sed 's/^/\t/'
done
