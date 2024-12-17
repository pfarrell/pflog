#!/usr/bin/env bash

for src in ../*.jpg ../*.jpeg ../*.JPG ../*.JPEG; do
    if [ -f "$src" ]; then
        cropped=$(echo $src | sed -e 's/\.\.\///');
        if [ ! -f $cropped ]; then
            smartcroppy --width 295 --height 177 $src $cropped;
        fi;
    fi;
done

