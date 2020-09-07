#!/usr/bin/env bash

. ./PKGBUILD

if [[ $1 = deps ]]
then
echo ${depends[@]} ${makedepends[@]}
elif [[ $1 = vers ]]
then
  if [[ $epoch != "" ]] && [[ $epoch != 0 ]]
  then
    epoch=${epoch}:
  else
    epoch=""
  fi
  echo "${epoch}$pkgver-$pkgrel"
elif [[ $1 = arch ]]
then
  echo $arch
elif [[ $1 = pkgname ]]
then
  echo ${pkgname[@]}
fi
