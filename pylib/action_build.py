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

def Main(actt, cfg):
    packages = cfg['packages']
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(pkg_name)
        if pkg_enabled == 1:
            if(os.path.exists(local_repo_path)):
                print "Build " + pkg_name
                build_pkg = _loadModule(iopc.PACKAGE_CFG, [pkg_name])
                try:
                    build_pkg.MAIN()
                except Exception as ex:
                    print ex
            else:
                print local_repo_path + " Not exist!"

