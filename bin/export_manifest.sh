source $(dirname $0)/../lib/installation_helpers.sh

set_up_environment
trap tear_down_environment EXIT

python $LIB_DIR/run_export_manifest.py "$@"
