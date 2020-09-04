#!/usr/bin/env python3
# maintainer lxgr <lxgr@protonmail.com>
# WARNING: This is experimental code!

import os
import progressbar_buildaur as progressbar
import time
import requests
import sys

#global home
home=os.getcwd()

#colors
yellow="\033[33;1m"
red="\033[31;1m"
thic="\033[1m"
# config file
proto="https"
editor="nano"
compmeth=".tar.zst"
conf=open("/etc/buildaur/buildaur.conf").read()
try:
    exec(conf)
except:
    print(":: "+yellow+"Warning:\033[0m The config has errors in it.")

# args
args=sys.argv

# res=os.popen("cat /usr/share/buildaur/res").read()

def options(string):
    global mkopts
    mkopts=""
    options.confirm=True
    options.install=True
    options.color=True
    if string.find("n") != -1:
        options.confirm=False
    if string.find("di") != -1:
        options.install=False
    if string.find("co") != -1:
        global yellow
        global red
        global thic
        mkopts=mkopts+" -m"
        yellow=""
        red=""
        thic=""
    if string.find("spgp") != -1:
        mkopts=mkopts+" --skippgpcheck"

def resolve(pkgs, quiet):
    if quiet == False:
        print(":: Downloading packagelist...")
    url=proto+"://aur.archlinux.org/rpc/?v=5&type=multiinfo"
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
        try:
            localver=os.popen("pacman -Qqi "+pkgname+" 2>/dev/null").read().split("\n")[1].split(" ")[19]
        except:
            localver="---"
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
    resolve(pkgs, False)
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
            msg.append(" "+yellow+"Warning:\033[0m "+pkgname+"-"+localver+" is higher than AUR "+pkgver+"!")
        if pkgoutdate != ":null,":
            msg.append(" "+yellow+"Warning:\033[0m "+pkgname+" is flagged as out-of-date!")
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
    pkgsout=[]
    install=[]
    pcarg=""
    resolve(pkgs, False)
    print(":: Checking packages...")
    info(resolve.res, True)
    # Check if package is realy in AUR
    for i in range(int(info.rescount)):
        exec("update.out=info.array_"+str(i))
        pkgsout.append(update.out[0])
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
        elif sorted([pkgver, localver])[0] == localver:
            print(" "+thic+"Info:\033[0m "+pkgname+"-"+localver+" will be updated to "+pkgver)
        elif sorted([pkgver, localver])[0] == pkgver:
            print(" "+yellow+"Warning:\033[0m "+pkgname+"-"+localver+" is higher than AUR "+pkgver+"!")
        if pkgoutdate != ":null,":
            print(" "+yellow+"Warning:\033[0m "+pkgname+" is flagged as out-of-date!")
        install.append(i)
    # asking to continue
    print("")
    print("Packages ("+info.rescount+"): ", end='')
    for pkg in install:
        exec("update.out=info.array_"+str(pkg))
        pkgname=update.out[0]
        print(pkgname+" ", end='')
    print("")
    if options.confirm:
        ask=input("\n:: Continnue installation? [Y/n] ")
    else:
        ask="y"
    if (ask == "Y") or (ask == "y") or (ask == ""):
        print("")
        # home=os.getcwd()
        count=1
        for pkg in install:
            # full makeprocess
            # vars
            exec("update.out=info.array_"+str(pkg))
            pkgname=update.out[0]
            pkgver=update.out[1]
            print("("+str(count)+"/"+info.rescount+") Making package "+thic+pkgname+"\033[0m...")
            # Git repository
            os.chdir(home+"/.cache/buildaur/build")
            print(":: Cloning git repository...")
            os.system("rm -rf ./"+pkgname+" 2>/dev/null; git clone "+proto+"://aur.archlinux.org/"+pkgname)
            os.chdir(os.getcwd()+"/"+pkgname)
            # edit
            print(":: Printing PKGBUILD...")
            pkgbuild = open("PKGBUILD", "rt").read()
            print("\033[37m"+str(pkgbuild)+"\033[0m")
            if options.confirm:
                ask=input("\n:: Edit PKGBUILD? [y/N] ")
            else:
                ask="n"
            if (ask == "y") or (ask == "Y"):
                os.system(editor+" ./PKGBUILD")
                print(":: Going on")
            # Hooks
            hooks("prehooks")
            # depends
            depts()
            # makepkg
            print(":: Making the package...")
            os.system(" PKGEXT='.pkg"+compmeth+"' makepkg -s "+mkopts)
            # Hooks
            hooks("posthooks")
            # Defining pkgpath
            if os.popen('. ./PKGBUILD ; echo $arch').read().split('\n')[0] == "any":
                arch='any'
            else:
                arch=os.popen('uname -m').read().split('\n')[0]
            pkgpathes.append(os.getcwd()+"/"+pkgname+"-"+os.popen('. ./PKGBUILD ;if [[ $epoch != "" ]] && [[ $epoch != 0 ]]; then epoch=${epoch}: ;else epoch="" ;fi; echo "${epoch}$pkgver-$pkgrel"').read().split('\n')[0]+"-"+arch+".pkg"+compmeth)
            os.chdir(home)
            count=count+1
            print("")
        # installing packages
        if options.install:
            print(":: Installing packages...")
            inststring=""
            for path in pkgpathes:
                inststring=inststring+path+" "
            if options.confirm == False:
                pcarg=pcarg+" --noconfirm"
            os.system("sudo pacman -U "+pcarg+" "+inststring)
        else:
            print(":: Package(s) created in:")
            for path in pkgpathes:
                print(" "+path)
    else:
        exit()
# exec("out=info.array_1")
# print(out)
#
#
# pkgs=["brave-bin", "inxi"]
# resolve(pkgs)
# update()

def depts():
    list=""
    nedeps=[]
    neaurdeps=[]
    print(":: Checking for unresolved dependencies...")
    depends=os.popen(". ./PKGBUILD; echo ${depends[@]}").read().split("\n")[0].split(" ")
    for pkg in depends:
        list=list+" "+pkg
    instadepends=os.popen("pacman -Qq "+list+" 2>/dev/null").read().split("\n")
    del instadepends[-1]
    for pkg in depends:
        if pkg in instadepends:
            print("", end="")
        else:
            nedeps.append(pkg)
    resolve(nedeps, True)
    info(resolve.res, True)
    if int(info.rescount) != 0:
        for i in range(int(info.rescount)):
            exec("infoout.out=info.array_"+str(i))
            neaurdeps.append(infoout.out[0])
        curdir=os.getcwd()
        os.chdir(home)
        install(neaurdeps)
        os.chdir(curdir)

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
    print(":: "+red+"ERROR:\033[0m No options given!")
    exit(1)

if args[1][:4] == "-Syu":
    options(args[1])
    update()
elif args[1] == "-Q" or args[1] == "-Qq":
    pkgs=args
    arg=args[1]
    del pkgs[0:2]
    if len(pkgs) == 0:
        pkgs=os.popen("pacman -Qqm").read().split('\n')
    resolve(pkgs, False)
    if arg == "-Q":
        infoout(resolve.res, False)
    else:
        infoout(resolve.res, True)
elif args[1][:2] == "-S":
    options(args[1])
    pkgs=args
    del pkgs[0:2]
    if len(pkgs) == 0:
        print(":: "+red+"ERROR:\033[0m No packages given!")
        exit(1)
    install(pkgs)
elif args[1] == "-h" or args[1] == "--help":
    help()
else:
    print(":: "+red+"ERROR:\033[0m "+args[1]+" is no valid option!")
