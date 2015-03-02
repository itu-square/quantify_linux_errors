#!/bin/bash

version="$1"
runs="$2"

if [ "$version" == "" ]
then
    echo "Usage: ./run.sh [tar-ball] [number of compiles]"
    exit
fi

if [ "$runs" == "" ]
then
    runs="1"
fi

for i in `seq 1 "$runs"`
do
    echo -ne "$i/$runs\t"
    ./make_and_get_errors.sh "$version"
done


