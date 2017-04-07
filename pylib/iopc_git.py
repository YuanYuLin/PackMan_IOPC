import subprocess
import os
import sys

def execCmd(cmd_list, work_dir, debug, proc_output=subprocess.PIPE):
    DEBUG = debug
    cmd_str = ''
    response = []
    if DEBUG == False:
        if os.name == "nt":
            proc=subprocess.Popen(cmd_list, cwd=work_dir, shell=True, stdout=proc_output, stderr=proc_output)
        else:
            proc=subprocess.Popen(cmd_list, cwd=work_dir, stdout=proc_output, stderr=proc_output)

        if proc_output == subprocess.PIPE:
            response = proc.communicate()

        proc.wait()

        if proc_output == subprocess.PIPE:
            if response[0] :
                print "    *" + response[0]
            if response[1] :
                print "    *" + response[1]

    if DEBUG == True:
        for cmd in cmd_list:
            cmd_str += cmd + ' '
        print cmd_str

    return response

def clone(remote_repo_path):
    CMD = ['git', 'clone', remote_repo_path]
    return execCmd(CMD, ".", False, None)

def pull(local_repo_path):
    CMD = ['git', 'pull']
    return execCmd(CMD, local_repo_path, False, None)

def status(local_repo_path):
    CMD = ['git', 'status']
    return execCmd(CMD, local_repo_path, False, None)

def commit(local_repo_path):
    CMD = ['git', 'add', '.']
    execCmd(CMD, local_repo_path, False, None)

    CMD =  ['git', 'commit']
    execCmd(CMD, local_repo_path, False, None)

    CMD = ['git', 'push']
    execCmd(CMD, local_repo_path, False, None)

