import click
import os
import requests
import xml
import xmlschema


@click.command()
@click.argument('xml_file')
@click.argument('schema_file', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True,
              help="Verbose printout for XML validation errors.")
def cli(xml_file, schema_file, verbose):
    """Validates an XML against an XSD SCHEMA."""

    """Deterimine if argument is an URL"""
    try:
        resp = requests.get(xml_file)
        if 'xml' not in resp.headers['Content-Type']:
            click.echo(f"Error: Content of the URL ({resp.url})\n" +
                       "is not in an XML format. " +
                       "Make sure the URL is correct.\n")
            return
        if resp.status_code != requests.codes.ok:
            resp.raise_for_status()
        xml_file = resp.text
        xml_from_url = True

    except requests.exceptions.HTTPError as error:
        # If request responds with HTTP error
        click.echo(str(error) + "\nMake sure the URL is correct.\n")
        return

    except ValueError:
        # If argument is an existing path to a local file
        xml_from_url = False

    if not xml_from_url and not os.path.isfile(xml_file):
        click.echo(f"Error:\nInvalid value: Path {xml_file} does not exist.\n")
        return

    """Validation"""
    try:
        xmlschema.validate(xml_file, schema=schema_file)
        # When validation succeeds
        if xml_from_url:
            click.echo(f"The XML from the URL:\n{resp.url}")
            click.secho("is valid.\n", fg='green')
        else:
            click.echo("The XML file: " +
                       click.format_filename(xml_file, shorten=True))
            click.secho("is valid.\n", fg='green')

    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        # When validation does not succeed
        if xml_from_url:
            click.echo(f"The XML from the URL:\n{resp.url}")
            click.secho("is invalid.\n", fg='red')
        else:
            click.echo("The XML file: " +
                       click.format_filename(xml_file, shorten=True))
            click.secho("is invalid.\n", fg='red')
        if verbose:
            click.secho("Error:", bold=True)
            click.echo(err)

    except xml.etree.ElementTree.ParseError as err:
        # If there is a syntax error with either file
        click.echo("Faulty XML or XSD file was given.\n")
        if verbose:
            click.echo(f"Error: {err}")


if __name__ == "__main__":
    cli()
