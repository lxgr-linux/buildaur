#!/usr/bin/env python3
# maintainer lxgr <lxgr@protonmail.com>
# this software is licensed under the GPL v3
# WARNING: This is experimental code!

import os
import progressbar_buildaur as progressbar
import time
import requests
import sys
from pyalpm import Handle
from pathlib import Path
# res=os.popen("cat /usr/share/buildaur/res").read()

def options(string, optlen):
    global mkopts
    global pcarg
    options.confirm=True
    options.install=True
    options.color=True
    options.chroot=False
    if string.find("n") != -1:
        options.confirm=False
        pcarg+=" --noconfirm"
        optlen+=1
    if string.find("di") != -1:
        options.install=False
        optlen+=2
    if string.find("co") != -1:
        global yellow
        global red
        global thic
        mkopts+=" -m"
        yellow=""
        red=""
        thic=""
        optlen+=2
    if string.find("spgp") != -1:
        mkopts+=" --skippgpcheck"
        optlen+=4
    if string.find("ch") != -1:
        options.chroot=True
        optlen+=2
    if optlen != len(string):
        print(":: "+red+"ERROR:\033[0m "+string+" is no valid option!")
        exit(1)

def sorter(ver1, ver2):
	arr1=ver1.split("-")[0].split(".")
	arr2=ver2.split("-")[0].split(".")
	for i in range(sorted([len(arr2), len(arr1)])[1]):
		try:
			a=arr1[i]
		except:
			a="0"
		try:
			b=arr2[i]
		except:
			b="0"
		arg1=len(b)*"0"+a
		arg2=len(a)*"0"+b
		arrs=[arg1, arg2]
		if sorted(arrs)[0] == arg2 and arg1 != arg2:
			return ver1
		elif sorted(arrs)[0] == arg1 and arg1 != arg2:
			return ver2
	if ver1.split("-")[1] > ver2.split("-")[1]:
		return ver1
	elif ver2.split("-")[1] > ver1.split("-")[1]:
		return ver2

def resolve(pkgs, type, quiet):
    if quiet == False:
        print(":: Downloading packagelist...")
    url=proto+"://aur.archlinux.org/rpc/?v=5&type="+type
    if len(pkgs) == 0:
        exit(0)
    if type == "search":
        url+="&by=name&arg="+pkgs[0]
    else:
        # name processing to avoid bad packagenames
        npkgs=[]
        for pkg in pkgs:
            npkg=""
            if "+" in pkg:
                for letter in pkg:
                    if letter == "+":
                        npkg+="%2B"
                    else:
                        npkg+=letter
            else:
                npkg=pkg
            npkgs.append(npkg)
        pkgs=npkgs
        # producing url
        for pkg in pkgs:
            url=url+"&arg[]="+pkg
    try:
        r=requests.get(url)
    except:
        print(":: "+red+"ERROR:\033[0m Server is not reachable!")
        exit(1)
    resolve.res=str(r.content)

def info(res, quiet):
    info.rescount=res.split('"')[8].split(":")[1].split(",")[0]
    info.respkgs=[]
    cutted=res.split('{"ID"')
    if quiet == False:
        print(":: Collecting package data...")
    for i in range(int(info.rescount)):
        splitted=cutted[i+1].split('"')
        pkgname=splitted[3]
        pkgver=splitted[13]
        pkgdesc=splitted[17]
        pkgoutdate=splitted[28]
        if pkgoutdate in [":"]:
            pkgoutdate=splitted[26]
        try:
            pkg=localdb.get_pkg(pkgname)
            localver=pkg.version
        except:
            localver="---"
        array=[pkgname, pkgver, localver, pkgoutdate, pkgdesc]
        info.respkgs.append(pkgname)
        if quiet == False:
            progressbar.progress(i+1, int(info.rescount), "Collecting "+pkgname+"...")
        exec("info.array_"+str(i)+"=array")

