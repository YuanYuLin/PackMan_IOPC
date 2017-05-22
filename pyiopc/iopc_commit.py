import imp
import sys
import json
import os
import subprocess
import pprint
import iopc
import ops
import ops_git

def CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    if 1 == 1: #pkg_enabled == 1:
        if(os.path.exists(local_repo_path)):
            print "GIT commit [ " + pkg_name + " ]"
            version = ops_git.get_version_from_log(local_repo_path)
            major = version[0]
            minor = version[1] + 1
            aux = version[2]
            user_home_path = os.path.expanduser("~")

            while True:
                commit_msg = ops_git.get_commit_msg(user_home_path, major, minor, aux)
                print "=Commit Message==========="
                print commit_msg

                status = ops_git.status(local_repo_path)
                if status :
                    if len(status) == 3:
                        if status[2] == 0:
                            print status[0]
                        else:
                            print status[1]
                else:
                    print "Not a git repository!!"

                print "=========================="

                input_answer = raw_input(">>commit([Y]es/[N]o/E[x]it/[E]dit)")
                if (input_answer == "e"):
                    CMD=['vi', ops_git.get_commit_msg_file(user_home_path)]
                    ops.execCmd(CMD, local_repo_path, False, None)
                    continue
                if (input_answer == "x"):
                    print "Exit..."
                    sys.exit(1)
                elif (input_answer == "y"):
                    break
                elif (input_answer == ""):
                    continue
                else:
                    print "Answer " + input_answer
                    return

            ops_git.commit(local_repo_path, major, minor, aux, commit_msg)
            print "GIT commit END"

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
                CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)
        else:
            CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path)

