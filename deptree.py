#!/usr/bin/env python3

from buildaur import *

def branch(pkgs):
    alldeps=[]
    if len(pkgs) != 0:
        alldeps.append(deps(pkgs, do_install=False, quiet=True))
    if len(alldeps) != 0:
        alldeps+=branch(alldeps[0])
    return alldeps

def main(names):
    rescount, cutted=info(resolve(names))
    for i in range(rescount):
        pkg=Package(cutted, i)
        # print(names[i], end="")
        ret=[arr for arr in branch([pkg]) if len(arr) != 0]
        ret.reverse()
        print(ret)
        for arr in ret:
            for pkg in arr:
                print(pkg.name)

if __name__ == "__main__":
    main(["gtkdialog"])
