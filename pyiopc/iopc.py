import ops
import os
PACKAGE_CFG="/Package/CONFIG"

def getAccount(obj):
    return obj["account"]

def setAccount(obj, val):
    obj["account"] = val

def getCfg(obj):
    return obj["cfg"]

def setCfg(obj, val):
    obj["cfg"] = val

def getOutputDir(obj):
    return obj["output_dir"]

def setOutputDir(obj, val):
    obj["output_dir"] = val

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

def getTargetRootfs():
    full_path = ops.getEnv("ARCH_ROOTFS")
    return full_path

def getBinPkgPath():
    full_path = ops.getEnv("PACKAGES_DIR")
    return full_path

def getBaseRootFile(file_path):
    base_rootfs_dir = ops.getEnv("BASE_ROOTFS_DIR")
    return base_rootfs_dir + file_path

def getSdkInclude():
    sdkstage = ops.getEnv("SDKSTAGE")
    dst_includes = sdkstage + "/usr/include"
    return dst_includes

def getSdkLib():
    sdkstage = ops.getEnv("SDKSTAGE")
    dst_lib = sdkstage + "/usr/lib"
    return dst_lib

def getSdkPkgConfig():
    sdkstage = ops.getEnv("SDKSTAGE")
    dst_pc = sdkstage + "/pkgconfig/"
    return dst_pc

def make(workspace):
    CMD=['make']
    res = ops.execCmd(CMD, workspace, False, None)
    if res[2] != 0:
        print res[1]

def extractSrc(pkg_path, output_path):
    print pkg_path
    for obj in os.listdir(pkg_path):
        full_path = os.path.join(pkg_path, obj)
        if obj in ["Package", ".git", "LICENSE", ".gitignore"]:
            print "{" + obj + "} skip"
            continue
        ops.copyto(full_path, output_path)

def installBin(pkg_name, bin_obj, dst):
    bin_pkg_path = os.path.join(ops.getEnv("PACKAGES_DIR"), pkg_name)
    full_dst = bin_pkg_path + dst
    ops.mkdir(full_dst)
    ops.copyto(bin_obj, full_dst)

def installPkg(pkg_path):
    target_rootfs = ops.getEnv("ARCH_ROOTFS")
    for obj in os.listdir(pkg_path):
        full_path = ops.path_join(pkg_path, obj)
        if obj in ["Package", ".git", "LICENSE", ".gitignore"]:
            continue
        ops.copyto(full_path, target_rootfs)

def genPkgFiles(pkg_config_path):
    fp = open(ops.path_join(pkg_config_path, "CONFIG.py"), "w+")
    fp.writelines("import ops" + os.linesep)
    fp.writelines("import iopc" + os.linesep)
    fp.writelines("def MAIN_ENV(args):" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.writelines("def MAIN_EXTRACT(args):" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.writelines("def MAIN_CONFIGURE(args):" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.writelines("def MAIN_BUILD(args):" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.writelines("def MAIN_INSTALL(args):" + os.linesep)
    fp.writelines("  iopc.installPkg(arg['pkg_path'])" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.writelines("def MAIN_CLEAN_BUILD(args):" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.close()

def packPkg(pkg_name):
    bin_pkg_path = os.path.join(ops.getEnv("PACKAGES_DIR"), pkg_name)
    pkg_config_path = ops.path_join(bin_pkg_path, "Package")
    ops.mkdir(pkg_config_path)
    genPkgFiles(pkg_config_path)