def aspinfo(pkgs, quiet):
    print(":: Updatting asp database...")
    os.system("asp update 2>/dev/null")
    info.rescount=0
    if quiet == False:
        print(":: Collecting package data...")
    n=0
    for pkg, i in zip(pkgs, range(len(pkgs))):
        pkgname=pkg
        pkgver=os.popen("/usr/share/buildaur/outputter.sh asp "+pkg).read().split("\n")[0]
        try:
            pkg=localdb.get_pkg(pkgname)
            localver=pkg.version
        except:
            localver="---"
        pkgoutdate=":null,"
        pkgdesc="some pkg from asp"
        if pkgver != "error":
            array=[pkgname, pkgver, localver, pkgoutdate, pkgdesc]
            exec("info.array_"+str(n)+"=array")
            info.rescount+=1
            n+=1
        if quiet == False:
            progressbar.progress(i+1, int(len(pkgs)), "Collecting "+pkgname+"...")

def update():
    msg=[]
    update.willinst=[]
    pkgs=os.popen("pacman -Qqm").read().split("\n")
    resolve(pkgs,"multiinfo", False)
    if mode == "asp":
        info(resolve.res, True)
        npkgs=[]
        for pkg in pkgs:
            if pkg not in info.respkgs:
                npkgs.append(pkg)
        del npkgs[-1]
        info.rescount=0
        aspinfo(npkgs, False)
    else:
        info(resolve.res, False)
    print(":: Checking for outdated packages...")
    for i in range(int(info.rescount)):
        exec("update.out=info.array_"+str(i))
        pkgname=update.out[0]
        pkgver=update.out[1]
        localver=update.out[2]
        pkgoutdate=update.out[3]
        progressbar.progress(i+1, int(info.rescount), "Checking "+pkgname+"...")
        if pkgver == localver or pkgname in black:
            print("", end="")
        elif sorter(pkgver, localver) == pkgver:
            update.willinst.append(pkgname)
        elif sorter(pkgver, localver) == localver:
            msg.append(" "+yellow+"Warning:\033[0m "+pkgname+"-"+localver+" is higher than AUR "+pkgver+"!")
            if ask_warn_inst == 1:
                update.willinst.append(pkgname)
        if pkgoutdate != ":null,":
            msg.append(" "+yellow+"Warning:\033[0m "+pkgname+" is flagged as out-of-date!")
    print(":: Done")
    for i in msg:
        print(i)
    if update.willinst == []:
        print(" Nothing to do")
    else:
        install(update.willinst)

def infoout(res, quiet):
    info(res, True)
    for i in range(int(info.rescount)):
        exec("infoout.out=info.array_"+str(i))
        pkgname=infoout.out[0]
        if quiet:
            print(pkgname)
        else:
            pkgver=infoout.out[1]
            localver=infoout.out[2]
            pkgoutdate=infoout.out[3]
            pkgdesc=infoout.out[4]
            print(" "+pkgname+"-"+pkgver+" (local: "+localver+")")
            print("    "+pkgdesc)

