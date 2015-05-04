#!/bin/bash
# Will validate a configuration file (.config) by trying to run
# `make olddefconfig`, and see if the .config file has not changed.

# Not a very clean and nice way of validating, and it does not _really_
# work. In the sense, that if the file is permuted (lines are randomized) or
# even alphabetized, it will not output the same .config.
# So they should be in some order, that Kconfig tells us, I guess.

srcdir="linux-3.19"
configdir="/temp/gnf/"
export ARCH=x86
export SRCARCH=x86
export KERNELVERSION=3.19.0

cd "$srcdir"
#for i in `ls "$configdir"`
for i in `seq 0 9`
do
    echo -n "$i "
    cp "$configdir""$i" ./.config
    #make olddefconfig  2>/dev/null 1>/dev/null
    ./scripts/kconfig/conf --olddefconfig Kconfig  1>/dev/null 2>/dev/null
    lkdiff .config "$configdir""$i"  2>/dev/null 1>/dev/null
    if [ "$?" == "0" ]
    then
        echo ""
        echo "$i"
        echo "They are the same !!"
        echo ""
        echo "$i" >> thesame.txt
    fi
done
