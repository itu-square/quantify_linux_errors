#!/bin/bash
# Will validate a configuration file (.config) by trying to run
# `make olddefconfig`, and see if the .config file has not changed.

# Not a very clean and nice way of validating, and it does not _really_
# Work so well.

# The order of the lines in the .config does not matter
# If there are duplicates, `make olddefconfig` will fix
# the `# CONF... is not set` or `CONF_FOO=BAR` MUST be there

# TODO: must not hardcode stuff in the source code

srcdir="linux-4.0.4" # TODO
#srcdir="busybox-1.23.1"
configdir="/temp/gnf/" 
toyconfig_file="../scripts/gnf/ToyConfig"
#kconfig_file="Config.in"
kconfig_file="Kconfig"
if [ "$1" == "-d" ]
then
    toyexample=true
else
    toyexample=false
fi

export ARCH=x86 # TODO
export SRCARCH=x86 # TODO
export KERNELVERSION=4.0.4 # TODO

rm /temp/1 /temp/2

cd "$srcdir"
rm thesame.txt
if [ $toyexample == true ]
then
    echo "replacing Kconfig with ToyConfig"
    #cp "$kconfig_file" Config.in
    cp "$kconfig_file" Kconfig.orig
    cp "$toyconfig_file" "$kconfig_file"
fi
#for i in `seq 0 9`
for i in `ls "$configdir"`
do
    echo -n "$i "
    cp "$configdir""$i" ./.config
    # Too slow
        #make olddefconfig  2>/dev/null 1>/dev/null 
    # Maybe inaccurate ?
        #./scripts/kconfig/conf --olddefconfig Kconfig  1>> /temp/1 2>> /temp/2
    #make KCONFIG_NOSILENTUPDATE=1 silentoldconfig
    KCONFIG_NOSILENTUPDATE=1 ./scripts/kconfig/conf --silentoldconfig Kconfig
    #./scripts/kconfig/conf -s Config.in &> /dev/null

    #lkdiff .config "$configdir""$i" 
    #./scripts/diffconfig .config "$configdir""$i"
    if [ "$?" == "0" ]
    then
        echo ""
        echo "$i"
        echo "They are the same !!"
        echo ""
        echo "$i" >> thesame.txt
    fi
done

if [ $toyexample == true ]
then
    echo "restoring original Kconfig"
    cp Kconfig.orig "$kconfig_file"
    #cp Config.in.orig "$kconfig_file"
fi
