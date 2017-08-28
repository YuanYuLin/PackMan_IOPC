import imp
import sys
import os
import subprocess
import pprint
import iopc
import ops_git

def mergeFile(folder):
    for filename in os.listdir(folder):
        if iopc.is_split_info(folder, filename):
            info = iopc.read_split_info(folder, filename)
            if iopc.merge_file(folder, info):
                iopc.unlink_split_data(folder, info)

def MergePackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    if(os.path.exists(local_repo_path)):
        mergeFile(local_repo_path)

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
        if is_single_package:
            if single_package_name == pkg_name:
                MergePackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
        else:
            pkg_name_list.append(pkg_name)
            MergePackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)

