import imp
import sys
import json
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
    packages_dir = cfg['packages_dir']
    packages = cfg['packages']
    for pkg in packages:
        pkg_desc = ""
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        if (pkg_name == "") and (not pkg_enabled):
            continue
        if pkg_enabled :
            pkg_desc += "enabled:"
        else:
            pkg_desc += "disabled:"
        pkg_desc += "[ " + pkg_name + " ]"
        print pkg_desc
