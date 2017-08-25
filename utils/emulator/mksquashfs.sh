#!/bin/bash
WORKDIR=/home/yyl/data/embuilder/emulator
MKSQUASHFS="/home/yyl/data/embuilder/buildsystem/buildroot/VPB_ROOTFS/host/usr/bin/mksquashfs"
SRC_ROOTFS="$WORKDIR/lxc-debian-rootfs/rootfs"
DST_ROOTFS="$WORKDIR/debian_jessie.squashfs"
ROOTFS_OPTS="-noappend -comp gzip"

$MKSQUASHFS $SRC_ROOTFS $DST_ROOTFS $ROOTFS_OPTS
