from setuptools import setup

setup(
    name='xml-validator',
    version='0.1',
    py_modules=['validator'],
    install_requires=[
        'Click',
        'xmlschema',
    ],
    entry_points='''
        [console_scripts]
        xml-validator=validator:cli
    ''',
)
