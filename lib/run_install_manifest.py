import sys

from manifest import Manifest
from package_service import PackageService


manifest_repo = sys.argv[1]

manifest = Manifest(manifest_repo, PackageService())
manifest.install()
