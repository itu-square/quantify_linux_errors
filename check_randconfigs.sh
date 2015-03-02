#!/bin/bash

echo -en "Total\tnot set\t=n\t=y\tmod\tsum\tvar\n"
function find_ratio
{
    var="$1"
    total=`ls randconfig_results | wc | awk '{print $1}'`
    not=`grep "$var is not set" randconfig_results/*/config | wc | awk '{print $1}'`
    no=`grep "$var=n" randconfig_results/*/config | wc | awk '{print $1}'`
    yes=`grep "$var=y" randconfig_results/*/config | wc | awk '{print $1}'`
    mod=`grep "$var=m" randconfig_results/*/config | wc | awk '{print $1}'`

    notper=`echo "scale=0;$not*100/$total" | bc -l`
    noper=`echo "scale=0;$no*100/$total" | bc -l`
    yesper=`echo "scale=0;$yes*100/$total" | bc -l`
    modper=`echo "scale=0;$mod*100/$total" | bc -l`
    sumper=`echo "$notper+$noper+$yesper+$modper" | bc -l`
    

    echo -en "$total\t$notper%\t$noper%\t$yesper%\t$modper%\t$sumper%\t$var\n"
}


find_ratio "CONFIG_64BIT"
find_ratio "CONFIG_GENERIC_CLOCKEVENTS"
find_ratio "CONFIG_GENERIC_IRQ_PROBE"
find_ratio "CONFIG_INSTRUCTION_DECODER"
find_ratio "CONFIG_GENERIC_HWEIGHT"
find_ratio "CONFIG_FONT_8x16"
find_ratio "CONFIG_SERIAL_TIMBERDALE"
