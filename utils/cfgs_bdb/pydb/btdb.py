#!/usr/bin/python -Wall

import bsddb

def set_uint32(db, key, val):
    val_str = "%d" % (val)
    tmp_str = "%6s%04d%s" % ("UINT32", len(val_str), val_str)
    db[key] = tmp_str

def set_boolean(db, key, val):
    val_str = "%d" % (val)
    tmp_str = "%6s%04d%s" % ("_BOOL_", len(val_str), val_str)
    db[key] = tmp_str

'''
def set_boolean_true(db, key):
    tmp_str = "%6s%04d%d" % ("_BOOL_", 1, 1)
    db[key] = tmp_str

def set_boolean_false(db, key):
    tmp_str = "%6s%04d%d" % ("_BOOL_", 1, 0)
    db[key] = tmp_str
'''

def set_string(db, key, val):
    tmp_str = "%6s%04d%s" % ("STRING", len(val), val)
    db[key] = tmp_str

def open(path):
    db = bsddb.btopen(path, 'c')
    return db

def close(db):
    db.close()

def generate_mac(platform_name, idx):
    mac0 = 0
    mac1 = 0
    mac2 = 0
    mac3 = 0
    mac4 = 0
    mac5 = 0

    for ch in platform_name:
        mac3 += ord(ch)
    mac3 %= 255
    mac4 += len(platform_name)
    mac5 += idx

    if platform_name.startswith('raspberry'):
        mac0 = 0xb8
        mac1 = 0x27
        mac2 = 0xeb
    else :
        mac0 += 00
        mac1 += ord(platform_name[0])
        mac2 += ord(platform_name[1])

    tmp_str = "%02x:%02x:%02x:%02x:%02x:%02x" % (mac0, mac1, mac2, mac3, mac4, mac5)
    return tmp_str

'''
if __name__ == "__main__":
    print generate_mac("pandaboard", 0)
    print generate_mac("raspberrypi2", 1)

    db = bsddb.btopen('spam.db', 'c')
    set_uint32(db, "status.mntbase", 2)
    set_uint32(db, "status.netdev", 1)
    db.close()
'''
