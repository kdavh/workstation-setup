CONFIG_DIR="$HOME/.workstation-config"
SETUP_DIR="$CONFIG_DIR/workstation-setup"
LIB_DIR="$SETUP_DIR/lib"
PACKAGE_DEFS_DIR="$CONFIG_DIR/package_definitions"
MANIFESTS_DIR="$CONFIG_DIR/manifests"

function os_flavor() {
    echo $((test $(uname) = 'Darwin' && echo 'mac') || \cat /etc/*-release | grep -Po '(?<=^ID\=)\w*')
}

function set_up_environment() {
    ! test -d $CONFIG_DIR && mkdir -p $CONFIG_DIR

    os_flavor=$(os_flavor)

    if [ ! -d $CONFIG_DIR/venv ]; then
        if [ "$os_flavor" = 'debian' ]; then
            sudo apt-get update
            sudo apt install -y python3-pip;
        elif [ "$os_flavor" = 'mac' ]; then
            if ! command -v brew; then
                /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
            fi
            brew install python3
        else
            echo "OS FLAVOR \"${os_flavor}\"" not handled
            exit 1
        fi

        pip3 install virtualenv

        # linux non-sudo virtualenv install does not put virtualenv in $PATH
        python3 -m virtualenv -p python3 $CONFIG_DIR/venv
        source $CONFIG_DIR/venv/bin/activate

        # mac stopped finding wheel from venv, so make sure venv python finds it
        export PYTHONPATH=$PYTHONPATH:$CONFIG_DIR/venv/lib/python3.7/site-packages
        # requirements for venv
        pip install \
            pyyaml \
            pylint \
            requests \
            termcolor
    else
        source $CONFIG_DIR/venv/bin/activate
    fi
}

function tear_down_environment() {
   deactivate
}
