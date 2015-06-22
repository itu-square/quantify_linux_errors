#!/bin/bash

git clone https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
comm=`git --git-dir=linux-next/.git rev-parse origin`

mv linux-next "linux-next-$comm"
