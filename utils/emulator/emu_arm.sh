#!/bin/bash

if [ "$#" == "0" ]; then
    echo "emu_arm <kernel> <rootfs> <hda> <hdb> <hdc> <hdd>"
    exit 1
fi

LINUX_IMAGE="$1"
ROOTFS_IMAGE="$2"
HDA="$3"
HDB="$4"
HDC="$5"
HDD="$6"

IMAGE_HDA="$HDA"
IMAGE_MNT="/tmp/mnt"
IMAGE_LOOP="/dev/loop7"
OFFSET=`fdisk $IMAGE_HDA -l | grep "hda.img1" | awk '{ print  $3 }'`

echo "OFFSET=$OFFSET"
echo "losetup -o $(($OFFSET*512)) $IMAGE_LOOP $IMAGE_HDA "
losetup -o $(($OFFSET*512)) $IMAGE_LOOP $IMAGE_HDA 
mkfs -t vfat $IMAGE_LOOP
mkdir $IMAGE_MNT
mount $IMAGE_LOOP $IMAGE_MNT

cp $LINUX_IMAGE $IMAGE_MNT
cp $ROOTFS_IMAGE $IMAGE_MNT

umount $IMAGE_MNT
losetup -d $IMAGE_LOOP

WORKING_DIR=`dirname $0`
#HDA="$WORKING_DIR/hdd/hda"
#HDB="$WORKING_DIR/hdd/hdb"
#HDC="$WORKING_DIR/hdd/hdc"

QEMU="qemu-system-arm"
MACHINE="-M versatilepb"

KERNEL="-kernel $LINUX_IMAGE"
HDD="-hda $HDA -hdb $HDB -hdc $HDC -hdd $HDD"
NETDEV="-net nic -net tap,ifname=tap0,script=no,downscript=no"
#NETDEV="-netdev tap,id=tap0"
GRAPHIC="-vnc 0:0"
OPTS="-m 256"
#OPTS=""

BOOT_PARAMS="BOOT_DELAY=1 BOOT_DEV=/dev/sda1 BOOT_ROOTFS=rootfs.squashfs"

$QEMU $MACHINE $KERNEL $HDD $GRAPHIC $OPTS $INITRD $NETDEV -nographic -append "console=ttyAMA0,115200 init=/bin/sh $BOOT_PARAMS"
