source ./installation_helpers.sh

cd $LIB_DIR

bootstrap_installation_environment

python ./install.py "$1"
