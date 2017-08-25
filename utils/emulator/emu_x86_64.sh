#!/bin/bash

if [ "$#" == "0" ]; then
    echo "emu_arm <kernel> <hda> <hdb> <hdc>"
    exit 1
fi

WORKING_DIR=`dirname $0`
HDA="$WORKING_DIR/hdd/hda"
HDB="$WORKING_DIR/hdd/hdb"
HDC="$WORKING_DIR/hdd/hdc"

QEMU="qemu-system-x86_64"
MACHINE="-M q35"

KERNEL="-kernel $1"
#HDD="-hda $HDA -hdb $HDB -hdc $HDC "
HDD="-drive file=$HDA -drive file=$HDB -drive file=$HDC "
NETDEV="-net nic -net tap,ifname=tap0,script=no,downscript=no"
#NETDEV="-netdev tap,id=tap0"
#GRAPHIC="-nographic"
GRAPHIC="-vnc 0:0"
OPTS="-cpu core2duo -m 2048"

$QEMU $MACHINE $KERNEL $HDD $GRAPHIC $OPTS $INITRD $NETDEV -append "BOOT_DEV=/dev/sda1 BOOT_ROOTFS=rootfs.squashfs.x86_64 BOOT_DELAY=1 init=/init console=tty"
#kvm $MACHINE $KERNEL $HDD $GRAPHIC $OPTS $INITRD $NETDEV $APPEND
