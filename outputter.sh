#!/usr/bin/env bash

if [[ $1 = deps ]]
then
  . ./PKGBUILD
  echo ${depends[@]} ${makedepends[@]}
elif [[ $1 = vers ]]
then
  . ./PKGBUILD
  if [[ $epoch != "" ]] && [[ $epoch != 0 ]]
  then
    epoch=${epoch}:
  else
    epoch=""
  fi
  echo "${epoch}$pkgver-$pkgrel"
elif [[ $1 = asp ]]
then
  out=$(asp show $2 2>/dev/null)
  if [[ $? != 0 ]]
  then
    echo "error"
    exit
  fi
  epoch=0
  declare $(echo "$out" | egrep pkgver | head -1)
	declare $(echo "$out" | egrep pkgrel | head -1)
  declare $(echo "$out" | egrep epoch | head -1) >/dev/null
  if [[ $epoch != "" ]] && [[ $epoch != 0 ]]
  then
    epoch=${epoch}:
  else
    epoch=""
  fi
  echo "${epoch}$pkgver-$pkgrel"
elif [[ $1 = arch ]]
then
  . ./PKGBUILD
  echo $arch
elif [[ $1 = pkgname ]]
then
  . ./PKGBUILD
  echo ${pkgname[@]}
elif [[ $1 = "all" ]]
then
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
fi
