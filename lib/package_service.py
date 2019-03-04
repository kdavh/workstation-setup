import os
from os import path
from subprocess import run
from typing import List
import yaml

from display.terminal import TerminalDisplay
from events import EventStream, PULLING_PACKAGE_REPO
import introspect
from package import Package, PackageName, PACKAGE_DEFINITIONS_REPOS
from repo import pull

class PackageService(object):
    def __init__(self, os_flavor: str=None):
        self._os_flavor = os_flavor or introspect.os_flavor()
        self._data = {}
        self._event_stream = EventStream(TerminalDisplay())

    def install(self, name: PackageName, dependency_of: List[Package] = [], force: bool = False, ignore_dependencies: bool = False):
        definitions_dir = path.join(PACKAGE_DEFINITIONS_REPOS, name.repo, 'package_definitions')
        package = Package(
            self._os_flavor,
            name,
            self._package_data(name),
            definitions_dir,
            self._event_stream,
        )

        # pass self.install so Package can trigger an install for each of its dependencies
        return package.install(self.install, dependency_of, force, ignore_dependencies)

    def export(self, name: PackageName, dependency_of: List[Package] = []):
        definitions_dir = path.join(PACKAGE_DEFINITIONS_REPOS, name.repo, 'package_definitions')
        package = Package(
            self._os_flavor,
            name,
            self._package_data(name),
            definitions_dir,
            self._event_stream,
        )

        # pass self.export so Package can trigger an export for each of its dependencies
        return package.export(self.export, dependency_of)

    def _package_data(self, name: PackageName):
        self._event_stream.push(PULLING_PACKAGE_REPO, name.repo)
        pull(PACKAGE_DEFINITIONS_REPOS, name.repo)
        definitions_dir = path.join(PACKAGE_DEFINITIONS_REPOS, name.repo, 'package_definitions')

        if not self._data.get(name.repo):
            self._data[name.repo] = {}
            for file in os.listdir(definitions_dir):
                if file.endswith('.yaml'):
                    with open(path.join(definitions_dir, file)) as yaml_stream:
                        self._data[name.repo] = {**self._data[name.repo], **yaml.load(yaml_stream)}

        return self._data[name.repo][name.name]
