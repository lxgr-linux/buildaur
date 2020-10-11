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
from datetime import datetime
import math
import json
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

def liner(length, names, sep=""):
    width, height = os.get_terminal_size()
    lens=0
    for name in names:
        if lens+len(name)+2 < width-length:
            print(name+"  ", end="")
            lens+=len(name)+2
        else:
            lens=len(name)+2
            print("\n"+(length-len(sep))*" "+sep+name+"  ", end="")
    print("")

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

def resolve(pkgs, type="multiinfo", quiet=False, searchby="name"):
    pkgss=[]
    resolve.res=[]
    # cut pkglists in 200 pkgs bytes
    for i in range(math.ceil(len(pkgs)/200+1)):
        pkgss.append(pkgs[(i*200)-200:i*200])
    del pkgss[0]
    if quiet == False:
        print(":: Downloading packagelist...")
    for pkgs in pkgss:
        url=proto+"://aur.archlinux.org/rpc/?v=5&type="+type
        if len(pkgs) == 0:
            exit()
        if type == "search":
            url+="&by="+searchby+"&arg="+pkgs[0]
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
        resolve.res.append(str(r.content))

def info(ress, quiet=False):
    rescount=0
    cutted=[]
    info.respkgs=[]
    for res in ress:
        y=json.loads(res.split("b'")[1].split("'")[0])
        rescount+=int(y["resultcount"])
        cutted+=y["results"]
    #print(cutted)
    for i in range(rescount):
        for sname in ["Name", "Version", "URL", "Description", "Maintainer", "FirstSubmitted", "OutOfDate", "LastModified", "Popularity", "NumVotes"]:
            try:
                exec("info."+sname+"='"+str(cutted[i][sname])+"'")
            except:
                exec("info."+sname+"='None'")
        for sname in ["Depends", "MakeDepends", "OptDepends", "License", "Keywords"]:
            try:
                exec("info."+sname+"="+str(cutted[i][sname]))
            except:
                exec("info."+sname+"=['None']")
        # Filtering "\" from URL
        if "\\/" in info.URL:
            newURL=""
            for n in range(len(info.URL)):
                if info.URL[n] == '\\' and info.URL[n+1] == '\\' and info.URL[n+2] == "/":
                    newURL+=""
                elif info.URL[n] != "\\":
                    newURL+=info.URL[n]
            info.URL=newURL
        try:
            pkg=localdb.get_pkg(info.Name)
            localver=pkg.version
        except:
            localver="---"
        array=[info.Name, info.Version, localver, info.OutOfDate, info.Description, info.Depends, info.MakeDepends, info.OptDepends, info.License, info.URL, info.Maintainer, info.FirstSubmitted, info.LastModified, info.Popularity, info.NumVotes, info.Keywords]
        exec("info.array_"+str(i)+"=array")
        info.respkgs.append(info.Name)
        if quiet == False:
            progressbar.progress(i+1, int(rescount), "Collecting "+info.Name+"...")
    info.rescount=rescount

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
        pkgoutdate="null"
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
    resolve(pkgs)
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
        pkg=informer(i)
        progressbar.progress(i+1, int(info.rescount), "Checking "+pkg.name()+"...")
        if pkg.ver() == pkg.localver() or pkg.name() in black:
            print("", end="")
        elif sorter(pkg.ver(), pkg.localver()) == pkg.ver():
            update.willinst.append(pkg.name())
        elif sorter(pkg.ver(), pkg.localver()) == pkg.localver():
            msg.append(" "+yellow+"Warning:\033[0m "+pkg.name()+"-"+pkg.localver()+" is higher than AUR "+pkg.ver()+"!")
            if ask_warn_inst == 1:
                update.willinst.append(pkg.name())
        if pkg.outdate() != "None":
            msg.append(" "+yellow+"Warning:\033[0m "+pkg.name()+" is flagged as out-of-date since: "+datetime.utcfromtimestamp(int(pkg.outdate())).strftime('%Y-%m-%d %H:%M:%S')+"!")
    print(":: Done")
    for i in msg:
        print(i)
    if update.willinst == []:
        print(" Nothing to do")
    else:
        install(update.willinst)

