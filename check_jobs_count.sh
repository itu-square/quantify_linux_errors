#!/bin/bash
# This file will run a number of compilations with different number
# of jobs. You can then see which one is the fastest.

for i in `seq 1 15`
do
    ./run.sh linux-4.0-rc4.tar.xz 1 tinyconfig "$i"
done
