import os
from os import path
from subprocess import DEVNULL, run

def _run(cmd):
    return run(cmd, shell=True, stderr=DEVNULL, stdout=DEVNULL)

def pull(base_dir, repo_name: str, update=True):
    data_dir = path.join(base_dir, repo_name)
    if not path.isdir(data_dir):
        os.makedirs(path.dirname(data_dir), exist_ok=True)
        _run("git clone git@github.com:{}.git {}".format(repo_name, data_dir))
    elif update:
        _run("cd {} && git pull".format(data_dir))