def install(pkgs):
    pkgpathes=[]
    pkgsout=[]
    install=[]
    if mode == "asp":
        aspinfo(pkgs, True)
        print(":: Checking packages...")
    else:
        resolve(pkgs, "multiinfo", False)
        print(":: Checking packages...")
        info(resolve.res, True)
    # Check if package is realy in AUR
    for i in range(int(info.rescount)):
        exec("update.out=info.array_"+str(i))
        pkgsout.append(update.out[0])
    if len(pkgs) != len(pkgsout):
        for pkg in pkgs:
            if pkg not in pkgsout:
                print(":: "+red+"ERROR:\033[0m "+pkg+" not found!")
                exit(1)
    if info.rescount == "0":
        print(" Nothing to do")
        exit(0)
    # Checking packages for existance
    for i in range(int(info.rescount)):
        exec("update.out=info.array_"+str(i))
        pkgname=update.out[0]
        pkgver=update.out[1]
        localver=update.out[2]
        pkgoutdate=update.out[3]
        if pkgver == localver:
            print(" "+thic+"Info:\033[0m "+pkgname+"-"+localver+" is up to date -- reistalling")
        elif localver == "---":
            print("", end="")
        elif sorter(pkgver, localver) == pkgver:
            print(" "+thic+"Info:\033[0m "+pkgname+"-"+localver+" will be updated to "+pkgver)
        elif sorter(pkgver, localver) == localver:
            print(" "+yellow+"Warning:\033[0m "+pkgname+"-"+localver+" is higher than AUR "+pkgver+"!")
        if pkgoutdate != ":null,":
            print(" "+yellow+"Warning:\033[0m "+pkgname+" is flagged as out-of-date!")
        install.append(i)
    # asking to continue
    print("")
    print("Packages ("+str(info.rescount)+"): ", end='')
    for pkg in install:
        exec("update.out=info.array_"+str(pkg))
        pkgname=update.out[0]
        print(pkgname+"-"+pkgver+"  ", end='')
    print("")
    if options.confirm:
        ask=input("\n:: Continnue installation? [Y/n] ")
    else:
        ask="y"
    if ask == "Y" or ask == "y" or ask == "":
        print("")
        # home=os.getcwd()
        count=1
        max=str(info.rescount)
        for pkg in install:
            # full makeprocess
            # vars
            exec("update.out=info.array_"+str(pkg))
            pkgname=update.out[0]
            pkgver=update.out[1]
            print("("+str(count)+"/"+max+") Making package "+thic+pkgname+"\033[0m...")
            # Git repository
            os.chdir(home+"/.cache/buildaur/build")
            if mode == "asp":
                print(":: Exporting package...")
                os.system('rm -rf ./'+pkgname+' 2>/dev/null; asp export '+pkgname+' 2>/dev/null')
            else:
                print(":: Cloning git repository...")
                os.system("rm -rf ./"+pkgname+" 2>/dev/null;")
                while not os.path.exists("./"+pkgname+"/PKGBUILD"):
                    os.system("git clone "+proto+"://aur.archlinux.org/"+pkgname)
            os.chdir(os.getcwd()+"/"+pkgname)
            # edit
            if showPKGBUILD == 1:
                print(":: Printing PKGBUILD...")
                pkgbuild=open("PKGBUILD", "rt").read()
                print("\033[37m"+str(pkgbuild)+"\033[0m", end="")
            if showDiff == 1:
                print(":: Printing PKGDIFF...")
                diff=os.popen('git diff $(git log --pretty=format:"%h" | head -2 | xargs)').read()
                print("\033[37m"+diff+"\033[0m", end="")
            if options.confirm:
                ask=input("\n:: Edit PKGBUILD? [y/c/N] ")
            else:
                ask="n"
            if ask in ['y', 'Y']:
                os.system(editor+" ./PKGBUILD")
                print(":: Going on")
            if ask in ['c', 'C']:
                print(":: Exiting")
                exit()
            # Hooks
            hooks("prehooks")
            # depends
            depts()
            # makepkg
            if options.chroot:
                print(":: Updating chrootpackages...")
                os.system("arch-nspawn $CHROOT/root pacman -Syu "+pcarg)
                print(":: Making the package...")
                os.system("PKGEXT='.pkg"+compmeth+"' makechrootpkg -c -r $CHROOT -- -s"+mkopts)
            else:
                print(":: Making the package...")
                os.system(" PKGEXT='.pkg"+compmeth+"' makepkg -s "+mkopts)
            # Hooks
            hooks("posthooks")
            # Defining pkgpath
            if os.popen('/usr/share/buildaur/outputter.sh arch').read().split('\n')[0] == "any":
                arch='any'
            else:
                arch=os.popen('uname -m').read().split('\n')[0]
            # versioning for packages with multiple packagenames
            ver=os.popen("/usr/share/buildaur/outputter.sh vers").read().split('\n')[0]
            for pkgname in os.popen("/usr/share/buildaur/outputter.sh pkgname").read().split('\n')[0].split(' '):
                pkgpathes.append(os.getcwd()+"/"+pkgname+"-"+ver+"-"+arch+".pkg"+compmeth)
            os.chdir(home)
            count+=1
            print("")
        # installing packages
        if options.install:
            print(":: Installing packages...")
            inststring=""
            for path in pkgpathes:
                inststring=inststring+path+" "
            os.system("sudo pacman -U "+pcarg+" "+inststring)
        else:
            print(":: Package(s) created in:")
            for path in pkgpathes:
                print(" "+path)
    else:
        exit()

