import sys
import os

def ExportEnvs(args):
    import ops
    cfg = iopc.getCfg(args)
    envs = cfg['envs']
    for env in envs:
        if env['enabled']:
            ops.exportEnv(env['env'])

def EnvMain(args):
    import iopc_env
    iopc_env.Main(args)

def ExtractMain(args):
    import iopc_extract
    iopc_extract.Main(args)

def PatchMain(args):
    import iopc_patch
    iopc_patch.Main(args)

def ConfigureMain(args):
    import iopc_configure
    iopc_configure.Main(args)

def BuildMain(args):
    import iopc_build
    iopc_build.Main(args)

def CleanBuildMain(args):
    import iopc_clean_build
    iopc_clean_build.Main(args)

def InstallMain(args):
    import iopc_install
    iopc_install.Main(args)

def SdkenvMain(args):
    import iopc_sdkenv
    iopc_sdkenv.Main(args)

def AllMain(args):
    cfg = iopc.getCfg(args)
    packages = cfg['packages']
    for pkg in packages:
        for act in ["ENV", "EXTRACT", "PATCH", "CONFIGURE", "BUILD", "INSTALL", "SDKENV"]:
            pkg_enabled = pkg['enabled']
            pkg_name = pkg['name']
            params = [act, pkg_name]
            iopc.setParams(args, params)
            if pkg_enabled:
                ActionTable[act](args)


ActionTable = {
    "ALL": AllMain,
    "ENV": EnvMain,
    "EXTRACT": ExtractMain,
    "PATCH" : PatchMain,
    "CONFIGURE": ConfigureMain,
    "BUILD": BuildMain,
    "INSTALL": InstallMain,
    "SDKENV" : SdkenvMain,
    "CLEANBUILD": CleanBuildMain,
}

def help():
    print "BuildMan.py <packages_dir> <output_dir> <Action>"
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

    if len(sys.argv) < 4:
        help()

    packages_dir = sys.argv[1]
    output_dir   = sys.argv[2]
    action       = sys.argv[3]

    if action not in ActionTable:
        help()

    # Check and Load Packages configs
    packages_path = os.path.abspath(output_dir + os.sep + ".packages.json")
    if not os.path.exists(packages_path):
        print "[" + packages_path + "] not exist!"
        help()
    cfg = loadJson2Obj(packages_path)

    # Check and Load Account configs 
    account_path = os.path.abspath("account.json")
    if not os.path.exists(account_path):
        print "[" + account_path + "] not exist!"
        help()
    account = loadJson2Obj(account_path)

    import iopc
    args = {}
    iopc.setCfg(args, cfg)
    iopc.setOutputDir(args, output_dir)
    iopc.setAccount(args, account)
    iopc.setParams(args, sys.argv[3:])
    ExportEnvs(args)

    ActionTable[action](args)

