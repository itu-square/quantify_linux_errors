#!/bin/bash

# Auto configuration
tarfile="$1"
def_or_rnd="$2"
job_count="$3"
tardir=(${tarfile//.tar*/}) # Takes only the basename.
no_cores=`grep "processor.*:" /proc/cpuinfo|wc|awk '{print $1}'`
no_hz=`grep "model\ name" -m 1 /proc/cpuinfo|awk '{print $NF}'`
no_ram=`grep MemTotal /proc/meminfo|awk '{print $2}'`
rootdir=`pwd`

# Semi configuration
logrootdir="$rootdir/results/$tardir"
buginfofile="stderr_raw"
stdoutfile="stdout_raw"
timefile="time"
versionfile="program_version"
cpufile="cpu"
ramfile="ram"
conferrfile="conf_errors"
exitstatusfile="exit_status"
all=`echo "$LC_ALL"`
ctype=`echo "$LC_CTYPE"`
messages=`echo "$LC_MESSAGES"`
lang=`echo "$LANG"`
export LC_ALL=""
export LC_CTYPE=""
export LC_MESSAGES=""
export LANG=""
time_format="real %E\ncpuK %S\ncpuU %U\nmaxR %M\noutp %O\ncomm %C"

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

if [ "$3" == "" ]
then
    no_jobs=`expr "$no_cores" + 1`
else
    no_jobs="$3"
fi

###################################
## Making the configuration file ##
###################################

tar xfJ "$tarfile" 1> /dev/null 2> /dev/null
cd "$tardir"

# Ensures that the kernel tree is absolutely clean.
make mrproper

echo -ne "Conf\t"

if [ "$2" == "randconfig" ]
then
    make randconfig 2> /tmp/stderr.log 1> /dev/null
elif [ "$2" == "tinyconfig" ]
then
    make tinyconfig 2> /tmp/stderr.log 1> /dev/null
elif [ "$2" == "defconfig" ]
then
    make defconfig 2> /tmp/stderr.log 1> /dev/null
elif [ "$2" == "allnoconfig" ]
then
    make defconfig 2> /tmp/stderr.log 1> /dev/null
elif [ "$2" == "allyesconfig" ]
then
    make defconfig 2> /tmp/stderr.log 1> /dev/null
else
    echo "The 2nd argument is not understood. It should be the config"
    echo "type. Exiting"
    exit
fi
    
configError="$?"

if [ ! $configError == "0" ]
then
    echo "Error making a random configuration. Stopping..."
    echo "The configuration file is $logdir/$tardir/randconfig.conf"
    exit
fi


sorted_config=`grep -v "^#" .config | grep -v "^$" | sort`
configmd5=`echo "$sorted_config"  | md5sum | awk '{print $1}'`
logdir="$logrootdir/$configmd5"

if [ ! -d "$logdir" ]
then
    mkdir -p "$logdir"
fi

grep "warning" /tmp/stderr.log > "$logdir"/"$conferrfile"
cp ".config" "$logdir"/config
echo "$sorted_config" > "$logdir"/config_sorted

num_conf_errs=`wc "$logdir"/"$conferrfile"|awk '{print $1}'`
echo -en "$num_conf_errs wrns\t"

###########################
## Compiling  the source ##
###########################

echo -ne "gcc\t"

analyzer_version=`gcc -dumpversion`
analyzer="gcc"
mkdir "$logdir"/"$analyzer"
echo "$analyzer_version" > "$logdir"/"$analyzer"/version

#/usr/bin/time -o "$logdir"/"$timefile" -f"$time_format" \
    #make -j"$no_jobs" 2> "$logdir"/"$analyzer"/"$buginfofile" 1> /dev/null \
    #/

/usr/bin/time -o "$logdir"/"$timefile" -f"$time_format" make -k -j"$no_jobs" 2> "$logdir"/"$analyzer"/"$buginfofile" 1> "$logdir"/"$analyzer"/"$stdoutfile"
exitstatus="$?"

echo "$tardir" > "$logdir"/"$versionfile"
echo "$no_cores"x"$no_hz" > "$logdir"/"$cpufile"
echo "$no_ram" > "$logdir"/"$ramfile"
echo "$exitstatus" > "$logdir"/"$exitstatusfile"

echo -ne "$configmd5\t"

no_errors=`grep "\^" "$logdir"/"$analyzer"/"$buginfofile"|wc|awk '{print $1}'`
echo -ne "$no_errors wrns\t"
echo -ne `grep "real" "$logdir"/"$timefile"`"\n"

export LC_ALL="$all"
export LC_CTYPE="$ctype"
export LC_MESSAGES="$messages"
export LANG="$lang"
