import sys

from manifest import Manifest
from package_service import PackageService


manifest_repo = sys.argv[1]

manifest = Manifest(manifest_repo, PackageService())
manifest.install()


### TODO:
# pip install awscli \ # https://github.com/aws/aws-cl


### TODO: debian: xclip \ xsel \ inotify-tools \

### TODO:
#   # better cat
#   curl https://github.com/sharkdp/bat/releases/download/v0.6.1/bat_0.6.1_amd64.deb -L -o bat.deb
#   sudo dpkg -i bat.deb
#   rm bat.deb

#   # fuzzy finder, replaces ctrl-R shell lookup, other things
#   git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
#   ~/.fzf/install

#   # better git diff tool, not really the same interface as diff though
#   curl https://raw.githubusercontent.com/so-fancy/diff-so-fancy/master/third_party/build_fatpack/diff-so-fancy -o ~/bin/diff-so-fancy

#   # better find (by file name)
#   curl https://github.com/sharkdp/fd/releases/download/v7.1.0/fd_7.1.0_amd64.deb -L -o fd.deb
#   sudo dpkg -i fd.deb
#   rm fd.deb

#   # better du
#   sudo apt install ncdu
#   # better file explorer
#   sudo apt install nnn

#   # better help / man
#   npm install -g tldr

#   # get notified about things
#   go get -u github.com/variadico/noti/cmd/noti
