#!/usr/bin/env bash

if [[ $1 = asp ]]
then
  pkgout="$(asp show $2 2>/dev/null)"
  echo "$pkgout" > ./PKGBUILD
fi
. ./PKGBUILD
out="{'pkgnames' : ["
for name in ${pkgname[@]}
do
  out+="'$name', "
done
out+="], 'arch' : ["
for arc in ${arch[@]}
do
  out+="'$arc', "
done
out+="],"
if [[ $epoch != "" ]] && [[ $epoch != 0 ]]
then
  epoch=${epoch}:
else
  epoch=""
fi
out+=" 'ver' : '${epoch}$pkgver-$pkgrel', 'deps' : ["
for dep in ${depends[@]}
do
  out+="'$dep', "
done
out+="], 'makedeps' : ["
for dep in ${makedepends[@]}
do
  out+="'$dep', "
done
out+="]}"
echo $out
if [[ $1 = asp ]]
then
  rm ./PKGBUILD
fi
