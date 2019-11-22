from os import path
from io import BytesIO
from requests import get
from subprocess import run, DEVNULL
import yaml

from __init__ import CONFIG_DIR
from package import PackageName
from package_service import PackageService
from repo import pull

MANIFESTS_DIR = CONFIG_DIR + '/manifests'


class Manifest:

    def __init__(self, repo: str, package_service: PackageService):
        self._repo = repo
        self._package_service = package_service
        self._package_list = []

    @property
    def _list(self):
        pull(MANIFESTS_DIR, self._repo)

        if not self._package_list:
            with open(path.join(MANIFESTS_DIR, self._repo, 'manifest.yaml')) as m:
                data = yaml.safe_load(m)

                for full_package in data['install']:
                    name = PackageName(full_package)
                    for alias, real in data['aliases'].items():
                        if name.resolve_alias(alias, real):
                            break

                    self._package_list.append(name)

        return self._package_list

    def install(self):
        for package_name in self._list:
            self._package_service.install(package_name)
            input('REVIEW AND PRESS RETURN TO CONTINUE')

    def export(self):
        for package_name in self._list:
            self._package_service.export(package_name)
