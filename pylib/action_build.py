import imp
import sys
import json
import os
import subprocess
import pprint
import git
import iopc

def _loadModule(module_name, module_path):
    imp_fp, imp_pathname, imp_description = imp.find_module(module_name, module_path)
    module = imp.load_module('packageComponent', imp_fp, imp_pathname, imp_description)
    return module

def buildModule(pkg_enabled, pkg_name, local_repo_path):
    if pkg_enabled == 1:
        if(os.path.exists(local_repo_path)):
            print "Build " + pkg_name
            build_pkg = _loadModule(iopc.PACKAGE_CFG, [pkg_name])
            build_pkg.MAIN()
        else:
            print local_repo_path + " Not exist!"


def Main(args):
    cfg = iopc.getCfg(args)
    account = iopc.getAccount(args)
    params = iopc.getParams(args)
    is_single_package = iopc.isSinglePackage(args)
    single_package_name = iopc.getSinglePackageName(args)
    packages = cfg['packages']
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(pkg_name)
        if is_single_package:
            if single_package_name == pkg_name:
                buildModule(pkg_enabled, pkg_name, local_repo_path)
        else:
            buildModule(pkg_enabled, pkg_name, local_repo_path)

