#!/bin/bash


dir="$1"
cd "$dir"
mkdir allnoconfigs

for i in `ls arch`
do
    if [ -d "arch/$i" ]
    then
        make ARCH="$i" allnoconfig
        cp .config allnoconfigs/"$i"_allnoconfig
    fi
done
