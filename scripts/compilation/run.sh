#!/bin/bash

version="$1"
runs="$2"
config="$3"
jobs_count="$4"
lang=`echo $LC_ALL`

if [ "$version" == "" ]
then
    echo "Usage: ./run.sh [tar-ball] [number of compiles] [config type] <jobs_count>"
    exit
fi

if [ "$runs" == "" ]
then
    runs="1"
fi

for i in `seq 1 "$runs"`
do
    echo -ne "$i/$runs\t"
    ./make_and_get_errors.sh "$version" "$config" "$jobs_count"
done
