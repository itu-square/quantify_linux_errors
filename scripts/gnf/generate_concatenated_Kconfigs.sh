#!/bin/bash


dir="$1"
script_dir="scripts/gnf/"
output_dir="$script_dir""concatenated_Kconfigs/"

if [ ! -d "$output_dir" ]
then
    mkdir "$output_dir"
fi

for i in `ls "$1""/arch"`
do
    if [ -d "$1""/arch/$i" ]
    then
        python scripts/gnf/generate_concatenated_Kconfigs.py "$dir" "$i" > "$output_dir""$i"
    fi
done
