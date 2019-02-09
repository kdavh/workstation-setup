import os
from os import path
from subprocess import run

def pull(base_dir, repo_name: str, update=True):
    data_dir = path.join(base_dir, repo_name)
    if not path.isdir(data_dir):
        os.makedirs(path.dirname(data_dir), exist_ok=True)
        run("git clone git@github.com:{}.git {}".format(repo_name, data_dir), shell=True)
    elif update:
        run("cd {} && git pull".format(data_dir), shell=True)
