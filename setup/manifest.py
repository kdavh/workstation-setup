from package import PackageName
from package_service import PackageService
from . import CONFIG_DIR

from io import BytesIO
from requests import get
from subprocess import run, DEVNULL
import yaml

class Manifest:

    def __init__(self, manifest_source: str, package_service: PackageService):
        self._manifest_source = manifest_source
        self._package_service = package_service
        self._package_list = []

    @property
    def _list(self):
        if not self._package_list:
            yaml_stream = BytesIO(get(self._source_url).text)
            data = yaml.safe_load(yaml_stream)

            for full_package in data['install']:
                name = PackageName(full_package)
                for alias, real in data['aliases'].items():
                    if name.remove_alias(alias, real):
                        break

                self._package_list.append(name)

    @property
    def _source_url(self):
        return "https://raw.githubusercontent.com/{}/master/manifest.yaml".format(self._manifest_source)

    def install(self):
        for package_name in self._list:
            self._package_service.install(package_name)


