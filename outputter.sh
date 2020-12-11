#!/usr/bin/env bash

if [[ $1 = asp ]]
then
  pkgout="$(asp show $2 2>/dev/null)"
  echo "$pkgout" > ./PKGBUILD
fi
. ./PKGBUILD 2>/dev/null
atributes=("'pkgnames'" "'arch'" "'deps'" "'makedeps'")
arrays=("pkgname[@]" "arch[@]" "depends[@]" "makedepends[@]")
out="{"
if [[ $epoch != "" ]] && [[ $epoch != 0 ]]
then
  epoch+=:
else
  epoch=""
fi
for ((i=0; i<${#arrays[*]}; i++))
do
  out+="${atributes[$i]} : ["
  arr=${arrays[$i]}
  for j in ${!arr}
  do
    out+="'$j', "
  done
  out+="], "
done
out+=" 'ver' : '${epoch}$pkgver-$pkgrel'}"
echo $out
if [[ $1 = asp ]]
then
  rm ./PKGBUILD
fi
