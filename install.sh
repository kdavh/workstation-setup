CONFIG_DIR="$HOME/.workstation-config"

mkdir -p $CONFIG_DIR

if ! test -d $CONFIG_DIR/workstation-setup; then
    cd $CONFIG_DIR
    git clone https://github.com/kdavh/workstation-setup.git
    cd $CONFIG_DIR/workstation-setup
    git remote set-url origin git@github.com:kdavh/workstation-setup.git
fi

# set up git ssh keys
DEFAULT_USER=$(ssh -T git@github.com 2>&1 | grep -Eo ' (\S+)!' | sed 's/.$//' | sed 's/^.//')

if ! test -z "$DEFAULT_USER"; then
    echo "If $DEFAULT_USER is correct github user, press enter."
    echo "... otherwise,"
fi

echo "enter github user with access to applicable repos and that you want to use on this computer"
read GITHUB_USER

if ! test -z "$GITHUB_USER"; then
    if ! ssh -T git@github.com 2>&1 | grep 'Hi $GITHUB_USER!'; then
        ssh-keygen -t rsa -b 4096 -C $GITHUB_USER
        cat ~/.ssh/id_rsa.pub

        echo "log into github with $GITHUB_USER and go to https://github.com/settings/keys,"
        echo "add ssh key from above output"
        echo "press return when done"
        read
    fi
fi
