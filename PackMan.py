import sys
import os
import pprint

def SyncMain(args):
    import iopc_sync
    iopc_sync.Main(args)

def StatusMain(args):
    import iopc_status
    iopc_status.Main(args)

def CommitMain(args):
    import iopc_commit
    iopc_commit.Main(args)

def ListMain(args):
    import iopc_list
    iopc_list.Main(args)

def GenListMain(args):
    import iopc_genlist
    iopc_genlist.Main(args)

def SplitFilesMain(args):
    import iopc_splitfiles
    iopc_splitfiles.Main(args)

def MergeFilesMain(args):
    import iopc_mergefiles
    iopc_mergefiles.Main(args)

ActionTable = {
    "SYNC": SyncMain,
    "STATUS": StatusMain,
    "COMMIT": CommitMain,
    "LIST" : ListMain,
    "GENLIST": GenListMain,
    "SPLITFILES": SplitFilesMain,
    "MERGEFILES": MergeFilesMain,
}

def help():
    print "PackMan.py <packages_dir> <Action>"
    print "  Action:"
    for act in ActionTable:
        print "    " + act
    sys.exit(1)

def setLibPath():
    # append library path
    python_lib = os.path.abspath("pylib")
    sys.path.append(python_lib)

    if not os.path.exists(python_lib):
        print "Please download [pylib] from github!!"
        print "git clone https://github.com/YuanYuLin/pylib.git"
        sys.exit(1)

    sys.path.append(python_lib)
    python_lib = os.path.abspath("pyiopc")
    sys.path.append(python_lib)

def loadJson2Obj(path):
    import ops
    return ops.loadJson2Obj(path)

if __name__ == '__main__':
    setLibPath()

    if len(sys.argv) < 3:
        help()

    packages_dir = sys.argv[1]
    action       = sys.argv[2]

    if action not in ActionTable:
        help()

    # Check and Load Packages configs
    cfg = {"DEBUG":False, "name":"packages_dir", "packages_dir":"packages", "packages":[]}
    for obj in os.listdir(packages_dir):
        if os.path.isdir(os.path.join(packages_dir, obj)):
            cfg["packages"].append({"enabled":True, "name": obj})
    '''
    packages_path = os.path.abspath(packages_dir + os.sep + ".packages.json")
    if not os.path.exists(packages_path):
        print "[" + packages_path + "] not exist!"
        help()
    cfg = loadJson2Obj(packages_path)
    '''
    # Check and Load Account configs 
    account_path = os.path.abspath("account.json")
    if not os.path.exists(account_path):
        print "[" + account_path + "] not exist!"
        help()
    account = loadJson2Obj(account_path)

    import iopc
    args = {}
    iopc.setCfg(args, cfg)
    iopc.setAccount(args, account)
    iopc.setParams(args, sys.argv[2:])

    ActionTable[action](args)

