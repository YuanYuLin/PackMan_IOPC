import json
import sys
import os
from subprocess import call
import struct
import ConfigParser

def execmd(cmd):
    print cmd
    call(cmd)

def help():
    print "gen_image.py <layout.json> <storage device> <output bsp dir> <output rootfs dir"
    print "  ex: gen_image.py layout.json /dev/sdd output/bsp_armel output/rootfs_armel"
    sys.exit(1)

def setLibPath():
    # append library path
    python_lib = os.path.abspath("pylib")
    sys.path.append(python_lib)

    if not os.path.exists(python_lib):
        print "Please download [pylib] from github!!"
        print "git clone https://github.com/YuanYuLin/pylib.git"
        sys.exit(1)

    sys.path.append(python_lib)
    python_lib = os.path.abspath("pyiopc")
    sys.path.append(python_lib)

def head_to_binary(pack):
    data = bytearray('\0' * 64)
    idx = 0
    for ch in bytearray(pack):
        data[idx] = ch
        idx += 1
    return data

def size_to_bytes(size_str):
    val = 0
    if size_str[-1:] == 'B':
        val = int(size_str[0:-1])
    elif size_str[-1:] == '%':
        val = 0xFFFFFFFF
    return val

def create_header(layout_obj):
    header = bytearray('\0' * (64 *1024))
    buffers = []
    version = 1
    table_type = str(layout_obj["table_type"])
    platform = str(layout_obj["platform"])
    platform_id = layout_obj["platform_id"]
    print table_type, platform, platform_id
    pack = struct.pack("12sI20sI12s", "$[IOPCHEAD]$".ljust(12), version, platform.ljust(20), platform_id, table_type.ljust(12))
    buffers.append(head_to_binary(pack))
    for part in layout_obj["parts"]:
        obj = layout_obj[part]
        part_name = str(part)
        boot=obj["boot"]
        fstype = str(obj["fstype"])
        start = size_to_bytes(obj["start"])
        end = size_to_bytes(obj["end"])

        bin_file = obj["bin_files"]
        pack = struct.pack("12s10s10sQQB", "$[IOPCREC]$".ljust(12), part_name.ljust(10), fstype.ljust(10), start, end, boot)
        buffers.append(head_to_binary(pack))

    pack = struct.pack("12sI20sI12s", "$[IOPCEND]$".ljust(12), version, platform.ljust(20), platform_id, table_type.ljust(12))
    buffers.append(head_to_binary(pack))
    idx = 0
    for sec in buffers:
        for ch in sec:
            header[idx]=ch
            idx+=1

    return header

def is_file_exist(binfile, output_dir):
    print os.path.join(output_dir, binfile)
    if os.path.exists(os.path.join(output_dir, binfile)):
        return True
    return False

def read_file(binfile, output_dir):
    data = None
    with open(os.path.join(output_dir, binfile), "rb") as bin_file:
        data = bin_file.read()
    return data

def overwrite_to(offset, src, dst):
    fp = open(dst, "r+b")
    fp.seek(offset)
    fp.write(src)
    fp.close()

def mkfs_and_copy_bins(off_start, storage_dev, bin_files, fstype):
    part_dev = '/dev/loop7'
    mount_dir = '/mnt'
    execmd(['sudo', 'losetup', '-o', str(off_start), part_dev, storage_dev])
    execmd(['sudo', 'mkfs', '-t', fstype, part_dev])
    execmd(['sudo', 'mount', '-t', fstype, part_dev, mount_dir])
    for bin_file in bin_files:
        if is_file_exist(bin_file, bsp_dir):
            execmd(['sudo', 'cp', os.path.join(bsp_dir, bin_file), mount_dir])
        if is_file_exist(bin_file, rootfs_dir):
            execmd(['sudo', 'cp', os.path.join(rootfs_dir, bin_file), mount_dir])

    execmd(['sudo', 'umount', mount_dir])
    execmd(['sudo', 'losetup', '-d', part_dev])

if __name__ == '__main__':
    setLibPath()
    print len(sys.argv)
    if len(sys.argv) < 5:
        help()

    dao_ini = sys.argv[1]
    storage_dev = sys.argv[2]
    bsp_dir     = sys.argv[3]
    rootfs_dir  = sys.argv[4]
    config = ConfigParser.ConfigParser()
    config.read(dao_ini)
    layout = config.get('CFG_IMAGE', 'layout')
    layout_obj  = json.loads(layout)
    table_type = layout_obj["table_type"]

    if table_type == "gpt":
        print "GPT"
    elif table_type == "msdos":
        print "MBR"
    else:
        print "Table type not supported " + table_type
        sys.exit(1)

    execmd(['sudo', 'parted', storage_dev, 'mktable', table_type])

    header_bin = create_header(layout_obj)
    overwrite_to((1024*1024), header_bin, storage_dev)

    part_index = 0
    parts = layout_obj["parts"]
    for part in parts:
        obj = layout_obj[part]
        fstype = obj["fstype"]
        fs_start = obj["start"]
        fs_end = obj["end"]
        fs_boot = obj["boot"]
        bin_files = obj["bin_files"]
        if (fstype == "iopcdao") or (fstype == "iopcdaobk"):
            print "iopcdao"
            off_start = int(fs_start[0:-1], 10)
            off_end = int(fs_end[0:-1],10)
            for bin_file in bin_files:
                bin_data = None
                if is_file_exist(bin_file, bsp_dir):
                    print "in bsp"
                    bin_data = read_file(bin_file, bsp_dir)
                if is_file_exist(bin_file, rootfs_dir):
                    print "in rootfs"
                    bin_data = read_file(bin_file, rootfs_dir)

                if bin_data != None :
                    print off_start, off_end
                    overwrite_to(off_start, bin_data, storage_dev)
        elif fstype == "fat32":
            print "fat32" 
            off_start = int(fs_start[0:-1], 10)
            off_end = int(fs_end[0:-1],10)
            execmd(['sudo', 'parted', storage_dev, 'mkpart', 'primary', 'fat32', fs_start, fs_end])
            mkfs_and_copy_bins(off_start, storage_dev, bin_files, 'vfat')
            part_index += 1
        elif fstype == "ext4":
            print "ext4"
            off_start = int(fs_start[0:-1], 10)
            off_end = int(fs_end[0:-1],10)
            execmd(['sudo', 'parted', storage_dev, 'mkpart', 'primary', 'ext4', fs_start, fs_end])
            mkfs_and_copy_bins(off_start, storage_dev, bin_files, 'ext4')
            part_index += 1
        else:
            print "Fstype not supported " + fstype

        if fs_boot == 1 :
            print "Fsboot " + str(part_index)
            execmd(['sudo', 'parted', storage_dev, 'set', str(part_index), 'boot', 'on'])

    #print layout_obj
    #print storage_dev
    #print dao_bin_file
