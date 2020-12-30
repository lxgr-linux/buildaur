#!/usr/bin/env python3

from buildaur import *

def branch(pkgs):
    alldeps=[]
    for pkg in pkgs:
        alldeps.append(deps(pkg))
    for pkg in alldeps:
        alldeps+=branch(pkg)
    return alldeps
