import sys
import os

def setLibPath():
    # append library path
    python_lib = os.path.abspath("pylib")
    sys.path.append(python_lib)

    if not os.path.exists(python_lib):
        print "Please download [pylib] from github!!"
        sys.exit(1)

    sys.path.append(python_lib)
    python_lib = os.path.abspath("pyiopc")
    sys.path.append(python_lib)

def loadJson2Obj(path):
    import ops
    return ops.loadJson2Obj(path)

def SyncMain(args):
    import iopc_sync
    iopc_sync.Main(args)

def BuildMain(args):
    import iopc_build
    iopc_build.Main(args)

def StatusMain(args):
    import iopc_status
    iopc_status.Main(args)

def CommitMain(args):
    import iopc_commit
    iopc_commit.Main(args)

def help():
    print "PackMan.py <menu file> <account file> <Action>"
    print "  Action:"
    for act in ActionTable:
        print "    " + act

ActionTable = {
    "SYNC": SyncMain,
    "BUILD": BuildMain,
    "STATUS": StatusMain,
    "COMMIT": CommitMain,
}

if __name__ == '__main__':
    setLibPath()

    if len(sys.argv) < 4:
        help()
        sys.exit(1)

    json_menu    = sys.argv[1]
    account_menu = sys.argv[2]
    action       = sys.argv[3]

    if action not in ActionTable:
        help()
        sys.exit(1)

    cfg     = loadJson2Obj(json_menu)
    account = loadJson2Obj(account_menu)

    import iopc
    args = {}
    iopc.setCfg(args, cfg)
    iopc.setAccount(args, account)
    iopc.setParams(args, sys.argv[3:])

    ActionTable[action](args)

