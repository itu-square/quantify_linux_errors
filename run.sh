#!/bin/bash

# Configuration
gcc='gcc-4.9' # Dont think about it if you are not on mtlab.itu.dk
servername="mtlab" # Dont think about it if you are not on mtlab.itu.dk

# Autoconfiguration
hostname=`hostname`
gittag="next-$olddate"
olddate=`date --date '90 days ago' +%Y%m%d`


# Checking for arguments
if [ "$1" == "" ]
then
    echo "Missing arguments"
    echo "Usage: ./run.sh <new linux src dir> <old linux src dir> [# of runs]"
    exit
fi

if [ "$2" == "" ]
then
    echo "Missing arguments"
    echo "Usage: ./run.sh <new linux src dir> <old linux src dir> [# of runs]"
    exit
fi

if [ "$3" == "" ]
then
    echo "No second argument (which sets the number of runs.)"
    echo "Just running it once, then..."
    runs=1
else
    runs="$3"
fi 



# Replace `gcc with gcc-4.9` if on mtlab server.
# This is kinda hacky, I know. But works, so hey.
if [ "$hostname" == "mtlab" ]
then
    sed -i 's/= gcc$/= gcc-4.9/' "$1"/Makefile
    sed -i 's/= gcc$/= gcc-4.9/' "$2"/Makefile
    sed -i 's/)gcc$/)gcc-4.9/' "$1"/Makefile
    sed -i 's/)gcc$/)gcc-4.9/' "$2"/Makefile
fi


# Logging to timer file.
oldtime=`date +%s`
echo "### Running $runs times on $1" >> run.log
echo "0/$runs $time" >> run.log

# Running mrproper, and maybe changing the name of gcc. This is probably only
# necessary on this server, since the native gcc is version 4.6 or some old
# junk.
#python scripts/compilation/make_mrproper.py "$1" "gcc-4.9"

### RUNNING ON THE FIRST VERSION
python scripts/compilation/make_mrproper.py "$1"
python scripts/compilation/make_mrproper.py "$2"

for i in `seq 1 "$runs"`
do
    echo "$i/$runs"
    python scripts/compilation/make_config.py "$1"
    python scripts/compilation/make.py "$1" "$gcc"
    python scripts/categorization/categorize_errors.py "$1"
    python scripts/submission/upload_results.py "$1"
    python scripts/submission/backup_results.py "$1"
    newtime=`date +%s`
    diftime=`echo "$newtime - $oldtime" | bc -q`
    oldtime="$newtime"
    echo "$i/$runs $diftime \t $1" >> run.log

    # Copying the .config file over to the other version

    cp "$1/config" "$2/config"

    echo "$i/$runs"
    #python scripts/compilation/make_config.py "$2"
    python scripts/compilation/make_olddef.py "$2"
    python scripts/compilation/make.py "$2" "$gcc"
    python scripts/categorization/categorize_errors.py "$2"
    python scripts/submission/upload_results.py "$2"
    python scripts/submission/backup_results.py "$2"
    newtime=`date +%s`
    diftime=`echo "$newtime - $oldtime" | bc -q`
    oldtime="$newtime"
    echo "$i/$runs $diftime \t $1" >> run.log
done
