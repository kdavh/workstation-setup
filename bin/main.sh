#!/usr/bin/env bash

# this will allow access to all subscripts ++
usage="$(cat <<USAGE
Usage: wk [options] command subcommand

wk is a tool for controlling workspace configuration and installation on multiple computer architectures.

Commands:
  config - commands having to do with own tool configuration
    edit - open workstation code in editor
    commit - commit local changes for core tools, package and manifest definitions

USAGE
)"

cmd1="$1"
cmd2="$2"

if [ "$cmd1" = "-h" ]; then
    printf "$usage\n"
    exit 0
fi

dot_dir="${HOME}/.workstation-config"
bin_dir="${dot_dir}/workstation-setup/bin"

case "$cmd1" in
    config)
        case "$cmd2" in
            commit)
                "${bin_dir}/config_commit.sh"
                ;;
            edit)
                code -n $dot_dir
                ;;
            *)
                echo "$cmd2 not valid"
        esac
        ;;

    install)
        shift
        $bin_dir/install_package.sh "$@"
        ;;
    *)
        echo "$cmd1 not valid"
esac
