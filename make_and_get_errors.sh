#!/bin/bash

tardir="busybox-1.23.1"
tarfile="busybox-1.23.1.tar.bz2"
logroot="results"

if [ -d "$tardir" ]
then
    echo "The tar has already been unpacked. removing... "
    rm -r "$tardir"
fi

echo "Unpacking the tar file..."
if [ ! -f "$tarfile" ]
then
    echo "The tar file $tarfile does not exist in this folder."
    echo "Please go get the busybox code, and place the tar in this folder."
    exit
fi

tar xvf "$tarfile" 1> /dev/null 2> /dev/null
cd "$tardir"

make randconfig 2> /dev/null 1> /dev/null
configError="$?"

if [ ! $configError == "0" ]
then
    echo "Error making a random configuration. Stopping..."
    echo "The configuration file is $logdir/randconfig.conf"
    exit
fi

configmd5=`md5sum .config | awk '{print $1}'`
logdir="../$logroot/$configmd5"

if [ ! -d "$logdir" ]
then
    mkdir -p "$logdir"
fi

cp ".config" "$logdir"/config

echo "Beginning the compiling process"

# -j5 means I am using all 4 cores of my CPU.
# It should be (# of cores + 1) for some reason.
make -j5 2> "$logdir"/buginfo 1> /dev/null
echo "gcc -Wall" > "$logdir"/analyser

echo "Done"
