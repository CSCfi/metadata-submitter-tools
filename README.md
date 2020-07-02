[![Build Status](https://travis-ci.com/CSCfi/metadata-submitter-tools.svg?branch=master)](https://travis-ci.com/CSCfi/metadata-submitter-tools)

# Metadata submitter tools

## XML Validation CLI

Command-line tool for validating a given XML file against a specific XSD Schema.

### Installing

Note: The tool requires Python 3.6+

Clone the project and install with `pip`:
```
git clone https://github.com/CSCfi/metadata-submitter-tools.git
cd metadata-submitter-tools
pip install .
```

### Tests

Tests can be executed with tox automation:
```
# Install tox first if not installed
pip install tox
# Run tests
tox
```

### Usage

After installation, the validation tool is used by by executing `xml-validate` in a terminal with specified options/arguments followingly:

```
xml-validate <option> <xml-file> <schema-file>
```

The `<xml-file>` and `<schema-file>` arguments need to be the correct filenames (including path) of a local XML file and the corresponding XSD file.
The `<option>` can be `--help` for showing help and `-v` or `--verbose` for delivering a detailed validation error message.

Below is a terminal demonstration of the usage of this tool, which displays the different outputs the CLI will produce:

[![asciicast](https://asciinema.org/a/ykioH41E9Y38fG404hReQedyc.svg)](https://asciinema.org/a/ykioH41E9Y38fG404hReQedyc)

### Packages/Libraries used

* [Click](https://click.palletsprojects.com/en/7.x/)
* [xmlschema](https://xmlschema.readthedocs.io/en/latest/index.html)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contibuting

If you want to contribute to a project and make it better, your help is very welcome. For more info about how to contribute, see [CONTRIBUTING](CONTRIBUTING.md).
