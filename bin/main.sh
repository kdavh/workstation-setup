#!/bin/sh

# this will allow access to all subscripts ++

cmd1="$1"
cmd2="$2"

dot_dir="${HOME}/.workstation-config"
bin_dir="${dot_dir}/workstation-setup/bin"

case "$cmd1" in
    config)
        case "$cmd2" in
            commit)
                "${bin_dir}/config_commit.sh"
                break
                ;;
            edit)
                code -n $dot_dir
                break
                ;;
            *)
                echo "$cmd2 not valid"
        esac
        break
        ;;

    *)
        echo "$cmd1 not valid"
esac
