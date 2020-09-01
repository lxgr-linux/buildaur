#!/usr/bin/env python3
# maintainer lxgr <lxgr@protonmail.com>
# WARNING: This is experimental code!

import os
import progressbar_buildaur as progressbar
import time
import requests
import sys

args=sys.argv

# res=os.popen("cat /usr/share/buildaur/res").read()

def resolve(pkgs):
    print(":: Downloading packagelist...")
    url="https://aur.archlinux.org/rpc/?v=5&type=multiinfo"
    for pkg in pkgs:
        url=url+"&arg[]="+pkg
    r=requests.get(url)
    resolve.res=str(r.content)

def info(res, quiet):
    info.rescount=res.split('"')[8].split(":")[1].split(",")[0]
    cutted=res.split('{')
    if quiet == False:
        print(":: Collecting package data...")
    for i in range(int(info.rescount)):
        exec("global array_"+str(i))
        splitted=cutted[i+2].split('"')
        pkgname=splitted[5]
        pkgver=splitted[15]
        localver=os.popen("pacman -Qqi "+pkgname).read().split("\n")[1].split(" ")[19]
        pkgoutdate=splitted[30]
        pkgdesc=splitted[19]
        array=[pkgname, pkgver, localver, pkgoutdate, pkgdesc]
        if quiet == False:
            progressbar.progress(i+1, int(info.rescount), "Collecting "+pkgname+"...")
        exec("info.array_"+str(i)+"=array")

def update():
    msg=[]
    update.willinst=[]
    pkgs=os.popen("pacman -Qqm").read().split("\n")
    resolve(pkgs)
    info(resolve.res, False)
    print(":: Checking packages...")
    print(" "+info.rescount+" Packages found!", flush=True)
    print(":: Checking for outdated packages...")
    for i in range(int(info.rescount)):
        exec("update.out=info.array_"+str(i))
        pkgname=update.out[0]
        pkgver=update.out[1]
        localver=update.out[2]
        pkgoutdate=update.out[3]
        progressbar.progress(i+1, int(info.rescount), "Checking "+pkgname+"...")
        if pkgver == localver:
            print("", end="")
        elif sorted([pkgver, localver])[0] == localver:
            # msg.append(" \033[1mInfo:\033[0m "+pkgname+" is out of date!")
            update.willinst.append(pkgname)
        elif sorted([pkgver, localver])[0] == pkgver:
            msg.append(" \033[33;1mWarning:\033[0m "+pkgname+"-"+localver+" is higher than AUR "+pkgver+"!")
        if pkgoutdate != ":null,":
            msg.append(" \033[33;1mWarning:\033[0m "+pkgname+" is flagged as out-of-date!")
    print(":: Done")
    for i in msg:
        print(i)
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
    install=[]
    resolve(pkgs)
    print(":: Checking packages...")
    info(resolve.res, True)
    if info.rescount == 0:
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
            print(" \033[1mInfo:\033[0m "+pkgname+"-"+localver+" is up to date -- reistalling")
        elif sorted([pkgver, localver])[0] == localver:
            print(" \033[1mInfo:\033[0m "+pkgname+"-"+localver+" will be updated to "+pkgver)
        elif sorted([pkgver, localver])[0] == pkgver:
            print(" \033[33;1mWarning:\033[0m "+pkgname+"-"+localver+" is higher than AUR "+pkgver+"!")
        if pkgoutdate != ":null,":
            print(" \033[33;1mWarning:\033[0m "+pkgname+" is flagged as out-of-date!")
        install.append(i)
    # asking to continue
    print("")
    print("Packages ("+info.rescount+"): ", end='')
    for pkg in install:
        exec("update.out=info.array_"+str(pkg))
        pkgname=update.out[0]
        print(pkgname+" ", end='')
    print("")
    ask=input("\n:: Continnue installation? [Y/n] ")
    if (ask == "Y") or (ask == "y") or (ask == ""):
        print("")
        home=os.getcwd()
        count=1
        for pkg in install:
            # full makeprocess
            # vars
            exec("update.out=info.array_"+str(pkg))
            pkgname=update.out[0]
            pkgver=update.out[1]
            print("("+str(count)+"/"+info.rescount+") Making package \033[1m"+pkgname+"\033[0m...")
            # Git repository
            os.chdir(home+"/.cache/buildaur/build")
            print(":: Cloning git repository...")
            os.system("rm -rf ./"+pkgname+" 2>/dev/null; git clone https://aur.archlinux.org/"+pkgname)
            os.chdir(os.getcwd()+"/"+pkgname)
            # edit
            print(":: Printing PKGBUILD...")
            pkgbuild = open("PKGBUILD", "rt").read()
            print("\033[37m"+str(pkgbuild)+"\033[0m")
            ask=input("\n:: Edit PKGBUILD? [y/N] ")
            if (ask == "y") or (ask == "Y"):
                os.system("nano ./PKGBUILD")
                print(":: Going on")
            # Hooks
            hooks("prehooks")
            # makepkg
            print(":: Making the package...")
            os.system("makepkg -s")
            # Hooks
            hooks("posthooks")
            # Defining pkgpath
            if os.popen('. ./PKGBUILD ; echo $arch').read().split('\n')[0] == "any":
                arch='any'
            else:
                arch=os.popen('uname -m').read().split('\n')[0]
            pkgpathes.append(os.getcwd()+"/"+pkgname+"-"+os.popen('. ./PKGBUILD ;if [[ $epoch != "" ]] && [[ $epoch != 0 ]]; then epoch=${epoch}: ;else epoch="" ;fi; echo "${epoch}$pkgver-$pkgrel"').read().split('\n')[0]+"-"+arch+".pkg.tar.zst")
            os.chdir(home)
            count=count+1
            print("")
        # installing packages
        print(":: Installing packages...")
        inststring=""
        for path in pkgpathes:
            inststring=inststring+path+" "
        os.system("sudo pacman -U "+inststring)
    else:
        exit()
