from setuptools import setup, find_packages

from validator import __author__, __title__, __version__

setup(
    # Core metadata specification here:
    # https://packaging.python.org/specifications/core-metadata/
    name='metadata-submitter-tools',  # Required
    version=__version__,  # Required
    description=__title__,  # Required
    author=__author__,  # Optional

    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'xmlschema',
    ],
    entry_points='''
        [console_scripts]
        xml-validate=validator.__main__:cli
    ''',
)
