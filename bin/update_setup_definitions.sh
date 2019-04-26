source $(dirname $0)/../lib/setup_helpers.sh
source $(dirname $0)/../lib/notify.sh

set_up_environment
trap tear_down_environment EXIT

echo "\nUpdates package_definitions, manifests, and workstation-setup repo\n\n"

function rebase_and_push() {
    cd $1
    notify_highlight "Processing $1"
    git add .
    if test -z "$(git diff-index --name-only HEAD --)"; then
        echo "$1 has no working changes, rebasing and pushing if needed"
        git pull --rebase
        git push
        return 0
    fi
    git diff HEAD
    git status
    notify_highlight "\nCommit and push changes? Enter commit message, 'y' for default message, or nothing to skip."
    read msg

    if test -n "$msg"; then
        if [ "$msg" == 'y' ]; then
            msg="Update $(git diff-index --name-only HEAD -- | paste -sd " " -)"
        fi
        git commit -m "$msg"
        git pull --rebase
        git push
    fi;
}

function rebase_and_push_nested_repos() {
    for repo_dir in $(find "$1" -mindepth 2 -maxdepth 2); do
        rebase_and_push $repo_dir
    done
}

rebase_and_push_nested_repos $PACKAGE_DEFS_DIR
rebase_and_push_nested_repos $MANIFESTS_DIR
rebase_and_push $SETUP_DIR
