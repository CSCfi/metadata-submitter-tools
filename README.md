[![Build Status](https://travis-ci.com/CSCfi/metadata-submitter-tools.svg?branch=master)](https://travis-ci.com/CSCfi/metadata-submitter-tools)

# Metadata submitter tools

## XML Validation CLI

Command line tool for validating a given XML file against a specific XSD Schema.

### Installing

Clone the project and install with: `pip install .`

### Tests

Tests can be executed with tox automation:
```
# pip install tox (if not installed)
tox
```

### Usage

```
xml-validate [OPTIONS] XML_FILE SCHEMA_FILE

Options:
  -v, --verbose  Verbose printout for XML validation errors.
  --help         Shows help.
```

### Packages/Libraries used

* [Click](https://click.palletsprojects.com/en/7.x/)
* [xmlschema](https://xmlschema.readthedocs.io/en/latest/index.html)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contibuting

If you want to contribute to a project and make it better, your help is very welcome. For more info about how to contribute, see [CONTRIBUTING](CONTRIBUTING.md).
