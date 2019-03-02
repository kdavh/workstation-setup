from copy import deepcopy
from logging import getLogger
import os
from os import path
from subprocess import Popen, PIPE, run
from typing import Callable, Dict, Tuple, List

from __init__ import CONFIG_DIR
import notify

PACKAGE_DEFINITIONS_REPOS = CONFIG_DIR + '/package_definitions'


class PackageName():
    def __init__(self, full_name: str, own_repo: str = None):
        self.repo, self.name = full_name.split(':')
        if self.repo == '@':
            if own_repo == None:
                raise TypeError('self repo must be set when repo is @')
            else:
                self.repo = own_repo

    @property
    def full(self):
        return ':'.join([self.repo, self.name])

    def resolve_alias(self, alias: str, real: str):
        if self.repo == alias:
            self.repo = real
            return True

        return False

    def __str__(self):
        return self.full


class Package():
    def __init__(self, os_flavor: str, name: PackageName, data: Dict, fs_context: str):
        self._os_flavor = os_flavor
        self._name = name
        self._data = deepcopy(data)
        self._data['dependencies'] = [PackageName(d, own_repo=name.repo) for d in self._data.get('dependencies', [])]
        self._fs_context = fs_context

    def export(self, handle_dependency: Callable[[str], None], dependency_of: List['Package'] = []) -> bool:
        if not self._handle_dependencies(handle_dependency, dependency_of):
            return False

        export_cmd = ''

        for definition in self._data.get('definitions', []):
            if self._os_flavor in definition.get('os_flavors'):
                export_cmd = definition.get('export')

                break

        notify.highlight(self._name, end='')
        if export_cmd:
            result = self._run(self._export_setup + export_cmd)
            if result.returncode == 0:
                notify.success(' -- Exported ✓✓✓')
                return True
            else:
                notify.failed(' -- Failed')
                return False
        else:
            notify.normal(' -- nothing to do')
            return True

    def install(self, handle_dependency: Callable[[str], None], dependency_of: List['Package'] = []) -> bool:
        if not self._handle_dependencies(handle_dependency, dependency_of):
            return False

        check_install_cmd = ''
        install_cmd = ''

        for definition in self._data.get('definitions', []):
            if self._os_flavor in definition.get('os_flavors'):
                # shortcut to install package using os's default installer
                if definition.get('package_name'):
                    check_install_cmd = self._os_default_check_install.format(definition.get('package_name'))
                    install_cmd = self._os_default_install.format(definition.get('package_name'))
                    break

                check_install_cmd = definition.get('check_install')
                install_cmd = definition.get('install')

                break

        notify.highlight(self._name, end='')

        if check_install_cmd and install_cmd:
            result = self._run(self._check_install_setup + check_install_cmd)
            if result.returncode == 0:
                notify.normal(' -- already installed, skipping')
                return True

            result = self._run(self._install_setup + install_cmd)
            if result.returncode == 0:
                notify.success(' -- Installed ✓✓✓')
            else:
                notify.failed(' -- Failed')
                return False

            return True
        else:
            raise Exception('"install" and "check_install" required for "{}" "{}"'.format(self._os_flavor, self._name))

    def _handle_dependencies(self, handle_dependency: Callable[[str], None], dependency_of: List['Package']) -> bool:
        dependencies = self._data.get('dependencies', [])
        if dependencies:
            notify.subtle('Dependencies for: {}... '.format(self._name))

            for dep in dependencies:
                notify.subtle('... Dependency ', end='')
                success = handle_dependency(dep, dependency_of + [self])
                if not success:
                    notify.failed('Aborting')
                    return False

        return True

    def _run(self, cmd):
        return run(cmd, shell=True, executable='/bin/bash', env=self._env())

    @property
    def _os_default_check_install(self) -> str:
        if self._os_flavor == 'debian':
            return "apt -qq --installed list apt -qq --installed list {} | grep -P '.+'"

        elif self._os_flavor == 'mac':
            return "brew ls --versions {}"

    @property
    def _os_default_install(self) -> str:
        if self._os_flavor == 'debian':
            return "sudo apt install -y {}"

        elif self._os_flavor == 'mac':
            return "brew install {}"

    @property
    def _check_install_setup(self):
        return """
            function package_manager_check_install() {{
                {};
            }};
            source $HOME/.bash_profile;
            set -x; # verbose
        """.format(self._os_default_check_install.format('"$1"'))

    @property
    def _install_setup(self):
        return """
            function package_manager_install() {{
                {};
            }};
            source $HOME/.bash_profile;
            set -e; # exit on error
            set -x; # verbose
        """.format(self._os_default_install.format('"$1"'))

    @property
    def _export_setup(self):
        return """
            source $HOME/.bash_profile;
            set -e; # exit on error
            set -x; # verbose
        """

    def _env(self) -> Dict[str, str]:
        return {
            'DATA_DIR': self._fs_context,
            'HOME': os.getenv('HOME'),
            'OS_FLAVOR': self._os_flavor,
        }
