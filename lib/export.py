import sys

from package import Package, PackageName
from package_service import PackageService


package = sys.argv[1]

PackageService().export(PackageName(package))