class informer():
    def __init__(self, pkg, type="by_num"):
        if type == "by_num":
            exec("informer.out=info.array_"+str(pkg))
            self.num=pkg
        elif type == "by_name":
            for i in range(int(info.rescount)):
                self.num=i
                exec("informer.out=info.array_"+str(i))
                if informer.out[0] == pkg:
                    break
    def ver(self):
        return informer.out[1]
    def localver(self):
        return informer.out[2]
    def name(self):
        return informer.out[0]
    def outdate(self):
        return informer.out[3]
    def desc(self):
        return informer.out[4]
    def depends(self):
        return informer.out[5]
    def makedepends(self):
        return informer.out[6]
    def optdepends(self):
        return informer.out[7]
    def license(self):
        return informer.out[8]
    def url(self):
        return informer.out[9]
    def maintainer(self):
        return informer.out[10]
    def submitted(self):
        return informer.out[11]
    def modified(self):
        return informer.out[12]
    def popularity(self):
        return informer.out[13]
    def votes(self):
        return informer.out[14]
    def keywords(self):
        if informer.out[15] == []:
            return ["null"]
        else:
            return informer.out[15]

def infoout(res, quiet=False, veryquiet=False):
    info(res, True)
    for i in range(int(info.rescount)):
        pkg=informer(i)
        if veryquiet:
            print(pkg.name())
        elif quiet:
            print(pkg.name(), pkg.ver())
        else:
            print(" "+pkg.name()+"-"+pkg.ver()+" (local: "+pkg.localver()+")")
            print("    "+pkg.desc())

def detailinfo(res):
    info(res, True)
    for i in range(int(info.rescount)):
        pkg=informer(i)
        print("Name                  : "+pkg.name())
        print("Version               : "+pkg.ver())
        print("Local Version         : "+pkg.localver())
        print("Description           : "+pkg.desc())
        print("Maintainer            : "+pkg.maintainer())
        print("URL                   : "+pkg.url())
        print("Licenses              : ", end='')
        liner(24, pkg.license())
        print("First submitted       : "+datetime.utcfromtimestamp(int(pkg.submitted())).strftime('%Y-%m-%d %H:%M:%S'))
        print("Last modified         : "+datetime.utcfromtimestamp(int(pkg.modified())).strftime('%Y-%m-%d %H:%M:%S'))
        print("Popularity            : "+pkg.popularity())
        print("Votes                 : "+pkg.votes())
        print("Keywords              : ", end='')
        liner(24, pkg.keywords())
        print("Pkg out-of-date       : ", end='')
        if pkg.outdate() == 'None':
            print(pkg.outdate())
        else:
            print(datetime.utcfromtimestamp(int(pkg.outdate())).strftime('%Y-%m-%d %H:%M:%S'))
        print("Dependencies          : ", end='')
        liner(24, pkg.depends())
        print("Makedependencies      : ", end='')
        liner(24, pkg.makedepends())
        print("Optional Dependencies : ", end='')
        liner(24, pkg.optdepends())
        print("")

