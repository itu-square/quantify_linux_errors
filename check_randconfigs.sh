#!/bin/bash

echo -en "Total\tunset\t=n\t=y\tmod\tsum\tvar\n"
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
find_ratio "CONFIG_SERIAL_TIMBERDALE"
find_ratio "CONFIG_GENERIC_HWEIGHT"
find_ratio "CONFIG_ARCH_HWEIGHT_CFLAGS"
find_ratio "CONFIG_GENERIC_IRQ_LEGACY_ALLOC_HWIRQ"
find_ratio "CONFIG_HAVE_HW_BREAKPOINT"
find_ratio "CONFIG_NET_DSA_HWMON"
find_ratio "CONFIG_MAC80211_MHWMP_DEBUG"
find_ratio "CONFIG_TOUCHSCREEN_TOUCHWIN"
find_ratio "CONFIG_HW_CONSOLE"
find_ratio "CONFIG_VT_HW_CONSOLE_BINDING"
find_ratio "CONFIG_HW_RANDOM"
find_ratio "CONFIG_HW_RANDOM_TIMERIOMEM"
find_ratio "CONFIG_HW_RANDOM_INTEL"
find_ratio "CONFIG_HW_RANDOM_AMD"
find_ratio "CONFIG_HW_RANDOM_GEODE"
find_ratio "CONFIG_HW_RANDOM_VIA"
find_ratio "CONFIG_HW_RANDOM_VIRTIO"
find_ratio "CONFIG_HWMON"
find_ratio "CONFIG_HWMON_VID"
find_ratio "CONFIG_HWMON_DEBUG_CHIP"
find_ratio "CONFIG_SENSORS_IIO_HWMON"
find_ratio "CONFIG_USB_HWA_HCD"
find_ratio "CONFIG_UWB_HWA"
find_ratio "CONFIG_CRYPTO_HW"
