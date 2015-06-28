#!/bin/bash

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
echo "### Running $runs times on $1" >> run.log
echo "### `date +%s`" >> run.log

# Running mrproper, and maybe changing the name of gcc. This is probably only
# necessary on this server, since the native gcc is version 4.6 or some old
# junk.
#python scripts/compilation/make_mrproper.py "$1" "gcc-4.9"
python scripts/compilation/make_mrproper.py "$1"

for i in `seq 1 "$runs"`
do
    echo "$i/$runs"
    #python scripts/compilation/make_config.py "$1"
    python scripts/compilation/make.py "$1"
    python scripts/categorization/categorize_errors.py "$1"
    #python scripts/submission/upload_results.py "$1"
    python scripts/submission/backup_results.py "$1"
    echo "$i/$runs `date +%s`" >> run.log
done
