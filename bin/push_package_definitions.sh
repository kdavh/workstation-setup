source $(dirname $0)/../lib/installation_helpers.sh

set_up_environment
trap tear_down_environment EXIT

for repo_dir in "$(find $PACKAGE_DEFS_DIR -mindepth 2 -maxdepth 2)"; do
    cd $repo_dir
    git add .
    git diff HEAD
    git status
    read -p "\nCommit and push changes?" yn

    if [ "$yn" == 'y' ]; then
        read -p "\nWhat is the commit message?" msg
        git commit -m "$msg"
        git push
    fi;
done
