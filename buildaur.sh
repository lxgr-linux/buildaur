#!/usr/bin/env bash
# maintainer lxgr <lxgr@protonmail.com>
# Warning this code may be unstable

editor=nano
showPKGBUILD=1
sudoreset=1
ask_warn_inst=1
layout=new
color=true
proto=https
. /etc/buildaur/buildaur.conf
black="$(cat /usr/share/buildaur/blacklist)"
# asp set-git-protocol $proto

colorer(){
	if [[ $color = true ]]
	then
		bold=$(tput bold)
		red=$(tput setaf 1)
		grey=$(tput setaf 7)
		yellow=$(tput setaf 11)
		normal=$(tput sgr0)
		colored=
	else
		bold=
		red=
		grey=
		yellow=
		normal=
		colored=--nocolor
	fi
}

colorer

if [[ $(whoami) = root ]]
then
	echo ":: ${red}${bold}ERROR:${normal} Don't run this script as root!"
	exit 1
fi

progress(){
	python3 -c "import os; import math; max=$2; i=$1; width, height = os.get_terminal_size(); string=' $3'+200*' ';pl=round(math.log(width/57 ,1.01644658));  print('\r('+(len(str(max))-len(str(i)))*' '+str(i)+'/'+str(max)+')'+string[:width-16+(6-2*len(str(max)))-pl]+'['+round((i/max)*pl)*'#'+(pl-round((i/max)*pl))*'-'+'] '+(3-len(str(round((i/max)*100))))*' '+str(round((i/max)*100))+'%', end='', flush=True)"
}

options(){
	installindex=i
	if [[ $(echo $1 | grep -E co) != "" ]]
	then
		if [[ $color = true ]]
		then
			color=false
		elif [[ $color = false ]]
		then
			color=true
		fi
		((argleng--)); ((argleng--))
		colorer
	fi
	if [[ $(echo $1 | grep -E n) != "" ]]
	then
		ask=--noconfirm
		((argleng--))
	fi
	if [[ $(echo $1 | grep -E spgp) != "" ]]
	then
		pgp=--skippgpcheck
		((argleng--)); ((argleng--)); ((argleng--)); ((argleng--))
	fi
	if [[ $(echo $1 | grep -E ch) != "" ]]
	then
		buildchroot=yes
		if [[ $(uname -m) = armv7l ]]
		then
			echo ":: ${bold}${yellow}Warning:${normal} You may run into some issues using chroots on ALARM!"
		fi
		((argleng--)); ((argleng--))
	fi
	if [[ $(echo $1 | grep -E di) != "" ]]
	then
		installindex=""
		((argleng--)); ((argleng--))
	fi
	if [[ $argleng != 0 ]]
	then
		echo ":: ${red}${bold}ERROR:${normal} '$fullarg' is no known option! Try --help to see all options!"
		exit 2
	fi
}

netcheck(){
	inet=1
	if [[ $net != true ]]
	then
		if [[ $(ping -c 1 google.de >/dev/null 2>/dev/null ; echo $?) != 0 ]]
		then
			if [[ $1 = "-x" ]]
			then
				inet=0
			else
				echo ":: ${red}${bold}ERROR:${normal} Network is not reachable!"
				exit 1
			fi
		fi
		net=true
  fi
}

