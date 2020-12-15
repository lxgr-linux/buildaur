trans={
"en" : {
    "conf_warning" : ":: %sWarning:\033[0m The config has errors in it.",
    "downloading" : ":: Downloading packagelist...",
    "downloading2" : "Downloading packagelist...",
    "error_server" : ":: %sERROR:\033[0m Server is not reachable!",
    "update_asp" : ":: Updatting asp database...",
    "collecting" : ":: Collecting package data...",
    "checking" : ":: Checking for outdated packages...",
    "checking1" : "Checking %s...",
    "checking2" : ":: Checking packages...",
    "warning_higher" : " %sWarning:\033[0m %s-%s is higher than AUR %s!",
    "warning_out-of-date" : " %sWarning:\033[0m %s is flagged as out-of-date since: %s!",
    "done" : ":: Done",
    "nothing" : " Nothing to do",
    "info_single" : {
        "name" : "Name",
        "ver" : "Version",
        "pkgb" : "Packagebase",
        "lver" : "Local Version",
        "desc" : "Description",
        "main" : "Maintainer",
        "url" : "URL",
        "fsub" : "First submitted",
        "lsub" : "Last modified",
        "pop" : "Popularity",
        "votes" : "Votes",
        "oof" : "Pkg out-of-date",
    },
    "info_arrays" : {
        "license" : "Licenses",
        "key" : "Keywords",
        "deps" : "Dependencies",
        "makedeps" : "Makedependencies",
        "optdeps" : "Optional dependencies",
    },
    "reinstalling" : " %sInfo:\033[0m %s-%s is up to date -- reinstalling",
    "updating" : " %sInfo:\033[0m %s-%s will be updated to %s",
    "error_not_found" : ":: %sERROR:\033[0m %s not found!",
    "packages" : "Packages (%s): ",
    "continnue" : "\n:: Continnue installation? [Y/n] ",
    "making" : "(%s/%s) Making package %s%s\033[0m...",
    "exporting" : ":: Exporting package...",
    "cloning" : ":: Cloning git repository...",
    "print_pkgb" : ":: Printing PKGBUILD...",
    "print_pkgdiff" : ":: Printing PKGDIFF...",
    "edit" : "\n:: Edit PKGBUILD? [y/c/N] ",
    "goingon" : ":: Going on",
    "exiting" : ":: Exiting",
    "update_chroot" : ":: Updating chrootpackages...",
    "making1" : ":: Making the package...",
    "installing" : ":: Installing packages...",
    "created" : ":: Package(s) created in:",
    "checking_deps" : ":: Checking for unresolved dependencies...",
    "hooks_off" : ":: deactivated hooks:",
    "hooks_on" : ":: Activated %s!",
    "hooks_off1" : ":: Deactivated %s!",
    "about" : "Buildaur %s -- An AUR helper with asp support\n\nThis package is submited and maintained by lxgr -- <lxgr@protonmail.com>\nThis software is licensed under the GPL3.\n\nThis software is made to help archlinux users to install and update packages from the AUR in a save and consistent way.",
    "running_hook" : ":: Running %s...",
    "error_root" : ":: %sERROR:\033[0m DON'T run this script as root, stupid!",
    "error_no_opts" : ":: %sERROR:\033[0m No options given!",
    "error_no_pkgs" : ":: %sERROR:\033[0m No packages given!",
    "error_makepkg": ":: %sERROR:\033[0m An error happened while making %s!",
    "error_search" : ":: %sERROR:\033[0m %s is not a valid search term!",
    "cleaning" : ":: Cleaning builddir...",
    "will_removed" : "B will be removed!",
    "creating_chroot" : ":: Creating a chrootdir",
    "error_pkgs_opts" : ":: %sERROR:\033[0m No package or other option is given!",
    "error_opts" : ":: %sERROR:\033[0m %s is no valid option!",
    "max_name_len" : 22,
    "help_start" : "buildaur - An AUR helper with asp support\nUsage: %s <option> <string>",
    "help" : {
        "main" : {
            "desc" : "General options:",
            "content" : {
                "-S" : "Installs a package",
                "-Q" : "Lists installed packages or searches for ones in the AUR",
                "-Qs" : "Search the AUR",
                "-Qi" : "Gives detailed package information",
                "-Syu" : "Updates all AUR packages",
                "-asp" : "Builds a package from source using asp (usefull for archlinux arm)",
                "-aspyu" : "Updates all asp packages (usefull for archlinux arm)",
                "--show" : "Shows the PKGBUILD of a given package",
                "--clear" : "Cleanes build dir",
                "-v|--version" : "Displays version of this program",
                "-l|--license" : "Displays license of this program",
                "--make-chroot" : "Creates a chroot dir which can be used for building packages",
                "--about" : "Displays an about text",
            },
        },
        "add_main" : {
            "desc" : "Additional options for -S,-R,-Syu,-asp,-aspyu:",
            "content" : {
                "n" : "Doesn't ask questions",
                "spgp" : "Skips pgp checks of sourcecode",
                "ch" : "Builds the package in a clean chroot (you may run into some problems using this on archlinux arm!)",
                "di" : "Just builds the package",
                "co" : "Toggles colored output on and off",
            },
        },
        "show" : {
            "desc" : "Additional options for --show:",
            "content" : {
                "--diff" : "Outputs diff between current pkgbuildver and former pkgbuildver",
            },
        },
        "Q" : {
            "desc" : "Additional options for -Q,-Qs",
            "content" : {
                "q" : "Just outputs pknames and vers",
                "qq" : "JUST outputs pknames",
                "--by" : "Defines the value that should be searched by (values: name name-desc maintainer depends makedepends optdepends checkdepends",
            },
        },
        "hooks" : {
            "desc" : "Hookoptions:",
            "content" : {
                "--listhooks" : "Lists all available and installed hooks",
                "--hook-activate" : "Activates a hook",
                "--hook-deactivate" : "Deactivates a hook",
            },
        },
        "help" : {
            "desc" : "Help options:",
            "content" : {
                "-h|--help" : "Displays this help-dialog",
            },
        },
    },
},
"de": {
    "conf_warning" : ":: %sWarnung:\033[0m Die Konfigurationsdatei beinhaltet Fehler!",
    "downloading" : ":: Lade Packetliste herunter...",
    "downloading2" : "Lade Packetliste herunter...",
    "error_server" : ":: %sERROR:\033[0m Server nicht erreichbar!",
    "update_asp" : ":: Update asp Datenbank...",
    "collecting" : ":: Sammle Packetdaten...",
    "checking" : ":: Überprüfe alte Packete...",
    "checking1" : "Überprüfe %s...",
    "checking2" : ":: Überprüfe Packete...",
    "warning_higher" : " %sWarnung:\033[0m %s-%s ist neuer als AUR %s!",
    "warning_out-of-date" : " %sWarnung:\033[0m %s ist als out-of-date markiert seit: %s!",
    "done" : ":: Fertig",
    "nothing" : " Nichts zu tun",
    "info_single" : {
        "name" : "Name",
        "ver" : "Version",
        "pkgb" : "Packagebase",
        "lver" : "Lokale Version",
        "desc" : "Beschreibung",
        "main" : "Instandhalter",
        "url" : "URL",
        "fsub" : "Zuerst hinzugefügt",
        "lsub" : "Zuletzt bearbeitet",
        "pop" : "Bekanntheit",
        "votes" : "Stimmen",
        "oof" : "Pkg out-of-date",
    },
    "info_arrays" : {
        "license" : "Lizenz",
        "key" : "Schlüsselwörter",
        "deps" : "Abhängigkeiten",
        "makedeps" : "Erstellungs Abhängigkeiten",
        "optdeps" : "Optionale Abhängigkeiten",
    },
    "reinstalling" : " %sInfo:\033[0m %s-%s ist schon auf neuster Version -- Reinstalliere",
    "updating" : " %sInfo:\033[0m %s-%s wird auf %s geupdatet",
    "error_not_found" : ":: %sERROR:\033[0m %s nicht gefunden!",
    "packages" : "Packete (%s): ",
    "continnue" : "\n:: Installation fortsetzen? [Y/n] ",
    "making" : "(%s/%s) Erstelle Packet %s%s\033[0m...",
    "exporting" : ":: Exportiere Packet...",
    "cloning" : ":: Klone git Repository...",
    "print_pkgb" : ":: Gebe PKGBUILD aus...",
    "print_pkgdiff" : ":: Gebe PKGDIFF aus...",
    "edit" : "\n:: PKGBUILD bearbeiten? [y/c/N] ",
    "goingon" : ":: Fahrefort",
    "exiting" : ":: Verlasse",
    "update_chroot" : ":: Update ChrootPackete...",
    "making1" : ":: Erstelle das Packet...",
    "installing" : ":: Installiere Packete...",
    "created" : ":: Packet(e) erstellt in:",
    "checking_deps" : ":: Suche nach unerfüllten Abhängigkeiten...",
    "hooks_off" : ":: Deaktivierte Hooks:",
    "hooks_on" : ":: Habe %s aktiviert!",
    "hooks_off1" : ":: Habe %s deaktiviert!",
    "about" : "Buildaur %s -- Ein AUR Helper mit ASP Support\n\nDieses Packet wird von lxgr -- <lxgr@protonmail.com> übermittelt und in Stand gehalten\nDiese Software ist unter der GPL3 lizensiert.\n\nDiese Software wurde geschrieben um es Archlinux Usern zu ermöglichen sicher und verlässlich Packete aus dem AUR zu installieren.",
    "running_hook" : ":: Laufe %s...",
    "error_root" : ":: %sERROR:\033[0m Führe dieses Skript NIEMALS als root aus, Dummkopf!",
    "error_no_opts" : ":: %sERROR:\033[0m Keine Optionen gegeben!",
    "error_no_pkgs" : ":: %sERROR:\033[0m Keine Packete gegeben!",
    "error_makepkg": ":: %sERROR:\033[0m Ein Fehler trat beim erstellen von %s auf!",
    "error_search" : ":: %sERROR:\033[0m %s ist keine valide Suchoption!",
    "cleaning" : ":: Räume Builddir auf...",
    "will_removed" : "B werden entfernt!",
    "creating_chroot" : ":: Erstelle Chrootdir",
    "error_pkgs_opts" : ":: %sERROR:\033[0m Keine Packete oder andere Optionen gegeben!",
    "error_opts" : ":: %sERROR:\033[0m %s ist keine valide Option!",
    "max_name_len" : 27,
    "help_start" : "buildaur - Ein AUR Helper mit ASP Support\nUsage: %s <option> <string>",
    "help" : {
        "main" : {
            "desc" : "Generelle Optionen:",
            "content" : {
                "-S" : "Installiert Packete",
                "-Q" : "Listet Packete auf",
                "-Qs" : "Sucht Packete im AUR",
                "-Qi" : "Gibt detaillierte Packetinformationen zurück",
                "-Syu" : "Updatet alle AUR Packete",
                "-asp" : "Erstellt Packete aus der Quelle",
                "-aspyu" : "Updatet alle Packete, welche über asp erstellt wurden",
                "--show" : "Gibt den Inhalt eines PKGBUILDs aus",
                "--clear" : "Bereinigt Erstellungsordner",
                "-v|--version" : "Gibt Version aus",
                "-l|--license" : "Gibt Lizenz aus",
                "--make-chroot" : "Erstellt chroot Ordner",
                "--about" : "Gibt einen Übertext aus",
            },
        },
        "add_main" : {
            "desc" : "Weitere Optionen für -S,-R,-Syu,-asp,-aspyu:",
            "content" : {
                "n" : "Fragt keine Fragen",
                "spgp" : "Überspringt pgp Check des Quellcodes",
                "ch" : "Erstellt das Packet in einem sauberen chroot Ordner",
                "di" : "Erstellt das Packet nur",
                "co" : "Deaktiviert farbige Ausgabe",
            },
        },
        "show" : {
            "desc" : "Weitere Optionen für --show:",
            "content" : {
                "--diff" : "Gibt Unterschied zwischen aktuellem und älterem PKGBUILD aus",
            },
        },
        "Q" : {
            "desc" : "Weitere Optionen für -Q,-Qs",
            "content" : {
                "q" : "Gibt nur Packetname und Version aus",
                "qq" : "Gibt nur Packetnamen aus",
                "--by" : "Suchoption nach der gesucht werden soll (values: name name-desc maintainer depends makedepends optdepends checkdepends",
            },
        },
        "hooks" : {
            "desc" : "Hookoptionen:",
            "content" : {
                "--listhooks" : "Gibt alle Hooks aus",
                "--hook-activate" : "Aktiviert eine Hook",
                "--hook-deactivate" : "Deaktiviert eine Hook",
            },
        },
        "help" : {
            "desc" : "Hilfeoptionen:",
            "content" : {
                "-h|--help" : "Gibt diesen Hilfedialog aus",
            },
        },
    },
},
}
