CONFIG_DIR="$HOME/.workstation-config"
LIB_DIR="$CONFIG_DIR/workstation-setup/lib"

function os_flavor() {
    echo $((test $(uname) = 'Darwin' && echo 'mac') || \cat /etc/*-release | grep -Po '(?<=^ID\=)\w*')
}

function set_up_environment() {
    ! test -d $CONFIG_DIR && mkdir -p $CONFIG_DIR

    os_flavor=$(os_flavor)

    if [ ! -d $CONFIG_DIR/venv ]; then
        if [ "$os_flavor" = 'debian' ]; then
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

        # requirements for venv
        pip install pyyaml requests
    else
        source $CONFIG_DIR/venv/bin/activate
    fi
}

function tear_down_environment() {
   deactivate
}
