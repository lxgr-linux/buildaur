#!/usr/bin/bash
# This script can be used to genrate an complete list of all packages which are awailable from the AUR
# This is not included in the baseinstall and is just for testing purposes

for i in {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}
do
	echo $i
	buildaur.py -Qsqq $i
done
