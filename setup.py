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
    extras_require={"test": ["coverage==7.0.5", "pytest==7.2.1", "pytest-cov==4.0.0", "tox==4.3.5"]},
    entry_points="""
        [console_scripts]
        xml-validate=validator.__main__:cli
    """,
)