def depts():
    nedeps=[]
    neaurdeps=[]
    depends=[]
    print(":: Checking for unresolved dependencies...")
    udepends=os.popen("/usr/share/buildaur/outputter.sh deps").read().split("\n")[0].split(" ")
    for dep in udepends:
        if ">" in dep:
            depends.append(dep.split(">")[0])
        elif "<" in dep:
            depends.append(dep.split("<")[0])
        elif "=" in dep:
            depends.append(dep.split("=")[0])
        else:
            depends.append(dep)
    for pkg in depends:
        paca=localdb.get_pkg(pkg)
        if str(paca) == "None":
            nedeps.append(pkg)
    if len(nedeps) > 0:
        resolve(nedeps,"multiinfo", True)
        info(resolve.res, True)
        if int(info.rescount) != 0:
            for i in range(int(info.rescount)):
                exec("infoout.out=info.array_"+str(i))
                neaurdeps.append(infoout.out[0])
            curdir=os.getcwd()
            os.chdir(home)
            install(neaurdeps)
            os.chdir(curdir)

def list_hooks():
    hooktypes=["prehooks", "posthooks", "prerunhooks", "postrunhooks", "hooks"]
    for hookdir in hooktypes:
        if hookdir == "hooks":
            print(":: deactivated hooks:")
        else:
            print(":: "+hookdir+":")
        for hook in sorted(os.listdir("/etc/buildaur/"+hookdir)):
            print(" "+hook)
            print(os.popen('. /etc/buildaur/'+hookdir+'/'+hook+'; echo "  $desc"').read().split("\n")[0])

def hook_activate(hooks):
    for hook in hooks:
        if hook in os.listdir('/etc/buildaur/hooks/'):
            hooktype=os.popen('. /etc/buildaur/hooks/'+hook+' 2>/dev/null; echo $type').read().split("\n")[0]
            os.system('sudo mv /etc/buildaur/hooks/'+hook+' /etc/buildaur/'+hooktype+'hooks/ 2>/dev/null')
            print(":: Activated "+hook+"!")
        else:
            print(':: '+red+'ERROR:\033[0m '+hook+' not found!')

def hook_deactivate(hooks):
    hooktypes=["prehooks", "posthooks", "prerunhooks", "postrunhooks"]
    for hook in hooks:
        a=0
        for hookdir in hooktypes:
            if hook in os.listdir("/etc/buildaur/"+hookdir):
                os.system('sudo mv  /etc/buildaur/'+hookdir+'/'+hook+' /etc/buildaur/hooks/ 2>/dev/null')
                print(":: Deactivated "+hook+"!")
                a=1
        if a != 1:
            print(':: '+red+'ERROR:\033[0m '+hook+' not found!')

