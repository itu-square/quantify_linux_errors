#!/bin/bash

folder="$1"
runs="$2"

if [ "$folder" == "" ]
then
    echo "Usage: ./generate_confs.sh [src-dir] [# runs]"
    exit
fi

if [ "$runs" == "" ]
then
    runs="1"
fi

logdir=`pwd`"/randconfig_results/"

if [ ! -d "$logdir" ] 
then
    mkdir -p "$logdir"
fi

cd "$folder"

function randconfigcreate 
{
    echo -en "clean\t"
    make clean 1> /dev/null 2> /dev/null
    echo -en "randconf\t"
    make randconfig 1> /dev/null 2> /dev/null

    md5sum=`md5sum .config | awk '{print $1}'`
    echo -en "$md5sum\n"
    mkdir -p "$logdir$md5sum"
    cp .config "$logdir$md5sum/config"
    
}

for i in `seq 1 "$runs"`
do 
    randconfigcreate
done

