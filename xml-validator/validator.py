import click
import xmlschema
import xml

@click.command()
@click.argument('xml_file', type=click.Path(exists=True))
@click.argument('schema_file', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, \
                help="Verbose printout for XML validation errors.")
def cli(xml_file, schema_file, verbose):
    """Validates an XML against an XSD SCHEMA."""

    try:
        xmlschema.validate(xml_file, schema=schema_file)
        click.echo(f"{click.format_filename(xml_file)} is valid.\n")

    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        click.secho(f"{click.format_filename(xml_file)} is invalid.\n", fg='red')
        if verbose:
            click.secho("Error:", bold=True)
            click.echo(err)

    except xml.etree.ElementTree.ParseError as err:
        click.echo("Faulty XML or XSD file was given.\n")
        if verbose:
            click.echo(f"Error: {err}")
