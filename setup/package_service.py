from . import CONFIG_DIR, PACKAGE_DEFINITIONS_DIR
import os
from subprocess import run
import yaml

from package import Package, PackageName


class PackageService(object):
    def __init__(self, os_flavor: str):
        self._os_flavor = os_flavor
        self._data = {}

    def install(self, package_name: PackageName, dependency_of: List[Package] = []):
        package = Package(self._os_flavor, package_name, self._package_data(package_name))

        # pass self.install so Package can trigger an install for each of its dependencies
        return package.install(self.install, dependency_of)

    def _package_data(self, name: PackageName):
        data_dir = PACKAGE_DEFINITIONS_DIR + '/' + name.repo
        if not os.path.isdir(data_dir):
            run("git clone git@github.com:{}.git {}".format(name.repo, data_dir))

        if not self._data[name.repo]:
            self._data[name.repo] = {}
            for file in os.listdir(data_dir):
                if file.endswith('.yaml'):
                    with open(data_dir + '/' + file) as yaml_stream:
                        self._data[name.repo] = {**self._data[name.repo], **yaml.load(yaml_stream)}

        return self._data[name.repo][name.name]