def help():
    print("buildaur - An AUR helper with asp support")
    print("Usage: "+args[0]+" <option> <string>")
    print("   General options:")
    print("      -S                : Installs a package")
    print("      -R                : Removes a package")
    print("      -Q                : Lists installed packages or searches for ones in the AUR")
    print("      -Qs               : Search the AUR")
    print("      -Syu              : Updates all AUR packages")
    #print("      -url              : Installs a package from a given git-repository")
    print("      -asp              : Builds a package from source using asp (usefull for archlinux arm)")
    print("      -aspyu            : Updates all asp packages (usefull for archlinux arm)")
    print("      --show            : Shows the PKGBUILD of a given package")
    print("      --clear           : Cleanes build dir")
    print("      -v|--version      : Displays version of this program")
    print("      -l|--license      : Displays license of this program")
    print("      --make-chroot     : Creates a chroot dir which can be used for building packages")
    print("      --about           : Displays an about text")
    print("")
    print("   Additional options for -S,-R,-Syu,-asp,-aspyu:")
    print("      n                 : Doesn't ask questions")
    print("      spgp              : Skips pgp checks of sourcecode")
    print("      ch                : Builds the package in a clean chroot (you may run into some problems using this on archlinux arm!)")
    print("      di                : Just builds the package")
    print("      co                : Toggles colored output on and off")
    print("")
    print("")
    print("   Additional options for --show:")
    print("      --diff            : Outputs diff between current pkgbuildver and former pkgbuildver")
    print("   Additional options for -Q,-Qs")
    print("      q                 : Just outputs pknames")
    print("      qq                : JUST outputs pknames")
    print("")
    print("   Hookoptions:")
    print("      --listhooks       : Lists all available and installed hooks")
    print("      --hook-activate   : Activates a hook")
    print("      --hook-deactivate : Deactivates a hook")
    print("")
    print("   Help options:")
    print("      -h|--help         : Displays this help-dialog")
    #print("      --help-hooks      : Displays help-dialog for hooks")

def about():
    pkg=localdb.get_pkg("buildaur")
    print("Buildaur "+pkg.version+" -- An AUR helper with asp support\n\nThis package is submited and maintained by lxgr -- <lxgr@protonmail.com>\nThis software is licensed under the GPL3.\n\nThis software is made to help archlinux users to install and update packages from the AUR in a save and consistent way.")

def hooks(type):
    hooks=os.popen("ls /etc/buildaur/"+type).read().split('\n')
    del hooks[-1]
    if len(hooks) > 0:
        print(":: Running "+type+"...")
        for hook in hooks:
            print(" "+hook+"...")
            os.system("/etc/buildaur/"+type+"/"+hook+" -u")

