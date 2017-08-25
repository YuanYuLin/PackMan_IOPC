import imp
import sys
import os
import subprocess
import pprint
import iopc
import ops_git

def Main(args):
    account = iopc.getAccount(args)
    cfg = iopc.getCfg(args)
    params = iopc.getParams(args)
    is_single_package = iopc.isSinglePackage(args)
    single_package_name = iopc.getSinglePackageName(args)
    packages_dir = os.path.abspath(cfg['packages_dir'])
    packages = cfg['packages']
    pkg_name_list = []
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(packages_dir + os.sep + pkg_name)
        remote_repo_path = account["URL"] + pkg_name
        pkg_name_list.append(pkg_name)

    iopc.genPackagesList(packages_dir, pkg_name_list)

