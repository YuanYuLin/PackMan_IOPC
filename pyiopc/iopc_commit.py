import imp
import sys
import json
import os
import subprocess
import pprint
import iopc
import ops
import ops_git

def checkSize_filelist(folder):
    for filename in os.listdir(folder):
        statinfo = os.stat(ops.path_join(folder, filename))
        if statinfo.st_size > iopc.MAX_FILE_SIZE:
            print(folder, filename, statinfo.st_size)
            print "Please SPLIT file", filename
            sys.exit(1)
        

def CommitPackage(pkg_enabled, pkg_name, remote_repo_path, local_repo_path):
    if 1 == 1: #pkg_enabled == 1:
        if(ops.isExist(local_repo_path)):
            checkSize_filelist(local_repo_path)
            exit
            print(chr(27) + "[2J")
            #print "PKG [ " + pkg_name + " ]"
            version = ops_git.get_version_from_log(local_repo_path)
            major = version[0]
            minor = version[1] + 1
            aux = version[2]
            user_home_path = os.path.expanduser("~")

            while True:
                isGitRepository = True
                commit_msg = ops_git.get_commit_msg(user_home_path, major, minor, aux)
                #print "=Commit Message==========="
                #print commit_msg

                status = ops_git.status(local_repo_path)
                if status :
                    print "PKG: [%s]" % (pkg_name)
                else:
                    print "Not a git repository!!"
                    isGitRepository = False

                print "=========================="

                if isGitRepository :
                    if len(status) == 3:
                        if status[2] == 0:
                            if status[0].find("nothing to commit") != -1:
                                break
                    input_answer = raw_input(">>commit([Y]es/[N]o/E[x]it/[E]dit/[S]Detail)")
                    if (input_answer == "e"):
                        CMD=['vi', ops_git.get_commit_msg_file(user_home_path)]
                        ops.execCmd(CMD, local_repo_path, False, None)
                        continue
                    if (input_answer == "s"):
                        if len(status) == 3:
                            if status[2] == 0:
                                print status[0]
                            else:
                                print status[1]
                        continue
                    elif (input_answer == "x"):
                        print "Exit..."
                        sys.exit(1)
                    elif (input_answer == "y"):
                        ops_git.commit(local_repo_path, major, minor, aux, commit_msg)
                        break
                    elif (input_answer == ""):
                        continue
                    else:
                        print "Answer " + input_answer
                        return

                print "GIT commit END"
                return

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

