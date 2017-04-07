import imp
import sys
import json
import os
import subprocess
import pprint
import iopc
import iopc_git

def CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    if pkg_enabled == 1:
        if(os.path.exists(local_repo_path)):
            print "GIT status " + pkg_name
            iopc_git.commit(local_repo_path)
            print "GIT status END"

def Main(args):
    account = iopc.getAccount(args)
    cfg = iopc.getCfg(args)
    params = iopc.getParams(args)
    is_single_package = iopc.isSinglePackage(args)
    single_package_name = iopc.getSinglePackageName(args)
    packages = cfg['packages']
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(pkg_name)
        remote_repo_path = account["URL"] + pkg_name
        if is_single_package:
            if single_package_name == pkg_name:
                CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
        else:
            CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)

