import click
import xmlschema
import xml
import requests


@click.command()
@click.argument('xml_file', type=click.Path())
@click.argument('schema_file', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True,
              help="Verbose printout for XML validation errors.")
def cli(xml_file, schema_file, verbose):
    """Validates an XML against an XSD SCHEMA."""
    try:
        # Checking if the given argument was an URL
        resp = requests.get(xml_file)
        if 'xml' not in resp.headers['Content-Type']:
            click.echo("Content of the URL is not in an XML format. " +
                       "Make sure the URL is correct.\n")
            return
        if resp.status_code != requests.codes.ok:
            resp.raise_for_status()
        xml_file = resp.text
        xml_from_url = True

    except requests.exceptions.HTTPError as error:
        click.echo(str(error) + "\nMake sure the URL is correct.\n")
        return

    except ValueError:
        # If argument is entered as a path to a local file
        xml_from_url = False

    # TODO handle errors from path bad paths (URLError)

    try:
        xmlschema.validate(xml_file, schema=schema_file)
        # If validation succeeds
        if xml_from_url:
            click.echo(f"The XML from the URL:\n{resp.url}")
            click.secho("is valid.\n", fg='green')
        else:
            click.echo("The XML file: " +
                       click.format_filename(xml_file, shorten=True))
            click.secho("is valid.\n", fg='green')
    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        # If validation does not succeed
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
