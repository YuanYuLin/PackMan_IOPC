
import json
import sys
import os
from subprocess import call
import struct

def read_from(offset, binfile, read_count):
    fp = open(binfile, "r+b")
    fp.seek(offset)
    data = fp.read(read_count)
    fp.close()
    return data

if __name__ == '__main__':
    offset = 512
    img_path = sys.argv[1]
    gpt_head = read_from(offset, img_path, 16)
    sign, rev, size = struct.unpack("8sII", gpt_head)
    print sign, hex(rev), size

    gpt_head = read_from(offset, img_path, size)

    sign, rev, size, crc32, resv, clba, blba, flba, llba, guid, slba, parts, size_part, crc32_part  = struct.unpack("8sIIIIQQQQ16sQIII", gpt_head)
    print "signature:   " + str(sign)
    print "revision:    " + str(hex(rev))
    print "header size: " + str(size)
    print "crc32:       " + str(crc32)
    print "reserved:    " + str(resv)
    print "Current LBA: " + str(clba)
    print "backup LBA:  " + str(blba)
    print "first LBA:   " + str(flba)
    print "last LBA:    " + str(llba)
    print "GUID:        " + guid
    print "starting LBS:" + str(slba)
    print "Parts:       " + str(parts)
    print "single part size:" + str(size_part)
    print "crc32_part:  " + str(crc32_part)
