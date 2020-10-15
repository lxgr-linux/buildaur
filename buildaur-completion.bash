_buildaur(){
local OPTIONS=(-S
		 -R
		 -Q{q,qq,' '}
		 -Qs{q,qq,' '}
		 -Syu
		 -asp
		 -aspyu
		 --show
		 --clear
		 -v --version
		 -l --license
		 --make-chroot
		 --about
		 --listhooks
		 --hook-activate
		 --hook-deactivate
		 -h --help)

local cur=${COMP_WORDS[COMP_CWORD]}
local prev=${COMP_WORDS[COMP_CWORD-1]}

if [[ $COMP_CWORD == 1 ]]
then
	COMPREPLY=($(compgen -W "${OPTIONS[*]}" -- "$cur"))
else
	case $prev in
		-S)
		if ! [[ ${#cur} -lt 2 ]]
		then
			COMPREPLY=($(compgen -W "$(buildaur -Qsqq $cur)" -- "$cur"))
		fi
		;;
		--show)
			COMPREPLY=($(compgen -W "$(buildaur -Qsqq $cur) --diff" -- "$cur"))
		;;
		--diff)
		if ! [[ ${#cur} -lt 2 ]]
		then
			COMPREPLY=($(compgen -W "$(buildaur -Qsqq $cur)" -- "$cur"))
		fi
		;;
		--by)
			byOPTIONS=(name name-desc maintainer depends makedepends optdepends checkdepends)
			COMPREPLY=($(compgen -W "${byOPTIONS[*]}" -- "$cur"))
		;;
		--hook-activate)
			COMPREPLY=($(compgen -W "$(ls /etc/buildaur/hooks) all" -- "$cur"))
		;;
		--hook-deactivate)
			COMPREPLY=($(compgen -W "$(ls /etc/buildaur/prehooks) $(ls /etc/buildaur/posthooks) $(ls /etc/buildaur/prerunhooks) $(ls /etc/buildaur/postrunhooks) all" -- "$cur"))
		;;
		-Qs*)
			COMPREPLY=($(compgen -W "$(buildaur -Qsqq $cur) --by" -- "$cur"))
		;;
		-Q* | name | name-desc | maintainer | depends | makedepends | optdepends | checkdepends)
			COMPREPLY=($(compgen -W "$(buildaur -Qsqq $cur)" -- "$cur"))
		;;
	esac
fi
}

complete -F _buildaur buildaur
