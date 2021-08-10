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
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "test": ["coverage==5.5", "pytest==6.2.4", "pytest-cov==2.12.1", "coveralls==3.2.0", "tox==3.24.1"]
    },
    entry_points="""
        [console_scripts]
        xml-validate=validator.__main__:cli
    """,
)
