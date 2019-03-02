source $(dirname $0)/../lib/installation_helpers.sh
source $(dirname $0)/../lib/notify.sh

set_up_environment
trap tear_down_environment EXIT

for repo_dir in "$(find $PACKAGE_DEFS_DIR -mindepth 2 -maxdepth 2)"; do
    cd $repo_dir
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
done
