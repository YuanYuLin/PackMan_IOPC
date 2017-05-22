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

def getBinPkgRootPath():
    full_path = ops.getEnv("PACKAGES_DIR")
    return full_path

def getBaseRootFile(file_path):
    base_rootfs_dir = ops.getEnv("BASE_ROOTFS_DIR")
    return base_rootfs_dir + file_path

def getBinPkgPath(pkg_name):
    bin_pkg_path = ops.path_join(getBinPkgRootPath(), pkg_name)
    return bin_pkg_path

def getSdkPath():
    sdkstage = ops.getEnv("SDKSTAGE")
    return sdkstage

def getSdkInclude():
    sdkstage = ops.getEnv("SDKSTAGE")
    dst_includes = sdkstage + "/usr/include"
    ops.mkdir(dst_includes)
    return dst_includes

def getSdkLib():
    sdkstage = ops.getEnv("SDKSTAGE")
    dst_lib = sdkstage + "/usr/lib"
    return dst_lib

def getSdkPkgConfig():
    sdkstage = ops.getEnv("SDKSTAGE")
    dst_pc = sdkstage + "/pkgconfig/"
    return dst_pc

def make(workspace, extrac_config=None):
    CMD=['make']
    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, False, None)
    if res[2] != 0:
        print res[1]

def make_debug(workspace, extrac_config=None):
    CMD=['make']
    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, True, None)

def make_install(workspace, extrac_config=None):
    CMD=['make', 'install']
    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, False, None)
    if res[2] != 0:
        print res[1]

def make_initramfs(workspace, output_dir, initramfs_file='root_initramfs.cpio.gz'):
    output_file = ops.path_join(output_dir, initramfs_file)
    CMD=['find', '.', '-print0', '|', 'cpio', '--null', '-ov', '--format=newc', '|', 'gzip', '-9', '>', output_file]
    res = ops.execCmd(CMD, workspace, True, None)
    if res[2] != 0:
        print res[1]

def make_squashfs(workspace, output_dir):
    output_file = ops.path_join(output_dir, "rootfs.squashfs")
    CMD=['mksquashfs', workspace, output_file, '-noappend', '-all-root', '-comp', 'lzo']
    res = ops.execCmd(CMD, workspace, True, None)
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
    bin_pkg_path = getBinPkgPath(pkg_name)
    full_dst = ops.path_join(bin_pkg_path, dst)
    ops.mkdir(full_dst)
    ops.copyto(bin_obj, full_dst)

def installPkg(pkg_name):
    binary_package = getBinPkgPath(pkg_name)
    target_rootfs = ops.getEnv("ARCH_ROOTFS")
    sdk_include = getSdkInclude()
    for obj in os.listdir(binary_package):
        full_path = ops.path_join(binary_package, obj)
        if obj in ["include"]:
            ops.path_join(full_path, ".")
            ops.copyto(ops.path_join(full_path, "."), getSdkInclude())
            continue
        if obj in ["Package", ".git", "LICENSE", ".gitignore"]:
            continue
        ops.copyto(full_path, target_rootfs)
        ops.copyto(full_path, getSdkPath())

def genPackagesList(output_dir, pkg_list):
    pkg_list.sort()
    fp = open(ops.path_join(output_dir, "package_list.json"), "w+")
    fp.writelines("{" + os.linesep)
    fp.writelines("\"DEBUG\":false," + os.linesep)
    fp.writelines("\"name\":\"all_packages\"," + os.linesep)
    fp.writelines("\"packages_dir\":\"packages\"," + os.linesep)
    fp.writelines("\"packages\":[" + os.linesep)
    for pkg in pkg_list:
        fp.writelines("{\"enabled\": 1, \"name\":" + "\"" + pkg + "\"}," + os.linesep)
    fp.writelines("{\"enabled\": 0, \"name\":\"\"}" + os.linesep)
    fp.writelines("]," + os.linesep)
    fp.writelines("\"version\":\"1.0.0\"" + os.linesep)
    fp.writelines("}" + os.linesep)

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
    fp.writelines("  iopc.installPkg(args['pkg_name'], args['pkg_path'])" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.writelines("def MAIN_CLEAN_BUILD(args):" + os.linesep)
    fp.writelines("  return False" + os.linesep)
    fp.close()

def packPkg(pkg_name):
    bin_pkg_path = getBinPkgPath(pkg_name)
    pkg_config_path = ops.path_join(bin_pkg_path, "Package")
    ops.mkdir(pkg_config_path)
    genPkgFiles(pkg_config_path)

