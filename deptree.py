#!/usr/bin/env python3

from buildaur import *

def branch(pkgs):
    alldeps=[]
    for pkg in pkgs:
        alldeps+=deps(pkg, do_install=False, quiet=True)
    if len(alldeps) != 0:
        alldeps+=branch(alldeps)
    return alldeps

def main(names):
    rescount, cutted=info(resolve(names))
    for i in range(rescount):
        pkg=Informer(cutted, i)
        for pkg in branch([pkg]):
            print(pkg.name, end=" ")
    print("")

if __name__ == "__main__":
    main(["python2-wnck"])
