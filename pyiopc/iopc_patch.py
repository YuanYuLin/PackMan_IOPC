import sys
import os
import iopc
import ops

def buildModule(pkg_enabled, pkg_name, pkg_args, pkg_patch, local_repo_path, output_path):
    if pkg_enabled == 1:
        print "===Patch===[" + pkg_name + "]"
        ops.mkdir(output_path)
        if(os.path.exists(local_repo_path)):
            build_pkg = None
            build_pkg = ops.loadModule(pkg_name, iopc.PACKAGE_CFG, [local_repo_path])
            args = {"pkg_name": pkg_name, "pkg_path": local_repo_path, "output_path": output_path, "pkg_args": pkg_args}
            stamp_file = output_path + os.sep + "STAMP.PATCH"
            if not os.path.exists(stamp_file):
                if build_pkg.MAIN_PATCH(args, pkg_patch):
                    ops.touch(stamp_file)
        else:
            print local_repo_path + " Not exist!"

def Main(args):
    cfg = iopc.getCfg(args)
    account = iopc.getAccount(args)
    params = iopc.getParams(args)
    output_dir = iopc.getOutputDir(args)
    is_single_package = iopc.isSinglePackage(args)
    single_package_name = iopc.getSinglePackageName(args)
    packages_dir = cfg['packages_dir']
    packages = cfg['packages']
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        pkg_args = pkg['args']
        pkg_patch = pkg['patch']
        local_repo_path = os.path.abspath(packages_dir + os.sep + pkg_name)
        output_path = os.path.abspath(output_dir + os.sep + pkg_name)
        if is_single_package:
            if single_package_name == pkg_name:
                buildModule(pkg_enabled, pkg_name, pkg_args, pkg_patch, local_repo_path, output_path)
                return
        else:
            buildModule(pkg_enabled, pkg_name, pkg_args, pkg_patch, local_repo_path, output_path)

