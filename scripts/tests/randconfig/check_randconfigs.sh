#!/bin/bash

# This will check the percentages of the features which are
# in the bottom of this file.
# Good for testing how random a set of configurations are.

dir="./results/randconfig_results"

if [ ! -d "$dir" ]
then
    echo "You should run ./generate_configs first to create some configs..."
    exit
fi


echo -en "Total\tunset\t=n\t=y\tmod\tsum\tvar\n"
function find_ratio
{
    var="$1"
    total=`ls "$dir" | wc | awk '{print $1}'`
    not=`grep "$var is not set" "$dir"/*/config | wc | awk '{print $1}'`
    no=`grep "$var=n" "$dir"/*/config | wc | awk '{print $1}'`
    yes=`grep "$var=y" "$dir"/*/config | wc | awk '{print $1}'`
    mod=`grep "$var=m" "$dir"/*/config | wc | awk '{print $1}'`

    notper=`echo "scale=0;$not*100/$total" | bc -l`
    noper=`echo "scale=0;$no*100/$total" | bc -l`
    yesper=`echo "scale=0;$yes*100/$total" | bc -l`
    modper=`echo "scale=0;$mod*100/$total" | bc -l`
    sumper=`echo "$notper+$noper+$yesper+$modper" | bc -l`
    

    echo -en "$total\t$notper%\t$noper%\t$yesper%\t$modper%\t$sumper%\t$var\n"
}


find_ratio "CONFIG_ELVIS"
find_ratio "CONFIG_FOO"
find_ratio "CONFIG_BAR"
find_ratio "CONFIG_FOOBAR"
find_ratio "CONFIG_BARBAR"
find_ratio "CONFIG_BARFOO"
