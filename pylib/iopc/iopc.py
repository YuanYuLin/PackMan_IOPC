
PACKAGE_CFG="/Package/CONFIG"
def getAccount(obj):
    return obj["account"]

def setAccount(obj, val):
    obj["account"] = val

def getCfg(obj):
    return obj["cfg"]

def setCfg(obj, val):
    obj["cfg"] = val

def getParams(obj):
    return obj["params"]

def setParams(obj, val):
    obj["params"] = val

def isSinglePackage(obj):
    params_len = len(obj["params"])
    if params_len >= 2:
        params = obj["params"]
        return True
    return False

def getSinglePackageName(obj):
    params_len = len(obj["params"])
    if params_len >= 2:
        params = obj["params"]
        return params[1]
    return ""

