#!/bin/bash

folder="$1"
runs="$2"
cwd=`pwd`"/"

if [ "$folder" == "" ]
then
    echo "Usage: ./generate_confs.sh [src-dir] [# runs]"
    exit
fi

if [ "$runs" == "" ]
then
    runs="1"
fi

logdir="$cwd/results/randconfig_results/"

if [ ! -d "$logdir" ] 
then
    mkdir -p "$logdir"
fi

# Entering folder
cd "$cwd$folder"

function randconfigcreate 
{
    #echo -en "clean\t"
    #make clean 1> /dev/null 2> /dev/null
    echo -en "randconf\t"
    make V=1 randconfig 1> /tmp/1.log  2> /tmp/2.log

    md5sum=`grep -v "^#" .config | grep -v "^$" | md5sum | awk '{print $1}'`
    echo -en "$md5sum\n"
    mkdir -p "$logdir$md5sum"
    cp .config "$logdir$md5sum/config"
    cp /tmp/1.log "$logdir$md5sum/stdout.log"
    cp /tmp/2.log "$logdir$md5sum/stderr.log"
    
}

for i in `seq 1 "$runs"`
do 
    randconfigcreate
done

