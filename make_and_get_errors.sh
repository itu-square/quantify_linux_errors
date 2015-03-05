#!/bin/bash

# Auto configuration
tarfile="$1"
tardir=(${tarfile//.tar*/}) # Takes only the basename.
no_cores=`grep "processor.*:" /proc/cpuinfo|wc|awk '{print $1}'`
no_cores=`expr "$no_cores" + 1`

# Semi configuration
logrootdir="results"
buginfofile="buginfo_raw"
timefile="time"
versionfile="program_version"

time_format="real %E\ncpuK %S\ncpuU %U\n\nmaxR %M\navgR %t\navgS %K\npage %Z"
time_format="$time_format""\n\ninp  %I\noutp %O\nrecM %r\nsenM %s\nsign %k\n"
time_format="$time_format""comm %C"


## Testing if everything is there

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

## Beginning the process

tar xf "$tarfile" 1> /dev/null 2> /dev/null
cd "$tardir"

echo -ne "Conf\t"
make randconfig 2> /dev/null 1> /dev/null
configError="$?"

if [ ! $configError == "0" ]
then
    echo "Error making a random configuration. Stopping..."
    echo "The configuration file is $logdir/randconfig.conf"
    exit
fi

configmd5=`md5sum .config | awk '{print $1}'`
logdir="../$logrootdir/$configmd5"

if [ ! -d "$logdir" ]
then
    mkdir -p "$logdir"
fi

cp ".config" "$logdir"/config

echo -ne "gcc\t"

analyzer="gcc"
mkdir "$logdir"/"$analyzer"

#/usr/bin/time -o "$logdir"/"$timefile" -f"$time_format" \
    #make -j"$no_cores" 2> "$logdir"/"$analyzer"/"$buginfofile" 1> /dev/null \
    #/

/usr/bin/time -o "$logdir"/"$timefile" -f"$time_format" make -j"$no_cores" 2> "$logdir"/"$analyzer"/"$buginfofile" 1> /dev/null

echo "$tardir" > "$logdir"/"$versionfile"

echo -ne "$configmd5\t"

no_errors=`grep "\^" "$logdir"/"$analyzer"/"$buginfofile"|wc|awk '{print $1}'`
echo -ne "$no_errors errors\t"
echo -ne `grep "real" "$logdir"/"$timefile"`"\n"

