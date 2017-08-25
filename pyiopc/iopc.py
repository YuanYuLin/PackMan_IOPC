import ops
import os
import sys

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

def getOutputRootDir():
    rootfs_dir = ops.getEnv("OUTPUT_ROOTFS_DIR")
    return rootfs_dir

def getBaseRootFile(file_path=None):
    base_rootfs_dir = ops.getEnv("BASE_ROOTFS_DIR")
    if file_path == None:
        return base_rootfs_dir
    else:
        return ops.path_join(base_rootfs_dir, file_path)

def getDevPkgPath(pkg_name):
    dev_pkg_path = ops.path_join(getOutputRootDir(), "Dev/" + pkg_name)
    ops.mkdir(dev_pkg_path)
    return dev_pkg_path

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

def make_web(workspace, materials_dir, menu_file, food_dir, debug=False):
    CMD=["python2.7", "cook.py", materials_dir, menu_file, food_dir, "MAKE"]

    res = ops.execCmd(CMD, workspace, debug, None)

    if debug:
        return 0

    if res[2] != 0:
        print res[1]
        sys.exit(1)

def configure(workspace, extrac_config=None, env_config=None, debug=False):

    CMD=[]
    if (debug and env_config):
        for env in env_config:
            CMD.append(env + '="' + env_config[env] + '"')

    #CMD=['./configure']
    CMD.append('./configure')

    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, debug, None, env_config=env_config)
    if debug:
        return 0

    if res[2] != 0:
        print res[1]
        sys.exit(1)

def make(workspace, extrac_config=None, debug=False):
    CMD=['make']
    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, debug, None)
    if res[2] != 0:
        print res[1]
        sys.exit(1)

def make_debug(workspace, extrac_config=None):
    CMD=['make']
    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, True, None)

def make_install(workspace, extrac_config=None, debug=False):
    CMD=['make', 'install']
    if extrac_config:
        for cfg in extrac_config:
            CMD.append(cfg)

    res = ops.execCmd(CMD, workspace, False, None)
    if res[2] != 0:
        print res[1]
        sys.exit(1)

def make_initramfs(workspace, output_dir, initramfs_file='root_initramfs.cpio.gz'):
    output_file = ops.path_join(output_dir, initramfs_file)
    CMD=['find', '.', '|', 'cpio', '-H', 'newc', '-o', '|', 'gzip', '-9', '>', output_file]
    res = ops.execCmd(CMD, workspace, True, None)
    print res
    if res[2] != 0:
        print res[1]

def make_squashfs(workspace, output_dir):
    output_file = ops.path_join(output_dir, "rootfs.squashfs")
    ops.rm_file(output_file)
    CMD=['mksquashfs', workspace, output_file, '-noappend', '-all-root', '-comp', 'lzo']
    res = ops.execCmd(CMD, output_dir, False, None)
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
            for root, dirnames, filenames in os.walk(full_path):
                for f_obj in filenames:
                    ops.copyto(ops.path_join(root, f_obj), getDevPkgPath(pkg_name))
            continue
        if obj in ["Package", ".git", "LICENSE", ".gitignore"]:
            continue
        ops.copyto(full_path, target_rootfs)
        ops.copyto(full_path, getSdkPath())
        for root, dirnames, filenames in os.walk(full_path):
            for f_obj in filenames:
                ops.copyto(ops.path_join(root, f_obj), getDevPkgPath(pkg_name))

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

def get_patch_list(pkg_path, patch_name):
    pkg_path = ops.path_join(pkg_path, "Package")
    patch_path = ops.path_join(pkg_path, "patches")
    patch_menu = ops.path_join(patch_path, "patch_menu")
    patch_list = ops.loadJson2Obj(patch_menu)
    patches = []
    for patch_group in patch_list:
        if patch_group == patch_name:
            for patch in patch_list[patch_group]:
                if patch["enabled"]:
                    patches.append(ops.path_join(patch_path, patch["name"]))
    return patches

def apply_patch(workspace, patch_file):
    CMD=['patch', '-p1', '-b', '-i', patch_file]
    print workspace
    print patch_file
    res = ops.execCmd(CMD, workspace, False, None)
    if res[2] != 0:
        return False
    return True
