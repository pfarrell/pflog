#!/usr/bin/env bash

for src in ../*.jpg ../*.jpeg;
  do
    cropped=$(echo $src | sed -e 's/\.\.\///');
    if [ ! -f $cropped ]; then
      smartcrop -W 295 -H 177 -i $src -o $cropped;
    fi;
  done
