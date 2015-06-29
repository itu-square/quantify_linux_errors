#!/bin/bash

# Configuration
# THIS SHOULD ONLY BE SET IF NECESSARY
# By that I mean if the `gcc` version of gcc is below 4.9
gcc='gcc-4.9'

if [ "$1" == "" ]
then
    echo "Missing argument"
    echo "Usage: ./run.sh <linux src dir> [# of runs]"
    exit
fi

if [ "$2" == "" ]
then
    echo "No second argument (which sets the number of runs.)"
    echo "Just running it once, then..."
    runs=1
else
    runs="$2"
fi 

#alias gcc=gcc-4.9
#python scripts/compilation/make_mrproper.py "$1"

# Logging to timer file.
oldtime=`date +%s`
echo "### Running $runs times on $1" >> run.log
echo "0/$runs $time" >> run.log

# Running mrproper, and maybe changing the name of gcc. This is probably only
# necessary on this server, since the native gcc is version 4.6 or some old
# junk.
#python scripts/compilation/make_mrproper.py "$1" "gcc-4.9"
python scripts/compilation/make_mrproper.py "$1"

for i in `seq 1 "$runs"`
do
    echo "$i/$runs"
    python scripts/compilation/make_config.py "$1"
    python scripts/compilation/make.py "$1" "$gcc"
    #python scripts/categorization/categorize_errors.py "$1"
    #python scripts/submission/upload_results.py "$1"
    #python scripts/submission/backup_results.py "$1"
    newtime=`date +%s`
    diftime=`echo "$newtime - $oldtime" | bc -q`
    oldtime="$newtime"
    echo "$i/$runs $diftime" >> run.log
done