info(){
	netcheck -x
	pkgnames=($@)
	if [[ $all = true ]] && [[ $inet = 0 ]]
	then
		res=$(cat /usr/share/buildaur/res)
	else
		if [[ $inet = 0 ]]
		then
			if [[ $notext != 1 ]]
			then
			 echo -e ":: ${red}${bold}ERROR:${normal} Network is not reachable!"
			fi
			exit 1
		fi
		if [[ $notext != 1 ]]
		then
			if [[ $all = true ]]
			then
				echo ":: Updating packagelist..."
			else
				echo ":: Qetting package infos..."
			fi
			echo " AUR packages..."
		fi
		res="${proto}://aur.archlinux.org/rpc/?v=5&type=multiinfo"
		counter=0
		while [[ $counter -lt ${#pkgnames[*]} ]]
		do
			res=${res}"&arg[]="${pkgnames[$counter]}
			((counter++))
		done
		res=$(curl -s $res)
		if [[ $notext != 1 ]]
		then
			echo " ASP packages..."
		fi
		asp update >/dev/null 2>/dev/null
		if [[ $all = true ]]
		then
			if [[ "$res" != "$(cat /usr/share/buildaur/res)" ]]
			then
				echo "$res" | sudo tee /usr/share/buildaur/res >/dev/null
			fi
		fi
	fi
	resultcount=$(echo "$res" | cut -d'"' -f9 | sed -e 's/://g' | sed -e 's/,//g')
	counter=0
	aurpacs=()
	if [[ $notext != 1 ]]
	then
		echo -e ":: Giving out package infos..."
	fi
	while [[ $counter -lt $resultcount ]]
	do
		cutted=$(echo $res | cut -d{ -f$(expr $counter + 3))
		name=$(echo $cutted | cut -d'"' -f6)
		ver=$(pacman -Qqi $name 2>/dev/null | xargs 2>/dev/null | awk {'print $6'})
		remoteinfo=$(echo $cutted | cut -d'"' -f20)
		if [[ $name = "" ]] || [[ $ver = "" ]]
		then
			ver="--- "
		fi
		if [[ $q = 1 ]]
		then
			echo $name
		else
			echo " "$name $(echo $cutted | cut -d'"' -f16) "(local: $ver)"
			if [[ $remoteinfo = "" ]]
			then
				echo "    ${bold}${yellow}Warning:${normal} AUR does not provide information about this package!"
			else
				echo "    "$remoteinfo
			fi
		fi
		aurpacs[$counter]=$name
		((counter++))
	done
	if [[ $only = aur ]]
	then
		exit
	fi
	localpacs=($(echo ${aurpacs[@]} $@ | tr ' ' '\n' | sort | uniq -u))
	counter=0
	for pac in ${localpacs[@]}
	do
		aspinfo=$(asp show $pac 2>/dev/null)
		pkgver=0
		if [[ $aspinfo = "" ]]
		then
			if [[ $(pacman -Qi $pac 2>/dev/null) != "" ]]
			then
				if [[ $q = 1 ]]
				then
					echo $pac
				else
					pkgver=$(pacman -Qi $pac 2>/dev/null | xargs | awk {'print $6'})
					echo "  $pac $ver is not installed from ASP!"
					echo "     ${bold}${yellow}Warning:${normal} AUR does not provide information about this package!"
				fi
			fi
		else
			if [[ $q = 1 ]]
			then
				echo $pac
			else
				declare $(echo "$aspinfo" | grep -E pkgver | head -1)
				declare $(echo "$aspinfo" | grep -E pkgrel | head -1)
				declare "$(echo "$aspinfo" | grep -E pkgdesc | head -1)"
				ver=$(pacman -Qqi $pac | xargs 2>/dev/null | awk {'print $6'})
				echo "  $pac $pkgver-$pkgrel (local: $ver)"
				echo "     $(echo $pkgdesc | sed 's/"//g')"
			fi
		fi
		((count++))
	done
}

search(){
	netcheck
	while [[ $# -gt 1 ]]
	do
		key=$2
		echo ":: Checking AUR packages..."
		res=$(curl -s ''${proto}'://aur.archlinux.org/rpc/?v=5&type=search&arg='$key'')
		resultcount=$(echo $res | cut -d'"' -f9 | sed -e 's/://g' | sed -e 's/,//g')
		echo "  $resultcount packages found"
  	echo ":: Giving out package infos..."
		counter=0
		while [[ $counter -lt $resultcount ]]
		do
			cutted=$(echo $res | cut -d{ -f$(expr $counter + 3))
			name=$(echo $cutted | cut -d'"' -f6)
			ver=$(pacman -Q $name 2>/dev/null | cut -d" " -f2 | xargs)
			remoteinfo=$(echo $cutted | cut -d'"' -f20)
			if [[ $name = "" ]] || [[ $ver = "" ]]
			then
				ver="--- "
			fi
			echo " "$name $(echo $cutted | cut -d'"' -f16) "(local: $ver)"
			if [[ $remoteinfo = "" ]]
			then
				echo "    ${bold}${yellow}Warning:${normal} AUR does not provide information about this package!"
			else
				echo "    "$remoteinfo
			fi
			((counter++))
		done
		shift
	done
}

show_PKGBUILD(){
	notext=1
	q=1
	if [[ $1 = "" ]]
	then
		echo ":: ${red}${bold}ERROR:${normal} No package is given!"
		exit 1
	elif [[ $# -gt 1 ]]
	then
		echo ":: ${red}${bold}ERROR:${normal} Just one package should be given!"
		exit 1
	elif [[ $(info $1) = $1 ]]
	then
		cd ~/.cache/buildaur/build
		rm -rf ./$1
		git clone "https://aur.archlinux.org/$1.git" 2>/dev/null
		cd ./$1
		less ./PKGBUILD
	else
		echo ":: ${red}${bold}ERROR:${normal} $1 ist not in the AUR!"
		exit 1
	fi
}

depts(){
	. ./PKGBUILD
	depends=($(echo -e ${depends[@]} ${makedepends[@]} | sed 's/ /\n/g'| uniq))
	aurdeps=()
	depmaxcount=${#depends[*]}
	echo ":: Checking for dependecies..."
	echo " ($depmaxcount) Packages: ${depends[@]}"
	echo ":: Checking for unresolved dependecies..."
	for pac in ${depends[@]}
	do
		if [[ $(pacman -Si $pac 2>/dev/null) = "" ]] && [[ $(pacman -Qi $pac 2>/dev/null) = "" ]]
		then
			aurdeps=(${aurdeps[@]} $pac)
		fi
	done
	notext=1
	q=1
	aurdeps=($(info ${aurdeps[@]}))
	echo " (${#aurdeps[*]}) Packages: ${aurdeps[@]}"
	if [[ ${aurdeps[@]} != "" ]]
	then
		echo ":: Installing them..."
		echo
		install ${aurdeps[@]}
		echo
	fi
}

install(){
	if [[ $@ = "" ]]
	then
		echo " Nothing to do"
	else
		netcheck
		hooks prerunhooks
		installcount=1
		preinst $@
		hooks postrunhooks
	fi
}

preinst(){
	echo ":: Checking packages..."
	installpac=()
	niceinstallpac=()
	for key in $@
	do
		if [[ $mode != asp ]] && [[ $mode != url ]]
		then
			ver=$(pacman -Qqi $key 2>/dev/null| xargs 2>/dev/null | awk {'print $6'})
			res=$(curl -s ''${proto}'://aur.archlinux.org/rpc/?v=5&type=multiinfo&arg[]='$key'')
			remotever=$(echo $res | cut -d'"' -f26)
			if [[ $(echo $res | cut -d'"' -f9) = ":0," ]]
			then
				echo "${red}${bold}ERROR:${normal} $key ist not in the AUR!"
				exit 1
			fi
			if [[ $ver = "" ]]
			then
				printf ""
			elif [[ $ver = $remotever ]]
			then
				echo " ${bold}${yellow}Warning:${normal} $key-$ver is allready on $remotever -- reinstalling"
			elif [[ $(echo -e "$ver\n$remotever" | sort -V | xargs | awk {'print $1'}) = $ver ]]
			then
				echo " ${bold}Info:${normal} $key-$ver will be updated to $remotever!"
			else
				echo " ${bold}${yellow}Warning:${normal} $key-$ver is higher than AUR $remotever!"
			fi
			if [[ $(echo $res | cut -d'"' -f41) != :null, ]]
			then
				echo " ${bold}${yellow}Warning:${normal} $key is flagged out of date!"
			fi
		elif [[ $mode = asp ]]
		then
			echo ":: Updating ASP packagelist..."
			asp update 2>/dev/null >/dev/null
			aspout=$(echo "$(asp show $key 2>/dev/null)" | grep -E pkgver | head -1)
			aspoutrel=$(echo "$(asp show $key 2>/dev/null)" | grep -E pkgrel | head -1)
			ver=$(pacman -Qqi $key 2>/dev/null| xargs 2>/dev/null | awk {'print $6'})
			pkgver=0
		 	if [[ $aspout = "" ]]
			then
				echo "${red}${bold}ERROR:${normal} $key ist not on ASP!"
				exit 1
			fi
			declare $aspout
			declare $aspoutrel
			remotever=$pkgver-$pkgrel
			if [[ $ver = "" ]]
			then
				printf ""
			elif [[ $ver = $pkgver-$pkgrel ]]
			then
				echo " ${bold}${yellow}Warning:${normal} $key-$ver is allready on $pkgver-$pkgrel -- reinstalling"
			elif [[ $(echo -e "$ver\n$pkgver-$pkgrel" | sort -V | xargs | awk {'print $1'}) = $ver ]]
			then
				echo " ${bold}Info:${normal} $key-$ver will be updated to $pkgver-$pkgrel!"
			else
				echo " ${bold}${yellow}Warning:${normal} $key-$ver is higher than ASP $pkgver-$pkgrel!"
			fi
		fi
		installpac=(${installpac[@]} $key)
		niceinstallpac=(${niceinstallpac[@]} $key-$remotever)
		shift
	done
	echo ""
	echo "Packages (${#installpac[*]}): ${niceinstallpac[@]}"
	echo ""
	if [[ $ask = "--noconfirm" ]]
	then
		ans=y
	else
		echo ":: Continnue installation? [Y/n]"
		read ans
	fi
	if [[ $ans == y ]] || [[ $ans == "" ]]
	then
		realinst ${installpac[@]}
	fi
}

realinst(){
	sudo pacman -Sy
	while [[ $# -gt 0 ]]
	do
		echo ""
		if [[ $mode = asp ]] || [[ $mode = url ]]
		then
			echo "($installcount/$(expr $# + $installcount - 1)) Installing ${bold}$1${normal} ..."
		else
			echo "($installcount/$(expr $# + $installcount - 1)) Installing ${bold}$1-$remotever${normal} ..."
		fi
		mkdir -p ~/.cache/buildaur/build
		cd ~/.cache/buildaur/build
		if [[ $mode = url ]]
		then
			find ./urlbuild/buildaur.lock >/dev/null 2>/dev/null
			if [[ $? = 0 ]]
			then
				echo ":: ${red}${bold}ERROR:${normal} Buildaur is currendly working in this directory! Finnish the process or remove $(pwd)/urlbuild/buildaur.lock!"
				exit 1
			fi
		else
			find ./$1/buildaur.lock >/dev/null 2>/dev/null
			if [[ $? = 0 ]]
			then
				echo ":: ${red}${bold}ERROR:${normal} Buildaur is currendly working in this directory! Finnish the process or remove $(pwd)/$1/buildaur.lock!"
				exit 1
			fi
		fi
		rm -rf  ~/.cache/buildaur/build/$1 ~/.cache/buildaur/build/urlbuild
		if [[ $mode = asp ]]
		then
			echo ":: Updating asp packagelist..."
			asp update >/dev/null 2>/dev/null
			echo ":: Exporting package..."
			asp export $1 2>/dev/null
			cd ~/.cache/buildaur/build/$1
			if [[ $? != 0 ]]
			then
				echo ":: ${red}${bold}ERROR:${normal} $1 not found!"
				exit 2
			fi
		else
			echo ":: Clonig git repository..."
			if [[ $mode = url ]]
			then
				git clone $1 ~/.cache/buildaur/build/urlbuild 2>/dev/null
				cd ~/.cache/buildaur/build/urlbuild
			else
				git clone ${proto}://aur.archlinux.org/$1.git ~/.cache/buildaur/build/$1 2>/dev/null
				cd ~/.cache/buildaur/build/$1
			fi
		fi
		touch ./buildaur.lock
		if [[ $showPKGBUILD = 1 ]]
		then
			echo ":: Printing out PKGBUILD...${grey}"
			echo ""
			cat ./PKGBUILD | sed 's/^/  /g'
			echo "$normal"
		fi
		if [[ $ask = "--noconfirm" ]]
		then
			ans=n
		else
			echo ":: Edit the PKGBUILD? [y/N]"
			read ans
		fi
		if [[ $ans == n ]] || [[ $ans == "" ]]
		then
			echo ":: Going on..."
		else
			$editor ./PKGBUILD
		fi
		if [[ $sudoreset = 1 ]]
		then
			sudo -k
		fi
		hooks prehooks
		depts
		if [[ $mode = url ]]
		then
			cd ~/.cache/buildaur/build/urlbuild
		else
			cd ~/.cache/buildaur/build/$1
		fi
		if [[ $buildchroot = yes ]]
		then
			if [[ $CHROOT = "" ]]
			then
				echo ":: ${red}${bold}ERROR:${normal}: CHROOT variable is not defined! Use '--make-chroot' to create a chroot first"
				exit 1
			fi
			echo ":: Updating chrootpackages..."
			arch-nspawn $CHROOT/root pacman -Syu $ask
			echo ":: Making and installing the package..."
			makechrootpkg -c -r $CHROOT -- -sf $ask $pgp $colored
			. ./PKGBUILD
			if [[ $installindex = i ]]
			then
				sudo pacman -U $ask ./${pkgname}-${pkgver}-${pkgrel}-${arch}.pkg.tar.zst
			fi
		else
			echo ":: Making and installing the package..."
			makepkg -s${installindex}f $ask $pgp $colored
		fi
		if [[ $? = 0 ]]
		then
			hooks posthooks
			if [[ $installindex = "" ]]
			then
				echo ":: Info: Succesfully created package in $(pwd)!"
			else
				echo ":: Installation finished!"
			fi
		else
			echo ":: ${red}${bold}ERROR:${normal} Package installation FAILED!"
			errorcount=$(expr $errorcount + 1)
		fi
		rm ./buildaur.lock
		shift
		((installcount++))
	done
}

update(){
	netcheck
	pkgnames=($(pacman -Qqm))
	res="${proto}://aur.archlinux.org/rpc/?v=5&type=multiinfo"
	counter=0
	while [[ $counter -lt ${#pkgnames[*]} ]]
	do
		res=${res}"&arg[]="${pkgnames[$counter]}
		((counter++))
	done
	echo ":: Updating packagelist..."
	echo " AUR packages..."
	res=$(curl -s $res)
	if [[ "$res" != "$(cat /usr/share/buildaur/res)" ]]
	then
		echo "$res" | sudo tee /usr/share/buildaur/res >/dev/null
	fi
	echo " ASP packages..."
	asp update >/dev/null 2>/dev/null
	if [[ $layout = new ]]
	then
	  new_checker
	else
		old_checker
	fi
	if [[ ${willinst[@]} != "" ]]
	then
		install ${willinst[@]}
	fi
	if [[ ${willinstasp[@]} != "" ]]
	then
		mode=asp
		install ${willinstasp[@]}
	fi
	if [[ ${willinstasp[@]} = "" ]] && [[ ${willinst[@]} = "" ]]
	then
		echo " Nothing to do"
	elif [[ $errorcount = 0 ]]
	then
		echo " No errors accured"
	else
		echo " $errorcount error(s) accured!"
	fi
}

new_checker(){
	resultcount=$(echo $res | cut -d'"' -f9 | sed -e 's/://g' | sed -e 's/,//g')
	fullcount=$(pacman -Qqm | wc -l)
	willinst=()
	aurpacs=()
	errorcount=0
	count=1
	textcounter=0
	echo ":: Checking localy installed packages..."
	echo " $fullcount packages are curently installed!"
	echo ":: Checking for outdated packages..."
	until [[ $count = $(expr $resultcount + 1 ) ]]
	do
		cutted=$(echo $res | cut -d{ -f$(expr $count + 2))
	  name=$(echo $cutted | cut -d'"' -f6)
	  ver=$(pacman -Qqi $name | xargs 2>/dev/null | awk {'print $6'})
		remotever=$(echo $cutted | cut -d'"' -f16)
		progress $count $fullcount "Checking packages $name..."
		if [[ $remotever = "$ver" ]] || [[ $(echo "$black" | grep -xE $name) = "$name" ]]
		then
			printf "" >/dev/null
		elif [[ $(echo -e "$ver\n$remotever" | sort -V | xargs | awk {'print $1'}) = $ver ]]
		then
			willinst=(${willinst[@]} $name)
		else
			text[$textcounter]="${bold}${yellow}Warning:${normal} $name-$ver is higher than AUR $remotever!"
			((textcounter++))
			if [[ $ask_warn_inst = 1 ]]
			then
				willinst=(${willinst[@]} $name)
			fi
		fi
		aurpacs[$count]=$name
		((count++))
	done
	localpacs=($(echo ${aurpacs[@]} $(pacman -Qqm) | tr ' ' '\n' | sort | uniq -u))
	willinstasp=()
	for pac in ${localpacs[@]}
	do
		aspinfo=$(asp show $pac 2>/dev/null)
		pkgver=0
		progress $count $fullcount "Checking packages $pac..."
		if [[ $aspinfo = "" ]]
		then
			pkgver=$(pacman -Qqi $pac | xargs 2>/dev/null | awk {'print $6'})
		else
			if [[ $(asp list-all | grep -E -Ex $pac) != "" ]]
			then
				declare $(echo "$aspinfo" | grep -E pkgver | head -1)
				declare $(echo "$aspinfo" | grep -E pkgrel | head -1)
				ver=$(pacman -Qqi $pac | xargs 2>/dev/null | awk {'print $6'})
				if [[ $(echo ${black[*]} | sed -e 's/ /\n/g'| grep -E -xE $pac) = "$pac" ]] || [[ $pkgver-$pkgrel = "$ver" ]]
				then
					printf "" >/dev/null
				elif [[ $(echo -e "$ver\n$pkgver-$pkgrel" | sort -V | xargs | awk {'print $1'}) = $ver ]]
				then
					willinstasp=(${willinstasp[@]} $pac)
				else
					text[$textcounter]="${bold}${yellow}Warning:${normal} $pac-$ver is higher than ASP $pkgver-$pkgrel!"
					((textcounter++))
					if [[ $ask_warn_inst = 1 ]]
					then
						willinstasp=(${willinstasp[@]} $pac)
					fi
				fi
			fi
		fi
		((count++))
	done
	progress $fullcount $fullcount "Checking packages..."
	echo
	echo ":: Done"
	for message in "${text[@]}"
	do
		echo " $message"
	done
}

# old check function -- may be removed later
old_checker(){
	resultcount=$(echo $res | cut -d'"' -f9 | sed -e 's/://g' | sed -e 's/,//g')
	willinst=()
	aurpacs=()
	errorcount=0
	willinst=()
	aurpacs=()
	counter=0
	count=1
	echo ":: Checking installed AUR packages..."
	echo "  $resultcount packages are curently installed from the AUR!"
	echo ":: Checking for outdated packages..."
	while [[ $counter -lt $resultcount ]]
	do
		cutted=$(echo $res | cut -d{ -f$(expr $counter + 3))
	  name=$(echo $cutted | cut -d'"' -f6)
	  ver=$(pacman -Qqi $name | xargs 2>/dev/null | awk {'print $6'})
		remotever=$(echo $cutted | cut -d'"' -f16)
	  if [[ $name = "" ]] || [[ $ver = "" ]]
	  then
	  ver="--- "
	  fi
		if [[ $(echo ${black[*]} | sed -e 's/ /\n/g'| grep -E -xE $name) = "$name" ]]
		then
			echo "($count/$resultcount) $name-$ver is out of date! $remotever is available! But it's on the blacklist and will not be updated!"
		elif [[ $remotever = "$ver" ]]
		then
			echo "($count/$resultcount) $name-$ver is up to date"
		elif [[ $(echo -e "$ver\n$remotever" | sort -V | xargs | awk {'print $1'}) = $ver ]]
		then
			echo "($count/$resultcount) $name-$ver is out of date! $remotever is available!"
			askinst
		else
			echo "($count/$resultcount) ${bold}${yellow}Warning:${normal} $name-$ver is higher than AUR $remotever!"
			if [[ $ask_warn_inst = 1 ]]
			then
				askinst
			fi
		fi
		aurpacs[$count]=$name
		((count++))
    ((counter++))
	done
	echo
	echo ":: Searching non AUR packages..."
	localpacs=($(echo ${aurpacs[@]} $(pacman -Qqm) | tr ' ' '\n' | sort | uniq -u))
	echo "  ${#localpacs[*]} packages are not installed from any repository"
	count=1
	willinstasp=()
	echo ":: Listing them..."
	for pac in ${localpacs[@]}
	do
		aspinfo=$(asp show $pac 2>/dev/null)
		pkgver=0
		if [[ $aspinfo = "" ]]
		then
			pkgver=$(pacman -Qqi $pac | xargs 2>/dev/null | awk {'print $6'})
			echo "($count/${#localpacs[*]}) $pac-$ver is not installed from ASP!"
		else
			aspout=$(echo "$aspinfo" | grep -E pkgver | head -1)
			aspoutrel=$(echo "$aspinfo" | grep -E pkgrel | head -1)
			declare $aspout
			declare $aspoutrel
			ver=$(pacman -Qqi $pac | xargs 2>/dev/null | awk {'print $6'})
			if [[ $(echo ${black[*]} | sed -e 's/ /\n/g'| grep -E -xE $pac) = "$pac" ]]
			then
				echo "($count/${#localpacs[*]})) $pac-$pkgver-$pkgrel is out of date! $pkgver-$pkgrel is available! But it's on the blacklist and will not be updated!"
			elif [[ $pkgver-$pkgrel = "$ver" ]]
			then
				echo "($count/${#localpacs[*]}) $pac-$ver is up to date"
			elif [[ $(echo -e "$ver\n$pkgver-$pkgrel" | sort -V | xargs | awk {'print $1'}) = $ver ]]
			then
				echo "($count/${#localpacs[*]}) $pac-$ver is out of date! $pkgver-$pkgrel is available!"
				askinst asp
			else
				echo "($count/${#localpacs[*]}) ${bold}${yellow}Warning:${normal} $pac-$ver is higher than ASP $pkgver-$pkgrel!"
				if [[ $ask_warn_inst = 1 ]]
				then
					askinst asp
				fi
			fi
		fi
		((count++))
	done
}

askinst(){
	if [[ $ask = "--noconfirm" ]]
	then
		ans=y
	else
		echo ":: Should it be updated? [Y/n]"
		read ans
	fi
	if [[ $ans == y ]] || [[ $ans == "" ]]
	then
		if [[ $1 != asp ]]
		then
			willinst=(${willinst${1}[@]} $name)
	  else
			willinstasp=(${willinstasp[@]} $pac)
		fi
	fi
}

hooks(){
	hooks=($(ls /etc/buildaur/$1))
	if [[ $hooks -gt 0 ]]
	then
		echo ":: Running $1..."
		for hook in ${hooks[@]}
		do
			echo " ${hook}..."
			/etc/buildaur/$1/${hook} -u
			if [[ $? != 0 ]]
			then
				echo "${bold}${red}ERROR:${normal} Hook '$hook' exitet with exitstatus '$?' !"
				echo ":: Exiting..."
				rm ./buildaur.lock
				exit 1
			fi
		done
	fi
}

listhooks(){
	hookers=(prehooks posthooks prerunhooks postrunhooks hooks)
	for hook in ${hookers[@]}
		do
		if [[ $hook = hooks ]]
		then
			echo "deactivated hooks:"
		else
			echo "$hook:"
		fi
		hooks=($(ls /etc/buildaur/$hook))
		for hoook in ${hooks[@]}
		do
			. /etc/buildaur/$hook/$hoook
			echo " $hoook"
			echo "  $desc"
		done
	done
}

activate(){
	for hook in $@
	do
		. /etc/buildaur/hooks/$hook 2>/dev/null
		sudo mv /etc/buildaur/hooks/$hook /etc/buildaur/${type}hooks/ 2>/dev/null
		if [[ $? = 0 ]]
		then
			echo ":: Activated $hook!"
		else
			echo ":: ${red}${bold}ERROR:${normal} $hook is not available!"
			exit 1
		fi
	done
}

deactivate(){
	for hook in $@
	do
		. /etc/buildaur/prehooks/$hook 2>/dev/null
		. /etc/buildaur/posthooks/$hook 2>/dev/null
		. /etc/buildaur/prerunhooks/$hook 2>/dev/null
		. /etc/buildaur/postrunhooks/$hook 2>/dev/null
		sudo mv /etc/buildaur/${type}hooks/$hook /etc/buildaur/hooks/ 2>/dev/null
		if [[ $? = 0 ]]
		then
			echo ":: Deactivated $hook!"
		else
			echo ":: ${red}${bold}ERROR:${normal} $hook is not available!"
			exit 1
		fi
	done
}

hookhelp(){
	echo "Help-dialog for hooks"
	echo ""
	echo "  Hooks are skripts that run before and after the packagebuild."
	echo "  They are made to for example modify the PKGBUILD"
	echo "  All hooks are stored in /etc/buildaur/hooks"
	echo "  In /etc/buildaur/prehooks are the hooks stored wich run before the packagebuild"
	echo "  and in /etc/buildaur/posthooks those wich run after the packagebuild."
	echo "  A hook always contains a 'type' (pre oder post) and a 'desc' variable."
	echo "  It also contains an if-function wich contains the modifications for the PKGBUILD and so on"
	echo "  See /etc/buildaur/prehooks/1-arm-archfix as an example."
	echo ""
	echo "   Hookoptions:"
	echo "      --listhooks       : Lists all available and installed hooks"
	echo "      --hook-activate   : Activates a hook"
	echo "      --hook-deactivate : Deactivates a hook"
}

help(){
	echo "buildaur - An AUR helper with asp support"
	echo "Usage: $0 <option> <string>"
	echo "   General options:"
	echo "      -S                : Installs a package"
	echo "      -R                : Removes a package"
	echo "      -Q                : Lists installed packages or searches for ones in the AUR"
	echo "      -Qs               : Search the AUR"
	echo "      -Syu              : Updates all AUR packages"
	echo "      -url              : Installs a package from a given git-repository"
	echo "      -asp              : Builds a package from source using asp (usefull for archlinux arm)"
	echo "      --show            : Shows the PKGBUILD of a given package"
	echo "      --clear           : Cleanes build dir"
	echo "      -v|--version      : Displays version of this program"
	echo "      -l|--license      : Displays license of this program"
	echo "      --make-chroot     : Creates a chroot dir which can be used for building packages"
	echo "      --about           : Displays an about text"
	echo ""
	echo "   Additional options for -S,-R,-Syu,-asp:"
	echo "      n                 : Doesn't ask questions"
	echo "      spgp              : Skips pgp checks of sourcecode"
	echo "      ch                : Builds the package in a clean chroot (you may run into some problems using this on archlinux arm!)"
	echo "      di                : Just builds the package"
	echo "      co                : Toggles colored output on and off"
	echo ""
	echo "   Hookoptions:"
	echo "      --listhooks       : Lists all available and installed hooks"
	echo "      --hook-activate   : Activates a hook"
  echo "      --hook-deactivate : Deactivates a hook"
	echo ""
	echo "   Help options:"
	echo "      -h|--help         : Displays this help-dialog"
	echo "      --help-hooks      : Displays help-dialog for hooks"
}

about(){
	echo -e "Buildaur $(pacman -Q buildaur | cut -d" " -f2 | xargs) -- An AUR helper with asp support\n\nThis package is submited and maintained by lxgr -- <lxgr@protonmail.com>\nThis software is licensed under the GPL3.\n\nThis software is made to help archlinux users to install and update packages from the AUR in a save and consistent way."
}

fullarg=$@

case $1 in
	-S | -Sn* | -Sspgp* | -Sc* | -Sdi* | -Sus* )
		argleng=$(expr ${#1} - 2)
		options $@
		shift
		install $@
		exit 0
	;;
	-url*)
		argleng=$(expr ${#1} - 4)
		options $@
		shift
		mode=url
		install $@
		exit 0
	;;
	-asp*)
		argleng=$(expr ${#1} - 4)
		options $@
		shift
		mode=asp
		install $@
		exit 0
	;;
	-Q)
		shift
		if [[ $1 = "" ]]
		then
			echo ":: Checking installed AUR packages..."
			echo " $(pacman -Qqm | wc -l) packages are curently installed!"
			all=true
			info $(pacman -Qqm)
		else
			info $@
		fi
		exit 0
	;;
	-Qq)
		shift
		q=1
		if [[ $1 = "" ]]
		then
			echo ":: Checking installed AUR packages..."
			instpac=$(pacman -Qqm)
			echo " $(echo "$instpac" | wc -l) packages are curently installed!"
			all=true
			info $instpac
		else
			info $@
		fi
		exit 0
	;;
	-Qs)
		if [[ $2 = "" ]]
		then
			echo ":: ${red}${bold}ERROR:${normal} No search subject given!"
			exit 2
		else
			search $@
		fi
		exit 0
	;;
	-R)
		sudo pacman $@
		exit 0
	;;
	-Rn)
		sudo pacman --noconfirm $@
		exit 0
	;;
	-Syu*)
		argleng=$(expr ${#1} - 4)
		options $@
		update
		exit 0
	;;
	--help | -h)
		help
		exit 0
	;;
	-v | --version)
		pacman -Q buildaur | cut -d" " -f2 | xargs
		exit 0
	;;
	-l | --license)
		less /usr/share/licenses/buildaur/LICENSE
		exit 0
	;;
	--clear)
		echo ":: Cleaning builddir..."
		echo "  $(du -hcs ~/.cache/buildaur/build | xargs | awk {'print $1'})B will be removed!"
		rm -rf ~/.cache/buildaur/build/*
		echo ":: Done!"
		exit 0
	;;
	--about)
		about
		exit 0
	;;
	--listhooks)
		listhooks
		exit 0
	;;
	--hook-activate)
		shift
		if [[ $1 = all ]]
		then
			activate $(ls /etc/buildaur/hooks)
		else
			activate $@
		fi
		exit 0
	;;
	--hook-deactivate)
		shift
		if [[ $1 = all ]]
		then
			deactivate $(ls /etc/buildaur/prehooks) $(ls /etc/buildaur/posthooks) $(ls /etc/buildaur/prerunhooks) $(ls /etc/buildaur/postrunhooks)
		else
			deactivate $@
		fi
		exit 0
	;;
	--help-hooks)
		hookhelp
		exit 0
	;;
	--make-chroot)
		echo ":: Creating a chrootdir"
		sudo rm -rf ~/chroot 2>/dev/null
		mkdir ~/chroot
		export CHROOT=$HOME/chroot
		mkarchroot $CHROOT/root base-devel
		echo "export CHROOT=$HOME/chroot" >> $HOME/.bashrc
		exit 0
	;;
	--show)
		shift
		show_PKGBUILD $@
		exit 0
	;;
	*)
		if [[ $1 = "" ]]
		then
			echo ":: ${red}${bold}ERROR:${normal} No options are given! Try --help to see all options!"
			exit 2
		else
			echo ":: ${red}${bold}ERROR:${normal} '$@' is no known option! Try --help to see all options!"
			exit 2
		fi
	;;
esac
