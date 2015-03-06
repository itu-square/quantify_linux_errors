#!/bin/bash

# Auto configuration
tarfile="$1"
def_or_rnd="$2"
tardir=(${tarfile//.tar*/}) # Takes only the basename.
no_cores=`grep "processor.*:" /proc/cpuinfo|wc|awk '{print $1}'`
no_hz=`grep "model\ name" -m 1 /proc/cpuinfo|awk '{print $NF}'`
no_ram=`grep MemTotal /proc/meminfo|awk '{print $2}'`
no_jobs=`expr "$no_cores" + 1`
rootdir=`pwd`

# Semi configuration
logrootdir="$rootdir/results/$tardir"
buginfofile="buginfo_raw"
timefile="time"
versionfile="program_version"
cpufile="cpu"
ramfile="ram"
conferrfile="conf_errors"

time_format="real %E\ncpuK %S\ncpuU %U\nmaxR %M\noutp %O"

####################################
## Testing if everything is there ##
####################################

if [ "$tarfile" == "" ]
then
    echo "Error: You must specify a tarball to compile"
    exit
fi

if [ -d "$tardir" ]
then
    echo -ne "rm tar\t"
    rm -r "$tardir"
fi

echo -ne "Untar\t"
if [ ! -f "$tarfile" ]
then
    echo "The tar file $tarfile does not exist in this folder. Exiting..."
    exit
fi

###################################
## Making the configuration file ##
###################################

tar xf "$tarfile" 1> /dev/null 2> /dev/null
cd "$tardir"

echo -ne "Conf\t"
make randconfig 2> /tmp/stderr.log 1> /dev/null
configError="$?"

if [ ! $configError == "0" ]
then
    echo "Error making a random configuration. Stopping..."
    echo "The configuration file is $logdir/$tardir/randconfig.conf"
    exit
fi


configmd5=`md5sum .config | awk '{print $1}'`
logdir="$logrootdir/$configmd5"

if [ ! -d "$logdir" ]
then
    mkdir -p "$logdir"
fi

grep "warning" /tmp/stderr.log > "$logdir"/"$conferrfile"
cp ".config" "$logdir"/config

num_conf_errs=`wc "$logdir"/"$conferrfile"|awk '{print $1}'`
echo -en "$num_conf_errs errs\t"

###########################
## Compiling  the source ##
###########################

echo -ne "gcc\t"

analyzer="gcc"
mkdir "$logdir"/"$analyzer"

#/usr/bin/time -o "$logdir"/"$timefile" -f"$time_format" \
    #make -j"$no_jobs" 2> "$logdir"/"$analyzer"/"$buginfofile" 1> /dev/null \
    #/

/usr/bin/time -o "$logdir"/"$timefile" -f"$time_format" make -j"$no_jobs" 2> "$logdir"/"$analyzer"/"$buginfofile" 1> /dev/null

echo "$tardir" > "$logdir"/"$versionfile"
echo "$no_cores"x"$no_hz" > "$logdir"/"$cpufile"
echo "$no_ram" > "$logdir"/"$ramfile"

echo -ne "$configmd5\t"

no_errors=`grep "\^" "$logdir"/"$analyzer"/"$buginfofile"|wc|awk '{print $1}'`
echo -ne "$no_errors errors\t"
echo -ne `grep "real" "$logdir"/"$timefile"`"\n"