if __name__ == "__main__":
    # global home and pathchecking
    home=str(Path.home())
    Path(home+"/.cache/buildaur/build").mkdir(parents=True, exist_ok=True)
    # colors
    yellow="\033[33;1m"
    red="\033[31;1m"
    thic="\033[1m"
    # config file
    proto="https"
    editor="nano"
    compmeth=".tar.zst"
    mode="normal"
    showPKGBUILD=1
    showDiff=0
    ask_warn_inst=0
    pcarg=""
    mkopts=""
    # configfile
    conf=open("/etc/buildaur/buildaur.conf").read()
    try:
        exec(conf)
    except:
        print(":: "+yellow+"Warning:\033[0m The config has errors in it.")
    # checking for root
    if home == "/root":
        print(":: "+red+"ERROR:\033[0m DON'T run this script as root, stupid!")
        exit(1)
    handle=Handle(".", "/var/lib/pacman")
    localdb=handle.get_localdb()
    # args
    args=sys.argv
    black=open("/usr/share/buildaur/blacklist").read().split("\n")
    # checking if args are given
    if len(args) == 1:
        print(":: "+red+"ERROR:\033[0m No options given!")
        exit(1)
    # args
    if args[1][:4] == "-Syu":
        options(args[1], 4)
        update()
    elif args[1][:6] == "-aspyu":
        options(args[1], 6)
        mode="asp"
        update()
    elif args[1] in ["-Q", "-Qq", "-Qqq"]:
        pkgs=args
        arg=args[1]
        del pkgs[0:2]
        if len(pkgs) == 0:
            pkgs=os.popen("pacman -Qqm").read().split('\n')
        if "qq" in arg:
            resolve(pkgs, "multiinfo", True)
        else:
            resolve(pkgs, "multiinfo", False)
        if arg == "-Q":
            infoout(resolve.res, False)
        elif arg in ["-Qq", "-Qqq"]:
            infoout(resolve.res, True)
    elif args[1] in ["-Qs", "-Qsq", "-Qsqq"]:
        pkgs=args
        arg=args[1]
        del pkgs[0:2]
        if "qq" in arg:
            resolve(pkgs, "search", True)
        else:
            resolve(pkgs, "search", False)
        if arg == "-Qs":
            infoout(resolve.res, False)
        elif arg in  ["-Qsq", "-Qsqq"]:
            infoout(resolve.res, True)
    elif args[1][:2] == "-S":
        options(args[1], 2)
        pkgs=args
        del pkgs[0:2]
        if len(pkgs) == 0:
            print(":: "+red+"ERROR:\033[0m No packages given!")
            exit(1)
        install(pkgs)
    elif args[1][:4] == "-asp":
        options(args[1], 4)
        pkgs=args
        del pkgs[0:2]
        if len(pkgs) == 0:
            print(":: "+red+"ERROR:\033[0m No packages given!")
            exit(1)
        mode="asp"
        install(pkgs)
    elif args[1] == "-h" or args[1] == "--help":
        help()
    elif args[1] == "--about":
        about()
    elif args[1] == "--clear":
        print(":: Cleaning builddir...")
        print(" "+os.popen("echo $(du -hcs ~/.cache/buildaur/build | xargs | awk {'print $1'})").read().split("\n")[0]+"B will be removed!")
        os.system("rm -rf ~/.cache/buildaur/build/*")
        print(":: Done!")
    elif args[1] == "--make-chroot":
        print(":: Creating a chrootdir")
        os.system('sudo rm -rf ~/chroot 2>/dev/null; mkdir ~/chroot; export CHROOT=$HOME/chroot; mkarchroot $CHROOT/root base-devel; echo "export CHROOT=$HOME/chroot" >> $HOME/.bashrc; exit 0')
    elif args[1] == "--listhooks":
        list_hooks()
    elif args[1] == "--hook-activate":
        hooks=[]
        if args[2] == "all":
            hooks+=os.listdir("/etc/buildaur/hooks")
        else:
            hooks=args[2:]
        hook_activate(hooks)
    elif args[1] == "--hook-deactivate":
        hooks=[]
        if args[2] == "all":
            hooktypes=["prehooks", "posthooks", "prerunhooks", "postrunhooks"]
            for hookdir in hooktypes:
                hooks+=os.listdir("/etc/buildaur/"+hookdir)
        else:
            hooks=args[2:]
        hook_deactivate(hooks)
    elif args[1] in ["--license", "-l"]:
        print(open("/usr/share/licenses/buildaur/LICENSE").read())
    elif args[1] in ["--version", "-v"]:
        pkg=localdb.get_pkg("buildaur")
        print(pkg.version)
    elif args[1] == "--show":
        try:
            secarg=args[2]
        except:
            print(":: "+red+"ERROR:\033[0m No package or other option is given!")
            exit(1)
        pkgs=args
        arg=args[1]
        if secarg == "--diff":
            del pkgs[0:3]
            if len(pkgs) == 0:
                print(":: "+red+"ERROR:\033[0m No package given!")
                exit(1)
        else:
            del pkgs[0:2]
        resolve(pkgs,"multiinfo", True)
        info(resolve.res, True)
        for i in range(int(info.rescount)):
            os.chdir(home+"/.cache/buildaur/build")
            exec("infoout.out=info.array_"+str(i))
            pkgname=infoout.out[0]
            os.system("rm -rf ./"+pkgname+" 2>/dev/null; git clone "+proto+"://aur.archlinux.org/"+pkgname+" 2>/dev/null")
            os.chdir(os.getcwd()+"/"+pkgname)
            if secarg == "--diff":
                os.system('git diff $(git log --pretty=format:"%h" | head -2 | xargs)')
            else:
                pkgbuild = open("PKGBUILD", "rt").read()
                print(pkgbuild)
    else:
        print(":: "+red+"ERROR:\033[0m "+args[1]+" is no valid option!")
