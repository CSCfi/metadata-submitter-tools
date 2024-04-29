"""Setup for Metadata Validator."""

from setuptools import setup, find_packages

from validator import __author__, __title__, __version__

with open("requirements.txt") as reqs:
    requirements = reqs.read().splitlines()

setup(
    # Core metadata specification here:
    # https://packaging.python.org/specifications/core-metadata/
    name="metadata-submitter-tools",  # Required
    version=__version__,  # Required
    description=__title__,  # Required
    author=__author__,  # Optional
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={"test": ["coverage==7.4.4", "pytest==8.2.0", "pytest-cov==5.0.0", "tox==4.15.0"]},
    entry_points="""
        [console_scripts]
        xml-validate=validator.__main__:cli
    """,
)
