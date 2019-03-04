import argparse
import sys

from package import Package, PackageName
from package_service import PackageService

parser = argparse.ArgumentParser()
parser.add_argument("package")
parser.add_argument("-f", "--force", action="store_true")
parser.add_argument("--ignore-dependencies", action="store_true")
args = parser.parse_args()

PackageService().install(PackageName(args.package), force=args.force, ignore_dependencies=args.ignore_dependencies)
