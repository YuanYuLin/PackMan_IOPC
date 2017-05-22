import imp
import sys
import json
import os
import subprocess
import pprint
import iopc
import ops_git

def ListPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    sym = "!"
    msg = "| "
    if 1 == 1: #pkg_enabled == 1:
        if(os.path.exists(local_repo_path)):
            status = ops_git.status(local_repo_path)
            if status :
                if len(status) == 3:
                    if status[2] == 0:
                        sym = "M"
                    else:
                        sym = "E"
                else:
                    sym = "!"
            else:
                sym = "@" 
    if sym == "@":
        user_action = "create repository"
    elif sym == "M":
        user_action = "commit           "
    else:
        user_action = "                 "

    msg = "< "
    msg += sym
    msg += " | "
    msg += user_action
    msg += " > "
    msg += " [ "
    msg += pkg_name
    msg += " ]"
    print msg 

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
        local_repo_path = os.path.abspath(packages_dir + os.sep + pkg_name)
        remote_repo_path = account["URL"] + pkg_name
        if pkg_name == "":
            continue
        if is_single_package:
            if single_package_name == pkg_name:
                ListPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
        else:
            ListPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
    print "M: Modified, @: Not git repo, E: Error, !: Unknow"
