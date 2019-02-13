from subprocess import run, PIPE

from __init__ import LIB_DIR

def os_flavor():
    return run(
        "source {}/installation_helpers.sh; os_flavor".format(LIB_DIR),
        # capture_output=True only available in python 3.7
        stdout=PIPE,
        stderr=PIPE,
        shell=True
    ).stdout.decode().strip()
