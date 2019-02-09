function os_flavor() {
    echo $((test $(uname) = 'Darwin' && echo 'mac') || \cat /etc/*-release | grep -Po '(?<=^ID\=)\w*')
}

function bootstrap_installation_environment() {
    os_flavor=$1
    shift

    if [ ! -d ./venv ]; then
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

        virtualenv -p python3 ./venv
        source ./venv/bin/activate

        # in venv
        pip install pyyaml requests
    else
        source ./venv/bin/activate
    fi
}
