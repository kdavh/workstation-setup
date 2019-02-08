#!/bin/bash

INSTALL_APP_DIR=$(dirname $_)/sys-install
ADDITIONAL_INSTALLS="$@"
CODE_DIR="$HOME/dev"
CONFIG_DIR="$HOME/.workstation-config"
SETUP_DIR="$CONFIG_DIR/workstation-setup/setup"

echo "which github user has access to applicable repos?"
read $GITHUB_USER

if ! ssh -T git@github.com | grep $GITHUB_USER; then
    ssh-keygen -t rsa -b 4096 -C $GITHUB_USER
    cat ~/.ssh/id_rsa.pub

    echo "log into github with $GITHUB_USER and go to https://github.com/settings/keys,"
    echo "add ssh key from above output"
    echo "press return when done"
    read
fi

mkdir -p $CONFIG_DIR

if ! test -d $SETUP_DIR ; then
    cd $CONFIG_DIR
    git clone git@github.com:kdavh/workstation-setup.git
fi

cd $SETUP_DIR

source ./installation_helpers.sh

OS_FLAVOR=$(os_flavor)

bootstrap_installation_environment $OS_FLAVOR

echo "Which installation manifest would you like to use? "
echo "Any github repo with a valid manifest.yaml"
echo "Examples:"
echo "kdavh/manifest-home"
echo "kdavh/twilio-setup"
read $MANIFEST_REPO

python ./install.py $OS_FLAVOR $MANIFEST_REPO
