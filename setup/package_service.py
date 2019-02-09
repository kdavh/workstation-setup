import os
from os import path
from subprocess import run
from typing import List
import yaml

from package import Package, PackageName, PACKAGE_DEFINITIONS_REPOS
from repo import pull

class PackageService(object):
    def __init__(self, os_flavor: str):
        self._os_flavor = os_flavor
        self._data = {}

    def install(self, name: PackageName, dependency_of: List[Package] = []):
        definitions_dir = path.join(PACKAGE_DEFINITIONS_REPOS, name.repo, 'package_definitions')
        package = Package(self._os_flavor, name, self._package_data(name), definitions_dir)

        # pass self.install so Package can trigger an install for each of its dependencies
        return package.install(self.install, dependency_of)

    def _package_data(self, name: PackageName):
        pull(PACKAGE_DEFINITIONS_REPOS, name.repo)
        definitions_dir = path.join(PACKAGE_DEFINITIONS_REPOS, name.repo, 'package_definitions')

        if not self._data.get(name.repo):
            self._data[name.repo] = {}
            for file in os.listdir(definitions_dir):
                if file.endswith('.yaml'):
                    with open(path.join(definitions_dir, file)) as yaml_stream:
                        self._data[name.repo] = {**self._data[name.repo], **yaml.load(yaml_stream)}

        return self._data[name.repo][name.name]
