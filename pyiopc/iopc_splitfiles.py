import imp
import sys
import json
import os
import subprocess
import pprint
import iopc
import ops
import ops_git

def checkSize_and_splitFilelist(folder):
    for filename in os.listdir(folder):
        statinfo = os.stat(ops.path_join(folder, filename))
        if statinfo.st_size > iopc.MAX_FILE_SIZE:
            print(folder, filename, statinfo.st_size)
            response = iopc.split_file(folder, filename)
            if len(response) >= 3:
                if response[2] == 0:
                    if iopc.gen_split_info(folder, filename, response[0]):
                        os.unlink(ops.path_join(folder, filename))
                        continue

            sys.exit(1)
        

def CheckFileAndSplitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    if(ops.isExist(local_repo_path)):
        checkSize_and_splitFilelist(local_repo_path)

def Main(args):
    account = iopc.getAccount(args)
    cfg = iopc.getCfg(args)
    params = iopc.getParams(args)
    is_single_package = iopc.isSinglePackage(args)
    single_package_name = iopc.getSinglePackageName(args)
    packages_dir = cfg['packages_dir']
    packages = cfg['packages']
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(packages_dir + os.sep + pkg_name)
        remote_repo_path = account["URL"] + pkg_name
        if pkg_name == "":
            continue
        if is_single_package:
            if single_package_name == pkg_name:
                CheckFileAndSplitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
        else:
            CheckFileAndSplitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)

