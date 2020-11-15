# LEGACY, USE https://github.com/kdavh/workstation

# workstation-setup
convenience script for setting up new workstation

## Install
```shell
bash -c "$(curl -fsS https://raw.githubusercontent.com/kdavh/workstation-setup/master/install.sh)"
```

## Usage

Install set of packages
```shell
$HOME/.workstation-config/workstation-setup/bin/install_manifest.sh kdavh/manifest-home
```
Install one package
```shell
$HOME/.workstation-config/workstation-setup/bin/install.sh kdavh/packages-core:git
```
