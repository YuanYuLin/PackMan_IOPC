import imp
import sys
import os
import subprocess
import pprint
import iopc
import ops_git

def mergeFile(workspace):
    for filename in os.listdir(folder):
        if iopc.is_split_info(filename):
            file_list = iopc.read_split_info(workspace, info_file)
            iopc.merge_file(workspace, file_list)

def SyncPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    if 1 == 1: #pkg_enabled == 1:
        print local_repo_path
        if(os.path.exists(local_repo_path)):
            print "GIT pull " + pkg_name
            Git = ops_git.pull(local_repo_path)
            print "GIT pull END"
        else:
            print "GIT clone " + pkg_name
            local_repo_path = os.path.abspath(local_repo_path + os.sep + '..')
            Git = ops_git.clone(remote_repo_path, local_repo_path)
            print "GIT clone END"

def Main(args):
    account = iopc.getAccount(args)
    cfg = iopc.getCfg(args)
    params = iopc.getParams(args)
    is_single_package = iopc.isSinglePackage(args)
    single_package_name = iopc.getSinglePackageName(args)
    packages_dir = os.path.abspath(cfg['packages_dir'])
    packages = cfg['packages']
    pkg_name_list = []
    print cfg
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(packages_dir + os.sep + pkg_name)
        remote_repo_path = account["URL"] + pkg_name
        print pkg_name
        if is_single_package:
            if single_package_name == pkg_name:
                print "SS", pkg_name
                SyncPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
                #mergeFilelist(local_repo_path)
        else:
            pkg_name_list.append(pkg_name)
            print "SS", pkg_name
            SyncPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
            #mergeFilelist(local_repo_path)

#    if not is_single_package:
#        iopc.genPackagesList(packages_dir, pkg_name_list)

