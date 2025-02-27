#!/bin/bash

echocol() {
  echo -e "\033[0;34m$@\033[0m"
}

#RESOLUTION=720p30
RESOLUTION=480p15
cd ./slides/animations
for script in *.py; do
    name=$(basename $script .py)
    echocol "Rendering $name..."
    manim -ql -a --hide-splash --progress_bar display --save_sections -v WARNING $script 
    echocol "Images for $name..."
    (
      cd media/images/$name/
      ls -1 *.png
    ) | sed 's/^/  /'
    echocol "Videos for $name..."
    (
      cd media/videos/$name/$RESOLUTION/
      ls -1 *.mp4
    ) | sed 's/^/  /'
    echocol "Sections for $name..."
    (
      cd media/videos/$name/$RESOLUTION/sections/
      ls -1 *.mp4
    ) | sed 's/^/  /'
done
