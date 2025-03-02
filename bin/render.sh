#!/bin/bash

echocol() {
  echo -e "\033[0;34m$@\033[0m"
}

#RESOLUTION=720p30
RESOLUTION=480p15
DEST=$(pwd)/slides/media/gen
cd ./slides/animations
for script in *.py; do
    name=$(basename $script .py)
    echocol "Rendering $name..."
    manim -ql -a --hide-splash --progress_bar display --save_sections -v WARNING $script 
    echocol "  Images for $name..."
    (
      cd media/images/$name/
      ls -1 *.png
      cp -f *.png $DEST
    ) 2>/dev/null | sed 's/^/    /'
    echocol "  Videos for $name..."
    (
      cd media/videos/$name/$RESOLUTION/
      ls -1 *.mp4
      cp -f *.mp4 $DEST
    ) 2>/dev/null | sed 's/^/    /'
    # echocol "  Sections for $name..."
    # (
    #   cd media/videos/$name/$RESOLUTION/sections/
    #   ls -1 *.mp4
    #   cp -f *.mp4 $DEST
    # ) 2>/dev/null | sed 's/^/    /'
done
