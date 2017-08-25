#!/bin/bash

if [ "$#" == "0" ]; then
    echo "emu_arm <kernel> <hda> <hdb> <hdc>"
    exit 1
fi

WORKING_DIR=`dirname $0`
HDA="$WORKING_DIR/hdd/hda"
HDB="$WORKING_DIR/hdd/hdb"
HDC="$WORKING_DIR/hdd/hdc"

QEMU="qemu-system-arm"
MACHINE="-M versatilepb"

KERNEL="-kernel $1"
HDD="-hda $HDA -hdb $HDB -hdc $HDC "
NETDEV="-net nic -net tap,ifname=tap0,script=no,downscript=no"
#NETDEV="-netdev tap,id=tap0"
#GRAPHIC="-nographic"
GRAPHIC="-vnc 0:0"
OPTS="-m 256"
#OPTS=""

$QEMU $MACHINE $KERNEL $HDD $GRAPHIC $OPTS $INITRD $NETDEV #-append console=ttyAMA0,115200
