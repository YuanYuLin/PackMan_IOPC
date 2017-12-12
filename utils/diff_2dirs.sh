#!/bin/bash

if [ $# -lt 2 ]; then
    echo "diff2dir.sh <dir1> <dir2>"
fi
DIR1=$1
DIR2=$2
diff -bur $DIR1 $DIR2 | grep 'diff -bur' | awk '{ print "vimdiff " $3 " " $4 }'
diff -bur $DIR1 $DIR2 | grep 'Only in '
