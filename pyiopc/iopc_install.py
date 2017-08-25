import sys
import os
import iopc
import ops

def buildModule(pkg_enabled, pkg_name, pkg_args, local_repo_path, output_path):
    if pkg_enabled == 1:
        print "===Install===[" + pkg_name + "]"
        ops.mkdir(output_path)
        if(os.path.exists(local_repo_path)):
            build_pkg = None
            build_pkg = ops.loadModule(pkg_name, iopc.PACKAGE_CFG, [local_repo_path])
            args = {"pkg_name": pkg_name, "pkg_path": local_repo_path, "output_path": output_path, "pkg_args": pkg_args}
            stamp_file = output_path + os.sep + "STAMP.INSTALL"
            if not os.path.exists(stamp_file):
                res = build_pkg.MAIN_INSTALL(args)
                iopc.packPkg(pkg_name)
                iopc.installPkg(pkg_name)
                if res:
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
        local_repo_path = os.path.abspath(ops.path_join(packages_dir, pkg_name))
        output_path = os.path.abspath(ops.path_join(output_dir, pkg_name))
        if is_single_package:
            if single_package_name == pkg_name:
                buildModule(pkg_enabled, pkg_name, pkg_args, local_repo_path, output_path)
                return
        else:
            buildModule(pkg_enabled, pkg_name, pkg_args, local_repo_path, output_path)

