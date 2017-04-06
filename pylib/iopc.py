import json

PACKAGE_CFG="/Package/CONFIG"

def loadJson2Obj(script):
    with open(script) as fd:
        data = json.load(fd)
    return data