# exec("out=info.array_1")
# print(out)
#
#
# pkgs=["brave-bin", "inxi"]
# resolve(pkgs)
# update()

def help():
    print("buildaur - An AUR helper with asp support")
    print("Usage: "+args[0]+" <option> <string>")
    print("   General options:")
    print("      -S                : Installs a package")
    print("      -R                : Removes a package")
    print("      -Q                : Lists installed packages or searches for ones in the AUR")
    print("      -Qs               : Search the AUR")
    print("      -Syu              : Updates all AUR packages")
    print("      -url              : Installs a package from a given git-repository")
    print("      -asp              : Builds a package from source using asp (usefull for archlinux arm)")
    print("      --show            : Shows the PKGBUILD of a given package")
    print("      --clear           : Cleanes build dir")
    print("      -v|--version      : Displays version of this program")
    print("      -l|--license      : Displays license of this program")
    print("      --make-chroot     : Creates a chroot dir which can be used for building packages")
    print("      --about           : Displays an about text")
    print("")
    print("   Additional options for -S,-R,-Syu,-asp:")
    print("      n                 : Doesn't ask questions")
    print("      spgp              : Skips pgp checks of sourcecode")
    print("      ch                : Builds the package in a clean chroot (you may run into some problems using this on archlinux arm!)")
    print("      di                : Just builds the package")
    print("      co                : Toggles colored output on and off")
    print("")
    print("   Hookoptions:")
    print("      --listhooks       : Lists all available and installed hooks")
    print("      --hook-activate   : Activates a hook")
    print("      --hook-deactivate : Deactivates a hook")
    print("")
    print("   Help options:")
    print("      -h|--help         : Displays this help-dialog")
    print("      --help-hooks      : Displays help-dialog for hooks")

def hooks(type):
    hooks=os.popen("ls /etc/buildaur/"+type).read().split('\n')
    del hooks[-1]
    if len(hooks) > 0:
        print(":: Running "+type+"...")
        for hook in hooks:
            print(" "+hook+"...")
            os.system("/etc/buildaur/"+type+"/"+hook+" -u")

if len(args) == 1:
    print(":: \033[31;1mERROR:\033[0m No options given!")
    exit(1)

if args[1] == "-Syu":
    update()
elif args[1] == "-Q" or args[1] == "-Qq":
    pkgs=args
    arg=args[1]
    del pkgs[0:2]
    if len(pkgs) == 0:
        pkgs=os.popen("pacman -Qqm").read().split('\n')
    resolve(pkgs)
    if arg == "-Q":
        infoout(resolve.res, False)
    else:
        infoout(resolve.res, True)
elif args[1] == "-S":
    pkgs=args
    del pkgs[0:2]
    if len(pkgs) == 0:
        print(":: \033[31;1mERROR:\033[0m No packages given!")
        exit(1)
    install(pkgs)
elif args[1] == "-h" or args[1] == "--help":
    help()
