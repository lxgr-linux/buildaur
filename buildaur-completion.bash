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
		if ! [[ ${#cur} -lt 3 ]]
		then
			COMPREPLY=($(compgen -W "$(buildaur.py -Qsqq $cur)" -- "$cur"))
		fi
		;;
	esac
fi
}

complete -F _buildaur buildaur.py
