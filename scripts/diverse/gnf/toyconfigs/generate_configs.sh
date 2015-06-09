#!/bin/bash

count=100
for i in `seq 1 "$count"`
do
    echo "config $i"
    echo "    bool 'text'"
    rnd=`echo "$RANDOM % 10" | bc`
    if [ "$rnd" -lt "8" ]
    then
        #TODO HERE
        echo "    depends on '
    fi
done
