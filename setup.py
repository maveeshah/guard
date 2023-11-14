from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in guard/__init__.py
from guard import __version__ as version

setup(
	name="guard",
	version=version,
	description="Customizing ERP for Guard service  providers",
	author="Ameer Muavia Shah",
	author_email="mavee.shah@hotmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
