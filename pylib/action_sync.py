import imp
import sys
import json
import os
import subprocess
import pprint
import git
import iopc

def Main(actt, cfg):
    packages = cfg['packages']
    for pkg in packages:
        pkg_name = pkg['name']
        pkg_enabled = pkg['enabled']
        local_repo_path = os.path.abspath(pkg_name)
        print local_repo_path + iopc.PACKAGE_CFG
        if pkg_enabled == 1:
            if(os.path.exists(local_repo_path)):
                print "GIT pull " + pkg_name
                try:
                    Git = git.cmd.Git(local_repo_path)
                    ret = Git.pull()
                except Exception as ex:
                    print ex
                print "GIT pull END"
            else:
                print "GIT clone " + pkg_name
                try:
                    Git = git.cmd.Git()
                    remote_repo = account["URL"] + pkg_name
                    ret = Git.clone(remote_repo)
                except Exception as ex:
                    print ex
                print "GIT clone END"

