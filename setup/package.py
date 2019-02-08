from . import PACKAGE_DEFINITIONS_DIR
from logging import getLogger
from subprocess import run, DEVNULL, STDOUT
from typing import Callable, Dict, Tuple, List


class Package():
    def __init__(self, os_flavor: str, name: PackageName, data: Dict):
        self._os_flavor = os_flavor
        self._name = name
        data['dependencies'] = [PackageName(d, own_repo=name.repo) for d in data.get('dependencies', [])]
        self._data = data


    def install(self, handle_dependency: Callable[[str], None], dependency_of: List[Package]) -> bool:
        dependencies: List[str] = self._data.get('dependencies', [])
        if dependencies:
            print('Installing dependencies for: {}... '.format(name))

            for dep in dependencies:
                print('... Dependency ', end='')
                success = handle_dependency(dep.replace('@', self._repo), dependency_of.append(self))
                if not success:
                    print('Aborting')
                    return False

        check_install_cmd = ''
        install_cmd = ''

        for definition in self._data.get('definitions', []):
            if self._os_flavor in definition.get('os_flavors'):
                # shortcut to install package using os's default installer
                if definition.get('package_name'):
                    check_install_cmd, install_cmd = self._os_package_install(definition.get('package_name'))
                    break

                check_install_cmd = definition.get('check_install')
                install_cmd = definition.get('install')
                break

        print('Installing: {}... '.format(name), end='')

        if check_install_cmd and install_cmd:
            result = run('set -x \n' + check_install_cmd, shell=True, text=True, env=self._env())
            if result.returncode == 0:
                print('already installed, skipping')
                return True

            result = run('set -x \n' + install_cmd, shell=True, text=True, env=self._env())
            if result.returncode == 0:
                print('✓')
            else:
                print('Failed')
                return False

            return True
        else:
            raise Exception('"install" and "check_install" required for {} {}'.format(self._os_flavor, name))

    def _os_package_install(self, name: str) -> Tuple[str, str]:
        if self._os_flavor == 'debian':
            return (
                "apt -qq --installed list apt -qq --installed list {} | grep -P '.+'".format(name),
                "sudo apt install -y {}".format(name)
            )

        elif self._os_flavor == 'mac':
            return (
                "brew ls --versions {}".format(name),
                "brew install -y {}".format(name)
            )

    def _env(self) -> Dict[str, str]:
        return {
            'DATA_DIR': PACKAGE_DEFINITIONS_DIR + '/' + self._
        }


class PackageName():
    def __init__(self, full_name: str, own_repo: str = None):
        self.repo, self.name = full_name.split(':')
        if self.repo == '@':
            if own_repo == None:
                raise TypeError('self repo must be set when repo is @')
            else:
                self.repo = own_repo

    def remove_alias(self, alias: str, real: str):
        if self.repo == alias:
            self.repo = real
            return True

        return False
