# Buildaur -- An AUR helper
by LXGR <lxgr@protonmail.com>

# Introduction

An AUR helper? what's that? And what's the AUR in general?
The AUR is an software repository for archlinux users and theyr self created or packaged software which is not in an official repository. There the packages are not stored traditionaly as packages, like in an normal software repository. They are stored as 'PKGBUILD's which are used in an makeprocess to create and install the package it self.
An AUR helper is an program which makes this job for you, just like a normal packagemanager like pacman.
Buildaur is one of those.
https://wiki.archlinux.org/index.php/Arch_User_Repository

# Installation

First the 'PKHBUILD' should be cloned from the AUR

$ git clone https://aur.archlinux.org/buildaur.git

Then the package has to be build and installed

$ cd ./buildaur
$ makepkg -si

Then the installation will be finished.

# Usage

Like most other shell programs buildaur has some options which can be used to specify what the program should exactly do:

Usage: /usr/bin/buildaur <option> <string>
   General options:
      -S                : Installs a package
      -R                : Removes a package
      -Q                : Lists installed packages or searches for ones in the AUR
      -Qs               : Search the AUR
      -Syu              : Updates all AUR packages
      -asp              : Builds a package from source using asp (suefull for archlinux arm)
      --clear           : Cleanes build dir
      -v|--version      : Displays version of this program
      -l|--license      : Displays license of this program

   Additional options for -S,-R,-Syu,-asp:
      n                 : Doesn't ask questions

   Hookoptions:
      --listhooks       : Lists all available and installed hooks
      --hook-activate   : Activates a hook
      --hook-deactivate : Deactivates a hook

   Help options:
      -h|--help         : Displays this help-dialog
      --help-hooks      : Displays help-dialog for hooks

Examples:
    buildaur -S cava    : Installes the package 'cava'
    buildaur -Sn cava   : Installes 'cava' without anking any questions
    buildaur -Syu       : Updates all packages which were instaleld from the AUR

# Special options

-asp:
  The '-asp' option has in the first case nothing todo with the AUR itself it's more a fuction which is very important for Archlinux ARM.
  It builds a specified package which may or may not be in the official Archlinux ARM repository, but is in the one for x86_64, completly from source and installes it. This is usefull because some packages are not already ported to ARM but may work.

hooks:
  Hooks are skripts that run before and after the packagebuild.
  They are made to for example modify the PKGBUILD
  All hooks are stored in /etc/buildaur/hooks
  In /etc/buildaur/prehooks are the hooks stored wich run before the packagebuild
  and in /etc/buildaur/posthooks those wich run after the packagebuild.
  A hook always contains a 'type' (pre oder post) and a 'desc' variable.
  It also contains an if-function wich contains the modifications for the PKGBUILD and so on
  See /etc/buildaur/prehooks/1-arm-archfix as an example.

  Hookoptions:
     --listhooks       : Lists all available and installed hooks
     --hook-activate   : Activates a hook
     --hook-deactivate : Deactivates a hook
