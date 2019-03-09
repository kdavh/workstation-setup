source $(dirname $0)/../lib/setup_helpers.sh
source $(dirname $0)/../lib/notify.sh

set_up_environment
trap tear_down_environment EXIT

echo "\nUpdates package_definitions, manifests, and workstation-setup repo\n\n"

function rebase_and_push() {
    cd $1
    echo "processing $1"
    git add .
    git diff HEAD
    git status
    notify_highlight "\nCommit and push changes?"
    read yn

    if [ "$yn" == 'y' ]; then
        notify_highlight "\nWhat is the commit message?"
        read msg
        git commit -m "$msg"
        git push
    fi;
}

function rebase_and_push_nested_repos() {
    for repo_dir in "$(find "$1" -mindepth 2 -maxdepth 2)"; do
        rebase_and_push $repo_dir
    done
}

rebase_and_push_nested_repos $PACKAGE_DEFS_DIR
rebase_and_push_nested_repos $MANIFESTS_DIR
rebase_and_push $SETUP_DIR