def install(pkgs):
    pkgpathes=[]
    pkgsout=[]
    install=[]
    nums=[]
    try:
        # Looking if pkgs are already in res
        for pkg in pkgs:
            ipkg=informer(pkg, type="by_name")
            nums.append(ipkg.num)
    except:
        if mode == "asp":
            aspinfo(pkgs, True)
        else:
            resolve(pkgs)
            info(resolve.res, True)
        nums=range(int(info.rescount))
    print(":: Checking packages...")
    if len(nums) == "0":
        print(" Nothing to do")
        exit(0)
    # Checking packages for atributes
    for i in nums:
        pkg=informer(i)
        if pkg.ver() == pkg.localver():
            print(" "+thic+"Info:\033[0m "+pkg.name()+"-"+pkg.localver()+" is up to date -- reistalling")
        elif pkg.localver() == "---":
            print("", end="")
        elif sorter(pkg.ver(), pkg.localver()) == pkg.ver():
            print(" "+thic+"Info:\033[0m "+pkg.name()+"-"+pkg.localver()+" will be updated to "+pkg.ver())
        elif sorter(pkg.ver(), pkg.localver()) == pkg.localver():
            print(" "+yellow+"Warning:\033[0m "+pkg.name()+"-"+pkg.localver()+" is higher than AUR "+pkg.ver()+"!")
        if pkg.outdate() != "None":
            print(" "+yellow+"Warning:\033[0m "+pkg.name()+" is flagged as out-of-date since: "+datetime.utcfromtimestamp(int(pkg.outdate())).strftime('%Y-%m-%d %H:%M:%S')+"!")
        install.append(i)
        pkgsout.append(pkg.name())
    # Check if package is realy in AUR
    if len(pkgs) != len(pkgsout):
        for pkg in pkgs:
            if pkg not in pkgsout:
                print(":: "+red+"ERROR:\033[0m "+pkg+" not found!")
                exit(1)
    # asking to continue
    print("")
    print("Packages ("+str(len(nums))+"): ", end='')
    packs=[]
    for i in install:
         pkg=informer(i)
         packs.append(pkg.name()+"-"+pkg.ver())
    liner(len("Packages ("+str(len(nums))+"): "), packs)
    if options.confirm:
        ask=input("\n:: Continnue installation? [Y/n] ")
    else:
        ask="y"
    if ask == "Y" or ask == "y" or ask == "":
        print("")
        # home=os.getcwd()
        count=1
        max=str(len(nums))
        for pkg in install:
            # full makeprocess
            # vars
            ipkg=informer(pkg)
            print("("+str(count)+"/"+max+") Making package "+thic+ipkg.name()+"\033[0m...")
            # Git repository
            os.chdir(home+"/.cache/buildaur/build")
            if mode == "asp":
                print(":: Exporting package...")
                os.system('rm -rf ./'+ipkg.name()+' 2>/dev/null; asp export '+ipkg.name()+' 2>/dev/null')
            else:
                print(":: Cloning git repository...")
                os.system("rm -rf ./"+ipkg.name()+" 2>/dev/null;")
                while not os.path.exists("./"+ipkg.name()+"/PKGBUILD"):
                    os.system("git clone "+proto+"://aur.archlinux.org/"+ipkg.name())
            os.chdir(os.getcwd()+"/"+ipkg.name())
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
        resolve(nedeps, quiet=True)
        info(resolve.res, True)
        if int(info.rescount) != 0:
            for i in range(int(info.rescount)):
                pkg=informer(i)
                neaurdeps.append(pkg.name)
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
    print("      -Qi               : Gives detailed package information")
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
    print("")
    print("   Additional options for -Q,-Qs")
    print("      q                 : Just outputs pknames and vers")
    print("      qq                : JUST outputs pknames")
    print("      --by              : Defines the value that should be searched by (values: name name-desc maintainer depends makedepends optdepends checkdepends")
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
            resolve(pkgs, quiet=True)
        else:
            resolve(pkgs)
        if arg == "-Q":
            infoout(resolve.res)
        elif arg =="-Qq":
            infoout(resolve.res, quiet=True)
        elif arg =="-Qqq":
            infoout(resolve.res, veryquiet=True)
    elif args[1] in ["-Qs", "-Qsq", "-Qsqq"]:
        searchby="name"
        pkgs=args
        arg=args[1]
        try:
            secarg=args[2]
        except:
            exit()
        if secarg == "--by":
            searchby=args[3]
            if args[3] in ["name", "name-desc", "maintainer", "depends", "makedepends", "optdepends", "checkdepends"]:
                searchby=args[3]
            del pkgs[0:4]
        else:
            del pkgs[0:2]
        for pkg in pkgs:
            if "qq" in arg:
                resolve([pkg], type="search", searchby=searchby, quiet=True)
            else:
                resolve([pkg], type="search", searchby=searchby)
            if arg == "-Qs":
                infoout(resolve.res, False)
            elif arg =="-Qsq":
                infoout(resolve.res, quiet=True)
            elif arg =="-Qsqq":
                infoout(resolve.res, veryquiet=True)
    elif args[1] == "-Qi":
        pkgs=args
        arg=args[1]
        del pkgs[0:2]
        if len(pkgs) == 0:
            pkgs=os.popen("pacman -Qqm").read().split('\n')
        resolve(pkgs, quiet=True)
        detailinfo(resolve.res)
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
    elif args[1] in ["--test", "-t"]:
        resolve(["buildaur", "cava", "brave-bin"])
        json_test(resolve.res)
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
        resolve(pkgs, quiet=True)
        info(resolve.res, True)
        for i in range(int(info.rescount)):
            os.chdir(home+"/.cache/buildaur/build")
            pkg=informer(i)
            os.system("rm -rf ./"+pkg.name()+" 2>/dev/null; git clone "+proto+"://aur.archlinux.org/"+pkg.name()+" 2>/dev/null")
            os.chdir(os.getcwd()+"/"+pkg.name())
            if secarg == "--diff":
                os.system('git diff $(git log --pretty=format:"%h" | head -2 | xargs)')
            else:
                pkgbuild = open("PKGBUILD", "rt").read()
                print(pkgbuild)
    else:
        print(":: "+red+"ERROR:\033[0m "+args[1]+" is no valid option!")
