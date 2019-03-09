from subprocess import check_output, PIPE

from __init__ import LIB_DIR

def os_flavor():
    return check_output(
        "source {}/setup_helpers.sh; os_flavor".format(LIB_DIR),
        executable='/bin/bash',
        shell=True
    ).decode().strip()
