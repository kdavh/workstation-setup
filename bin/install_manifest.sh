source $(dirname $0)/../lib/installation_helpers.sh

MANIFEST_REPO="$1"

set_up_environment
trap tear_down_environment EXIT

python $LIB_DIR/install_manifest.py "$MANIFEST_REPO"
