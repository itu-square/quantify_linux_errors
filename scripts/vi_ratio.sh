#!/bin/bash

srcdir="linux-3.19"
configdir="/tmp/gnf/"
export ARCH=x86
export SRCARCH=x86
export KERNELVERSION=3.19.0

cd "$srcdir"
#for i in `ls "$configdir"`
for i in `seq 0 9999`
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
