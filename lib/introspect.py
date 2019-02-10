from subprocess import run

from __init__ import LIB_DIR

def os_flavor():
    return run(
        "source {}/installation_helpers.sh; os_flavor".format(LIB_DIR),
        capture_output=True,
        shell=True
    ).stdout.decode().strip()
