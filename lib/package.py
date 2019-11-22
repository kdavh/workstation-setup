from copy import deepcopy
from logging import getLogger
import os
from os import path
from subprocess import DEVNULL, Popen, PIPE, run
from typing import Callable, Dict, Tuple, List

from __init__ import CONFIG_DIR
from events import (EventStream,
    INSTALL_STARTED, INSTALL_SUCCEEDED, INSTALL_FAILED, INSTALL_ALREADY_DONE,
    EXPORT_STARTED, EXPORT_SUCCEEDED, EXPORT_FAILED, EXPORT_ALREADY_DONE,
)

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
    def __init__(self,
        os_flavor: str,
        name: PackageName,
        data: Dict,
        fs_context: str,
        event_stream: EventStream
    ):
        self._os_flavor = os_flavor
        self._name = name
        self._data = deepcopy(data)
        self._data['dependencies'] = [PackageName(d, own_repo=name.repo) for d in self._data.get('dependencies', [])]
        self._fs_context = fs_context
        self._event_stream = event_stream
        self._verbose = False

    def install(self,
        handle_dependency: Callable[[str], None],
        dependency_of: List['Package'] = [],
        force: bool = False,
        ignore_dependencies: bool = False
    ) -> bool:
        self._event_stream.push(INSTALL_STARTED, self._name)

        if not ignore_dependencies:
            if not self._handle_dependencies(handle_dependency, dependency_of, force):
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

        if check_install_cmd and install_cmd:
            result = self._run(self._check_install_setup + check_install_cmd, verbose=self._verbose)
            if result.returncode == 0:
                self._event_stream.push(INSTALL_ALREADY_DONE, self._name)
                if not force:
                    return True

            result = self._run(self._install_setup + install_cmd)
            if result.returncode == 0:
                self._event_stream.push(INSTALL_SUCCEEDED, self._name)
            else:
                self._event_stream.push(INSTALL_FAILED, self._name)
                return False

            return True
        else:
            raise Exception('"install" and "check_install" required for "{}" "{}"'.format(self._os_flavor, self._name))

    def export(self,
        handle_dependency: Callable[[str], None],
        dependency_of: List['Package'] = [],
    ) -> bool:
        self._event_stream.push(EXPORT_STARTED, self._name)

        if not self._handle_dependencies(handle_dependency, dependency_of):
            return False

        export_cmd = ''

        for definition in self._data.get('definitions', []):
            if self._os_flavor in definition.get('os_flavors'):
                export_cmd = definition.get('export')

                break

        if export_cmd:
            result = self._run(self._export_setup + export_cmd)
            if result.returncode == 0:
                self._event_stream.push(EXPORT_SUCCEEDED, self._name)
                return True
            else:
                self._event_stream.push(EXPORT_FAILED, self._name)
                return False
        else:
            self._event_stream.push(EXPORT_ALREADY_DONE, self._name)
            return True

    def _handle_dependencies(self, handle_dependency: Callable[[str], None], dependency_of: List['Package'], *args, **kwargs) -> bool:
        dependencies = self._data.get('dependencies', [])

        if dependencies:
            for dep in dependencies:
                success = handle_dependency(dep, dependency_of + [self], *args, **kwargs)
                if not success:
                    return False

        return True

    def _run(self, cmd, verbose=True):
        kwargs = {}
        # TODO: move out to TerminalDisplay.   It gets initial value of verboseness from cli flag.
        # it determines what to display.  Use a event_stream.writeln method or something to signify text instead of event
        if not verbose:
            kwargs['stderr'] = DEVNULL
            kwargs['stdout'] = DEVNULL
        return run(cmd, shell=True, executable='/bin/bash', env=self._env(), **kwargs)

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
            # source $HOME/.bash_profile;
            set -e; # exit on error
            set -x; # verbose
        """

    def _env(self) -> Dict[str, str]:
        return {
            'DATA_DIR': self._fs_context,
            'HOME': os.getenv('HOME'),
            'USER': os.getenv('USER'),
            'OS_FLAVOR': self._os_flavor,
        }
