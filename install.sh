
INSTALL_APP_DIR=$(dirname $_)/sys-install
ADDITIONAL_INSTALLS="$@"
CODE_DIR="$HOME/dev"
CONFIG_DIR="$HOME/.workstation-config"
SETUP_DIR="$CONFIG_DIR/workstation-setup/setup"

# DEFAULT_USER=$(ssh -T git@github.com 2>&1 | grep -Eo ' (\S+)!' | sed 's/.$//' | sed 's/^.//')
# echo "If $DEFAULT_USER is correct github user, press enter."
# echo "... otherwise, enter current github user has access to applicable repos, or user you want to use on this computer"
# read GITHUB_USER

# if ! test -z $GITHUB_USER; then
#     if ! ssh -T git@github.com 2>&1 | grep 'Hi $GITHUB_USER!'; then
#         ssh-keygen -t rsa -b 4096 -C $GITHUB_USER
#         cat ~/.ssh/id_rsa.pub

#         echo "log into github with $GITHUB_USER and go to https://github.com/settings/keys,"
#         echo "add ssh key from above output"
#         echo "press return when done"
#         read
#     fi
# fi

# mkdir -p $CONFIG_DIR

# if ! test -d $SETUP_DIR ; then
#     cd $CONFIG_DIR
#     git clone git@github.com:kdavh/workstation-setup.git
# fi

cd $SETUP_DIR

source ./installation_helpers.sh

OS_FLAVOR=$(os_flavor)

bootstrap_installation_environment $OS_FLAVOR

# echo "Which installation manifest would you like to use? "
# echo "Any github repo with a valid manifest.yaml"
# echo "Examples:"
# echo "1. kdavh/manifest-home"
# echo "2. kdavh/twilio-setup"
# echo "or enter your own"
# read MANIFEST_REPO

# if test "$MANIFEST_REPO" = '1'; then
#     MANIFEST_REPO='kdavh/manifest-home'
# elif test "$MANIFEST_REPO" = '2'; then
    MANIFEST_REPO='kdavh/twilio-setup'
# else
#     exit 1
# fi

python ./install.py $OS_FLAVOR $MANIFEST_REPO
