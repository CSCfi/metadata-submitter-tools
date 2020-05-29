# Metadata submitter tools

## XML Validation CLI

Command line tool for validating a given XML file against a specific XSD Schema.

### Installing

```
virtualenv venv
. venv/bin/activate

pip install ./xml-validator
```

### Usage

```
xml-validator [OPTIONS] XML_FILE SCHEMA_FILE

Options:
  -v, --verbose  Verbose printout for XML validation errors.
  --help         Shows help
```

### Packages/Libraries used

* [Click](https://click.palletsprojects.com/en/7.x/)
* [xmlschema](https://xmlschema.readthedocs.io/en/latest/index.html)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
