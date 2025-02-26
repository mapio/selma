#!/bin/bash

echocol() {
  echo -e "\033[0;34m$@\033[0m"
}

force=false
if [ $# -gt 0 ]; then
  force=true
fi
(
  cd slides
  for slide in *.ipynb; do
    name=$(basename $slide .ipynb)
    if [ $force = true ]; then
      echocol "Executing ${name}..."
      jupyter nbconvert $slide --to notebook --execute --inplace
    fi
    if [ $slide -nt ../docs/${name}.html ]; then
      echocol "Converting ${name}..."
      jupyter nbconvert $slide --output ${name}.html  --to slides \
        --SlidesExporter.reveal_theme=serif \
        --SlidesExporter.reveal_scroll=True \
        --SlidesExporter.reveal_transition=none \
        --SlidesExporter.exclude_input_prompt=True \
        --SlidesExporter.exclude_output_prompt=True \
        --SlidesExporter.file_extension=.html \
        --TagRemovePreprocessor.remove_input_tags='{"hide"}'
      echocol "Moving to docs/${name}.html..."
      mv -f ${name}.html ../docs/${name}.html
    else
      echocol "Skipping ${name}, is up to date."
    fi
  done
)