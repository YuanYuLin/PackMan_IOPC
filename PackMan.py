import sys
import os

def setLibPath():
    # append library path
    python_lib = os.path.abspath("pylib")
    sys.path.append(python_lib)

def loadJson2Obj(path):
    import iopc
    return iopc.loadJson2Obj(path)

def SyncMain(args):
    import action_sync
    action_sync.Main(args)

def BuildMain(args):
    import action_build
    action_build.Main(args)

def StatusMain(args):
    import action_status
    action_status.Main(args)

def CommitMain(args):
    import action_commit
    action_commit.Main(args)

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
    if len(sys.argv) < 4:
        help()
        sys.exit(1)

    json_menu    = sys.argv[1]
    account_menu = sys.argv[2]
    action       = sys.argv[3]

    if action not in ActionTable:
        help()
        sys.exit(1)

    setLibPath()
    cfg     = loadJson2Obj(json_menu)
    account = loadJson2Obj(account_menu)

    import iopc
    args = {}
    iopc.setCfg(args, cfg)
    iopc.setAccount(args, account)
    iopc.setParams(args, sys.argv[3:])

    ActionTable[action](args)

