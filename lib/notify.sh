# https://misc.flogisoft.com/bash/tip_colors_and_formatting

NOTIFY_HEADER="\033[95m"
NOTIFY_OKBLUE="\033[94m"
NOTIFY_OKGREEN="\033[92m"
NOTIFY_WARNING="\033[93m" # yellow
NOTIFY_FAIL="\033[91m"
NOTIFY_ENDC="\033[0m"
NOTIFY_BOLD="\033[1m"
NOTIFY_UNDERLINE="\033[4m"

function notify_highlight() {
    echo -e "${NOTIFY_WARNING}${1}${NOTIFY_ENDC}"
}
