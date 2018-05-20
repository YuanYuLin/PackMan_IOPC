#!/bin/bash

if [ "$#" == "0" ]; then
    echo "emu_arm <index> <output bsp folder> <output rootfs folder>"
    echo "  usage: emu_xxx 0 /output/bsp_vpb /outpu/rootfs_mini"
    exit 1
fi

EMU_INDEX="$1"
OUTPUT_BSP_DIR="$2"
OUTPUT_ROOTFS_DIR="$3"

case "$EMU_INDEX" in
"0")
	NETWORK_TAP="tap0"
	NET_NUM="1"
	VNC_NUM="20"
;;
"1")
	NETWROK_TAP="tap1"
	NET_NUM="2"
	VNC_NUM="21"
;;
*)
	echo "error index ..."
	exit 1
;;
esac

LINUX_IMAGE="$OUTPUT_BSP_DIR/arch_arm/linux_image"
DTB_IMAGE="/data/PackMan_IOPC/packages/buildroot/buildroot-2017.02.3/output/images/versatile-pb.dtb"

HDA="$OUTPUT_BSP_DIR/arch_arm/qemu/hda.img"
HDB="$OUTPUT_BSP_DIR/arch_arm/qemu/hdb.img"
HDC="$OUTPUT_BSP_DIR/arch_arm/qemu/hdc.img"
HDD="$OUTPUT_BSP_DIR/arch_arm/qemu/hdd.img"

QEMU="qemu-system-arm"
MACHINE="-M versatilepb"

KERNEL="-kernel $LINUX_IMAGE"
#DTB="-dtb $DTB_IMAGE"
DTB=""
HDD="-hda $HDA -hdb $HDB -hdc $HDC -hdd $HDD"
#NETDEV="-net nic -net tap,ifname=$NETWORK_TAP,script=no,downscript=no"
NETDEV="-net nic,macaddr=52:54:01:23:45:0$NET_NUM -net tap,ifname=tap$NET_NUM,script=no,downscript=no"
#NETDEV="-net nic -net tap,id=net$NET_NUM,ifname=br0net$NET_NUM,script=no"
#NETDEV="-netdev tap,id=tap0"
GRAPHIC="-nographic -vnc :$VNC_NUM -vga std"
OPTS="-m 128"
#OPTS=""

BOOT_PARAMS="BOOT_DELAY=1 BOOT_DEV=/dev/sda BOOT_DEV_PART=1 BOOT_ROOTFS=rootfs.squashfs"

echo $QEMU $MACHINE $KERNEL $HDD $GRAPHIC $OPTS $INITRD $NETDEV -append "console=ttyAMA0,115200 init=/bin/sh $BOOT_PARAMS"
$QEMU $MACHINE $KERNEL $DTB $HDD $GRAPHIC $OPTS $INITRD $NETDEV -append "console=ttyAMA0,115200 init=/bin/sh $BOOT_PARAMS"
