# Buildaur -- An AUR helper
by LXGR <lxgr@protonmail.com>

# Introduction

An AUR helper? what's that? And what's the AUR in general?
The AUR is an software repository for archlinux users and their self created or packaged software which is not in an official repository. There the packages are not stored traditionaly as packages, like in a normal software repository. They are stored as 'PKGBUILD's which are used in a makeprocess to create and install the package itself.
An AUR helper is an program which does this job for you, just like a normal package manager like pacman.
Buildaur is one of those.
https://wiki.archlinux.org/index.php/Arch_User_Repository

# Installation

First the 'PKGBUILD' should be cloned from the AUR
```shell
$ git clone https://aur.archlinux.org/buildaur.git
```
Then the package has to be build and installed
```shell
$ cd ./buildaur
$ makepkg -si
```
Then the installation will be finished.

NOTE: If you are using manjaro linux and want to use the asp functionality of buildaur, you have to install asp, which is not in the manjaro repositorys.
To do this just clone asps git repo:
```shell
$ git clone https://aur.archlinux.org/asp.git
```
Then the package has to be build and installed
```shell
$ cd ./asp
$ makepkg -si
```
# Usage

Like most other shell programs buildaur has some options which can be used to specify what the program should exactly do:

buildaur - An AUR helper with asp support<br>
Usage: /usr/bin/buildaur <option> <string><br>
   General options:<br>
      -S                : Installs a package<br>
      -Q                : Lists installed packages or searches for ones in the AUR<br>
      -Qs               : Search the AUR<br>
      -Qi               : Gives detailed package information<br>
      -Syu              : Updates all AUR packages<br>
      -asp              : Builds a package from source using asp (usefull for archlinux arm)<br>
      -aspyu            : Updates all asp packages (usefull for archlinux arm)<br>
      --show            : Shows the PKGBUILD of a given package<br>
      --clear           : Cleanes build dir<br>
      -v|--version      : Displays version of this program<br>
      -l|--license      : Displays license of this program<br>
      --make-chroot     : Creates a chroot dir which can be used for building packages<br>
      --about           : Displays an about text<br>
<br>
   Additional options for -S,-R,-Syu,-asp,-aspyu:<br>
      n                 : Doesn't ask questions<br>
      spgp              : Skips pgp checks of sourcecode<br>
      ch                : Builds the package in a clean chroot (you may run into some problems using this on archlinux arm!)<br>
      di                : Just builds the package<br>
      co                : Toggles colored output on and off<br>
      dlf               : Pulls dependencies from PKGBUILD<br>
      git               : Updates all -git packages at updates<br>
<br>
<br>
   Additional options for --show:<br>
      --diff            : Outputs diff between current pkgbuildver and former pkgbuildver<br>
<br>
   Additional options for -Q,-Qs<br>
      q                 : Just outputs pknames and vers<br>
      qq                : JUST outputs pknames<br>
      --by              : Defines the value that should be searched by (values: name name-desc maintainer depends makedepends optdepends checkdepends)<br>
<br>
   Hookoptions:<br>
      --listhooks       : Lists all available and installed hooks<br>
      --hook-activate   : Activates a hook<br>
      --hook-deactivate : Deactivates a hook<br>
<br>
   Help options:<br>
      -h|--help         : Displays this help-dialog<br>
<br>

Examples:<br>
    buildaur -S cava    : Installes the package 'cava'<br>
    buildaur -Sn cava   : Installes 'cava' without asking any questions<br>
    buildaur -Syu       : Updates all packages which were installed from the AUR<br>

# Special options

-asp:
  The '-asp' option has in the first case nothing to do with the AUR itself, it's rather a fuction which is very important for Archlinux ARM.
  It builds a specified package, which may or may not be in the official Archlinux ARM repository, but is in the one for x86_64, completly from the source and installes it. This is usefull because some packages are not yet ported to ARM but may work.

hooks:
  Pre- and post-hooks are skripts that run before and after the package building.
  They are made to, for example modify the PKGBUILD.
  Pre- and post-run-hooks are skripts that run before the installation itself to fix dependency issues etc.
  All hooks are stored in /etc/buildaur/hooks.
  In /etc/buildaur/prehooks are the hooks stored wich run before the package building
  and in /etc/buildaur/posthooks those which run after the packagebuild.
  A hook always contains a 'type' (pre, post, prerun or postrun) and a 'desc' variable.
  It also contains an if-function which contains the modifications for the PKGBUILD etc.
  See /etc/buildaur/prehooks/1-arm-archfix as an example.

  Hookoptions:<br>
     --listhooks       : Lists all available and installed hooks<br>
     --hook-activate   : Activates a hook<br>
     --hook-deactivate : Deactivates a hook<br><br>
     When 'all' is given as argument for --hook-activate and --hook-deactivate the action applies to all hooks.

# Config file

The config file for buildaur is ' /etc/buildaur/buildaur.conf'. It can be used to set variables which appear in buildaur, like 'ask', 'pgp' and 'buildchroot'. It can also contain code that should be integrated into buildaur.

Available variables:
- yellow="\033[33;1m" # Color yellow
- red="\033[31;1m" # Color red
- thic="\033[1m" # Bold text
- proto="https" # Protocol to be used at downloads
- editor="nano" # Editor to edit PKGBUILD
- compmeth=".tar.zst" # Compression method of package
- mode="normal" # Default mode
- showPKGBUILD=1 # Print out PKGBUILD before build process
- showDiff=0 # Print out diffs between former and current PKGBUILD version before build process
- ask_warn_inst=0 # Ask to update packages which are higher than AUR
- pcarg="" # Default arguments for pacman
- mkopts="" # Default arguments for makepkg
- replace_deps={"vte" : "vte-legacy"} # Items in dependency which should be replaced with another one

Bash only options:
- sudoreset=1 # Reset sudo before PKGBUILD
- layout="new" # Old or new look of buildaur
- color="true" # Toggels colored output

# Blacklist

The blacklist stored in /usr/share/buildaur/blacklist contains package names which are excluded in updates.

# Bash version

There are two versions of this script, one is written in bash (buildaur.sh) and one in python (buildaur). The bash version was the former standart but was replaced in version 42.0.7.7 and is not longer in development.
