import click
import os
import requests
import xml
import xmlschema


def xmlFromURL(url, arg_type):
    """Deterimine if argument is an URL and return content from the URL."""
    try:
        resp = requests.get(url)
        if 'xml' not in resp.headers['Content-Type']:
            error = (f"Error: Content of the URL ({resp.url})\n" +
                     "is not in an XML format. " +
                     "Make sure the URL is correct.\n")
            raise Exception(error)
        elif resp.status_code != requests.codes.ok:
            resp.raise_for_status()
        else:
            return resp

    except ValueError:
        # If argument is an existing path to a local file
        if not os.path.isfile(url):
            error = (f"Error: Invalid value for {arg_type}\n" +
                     f"Path {url} does not exist.\n")
            raise Exception(error)
        else:
            return None

    except requests.exceptions.HTTPError as error:
        # If request responds with HTTP error
        error = (str(error) + "\nMake sure the URL is correct.\n")
        raise Exception(error)


@click.command()
@click.argument('xml_file')
@click.argument('schema_file')
@click.option('-v', '--verbose', is_flag=True,
              help="Verbose printout for XML validation errors.")
def cli(xml_file, schema_file, verbose):
    """Validates an XML against an XSD SCHEMA."""

    xml_from_url = False
    #xsd_from_url = False
    try:
        xml_resp = xmlFromURL(xml_file, 'XML_FILE')
        if xml_resp:
            xml_file = xml_resp.text
            xml_from_url = True

        xsd_resp = xmlFromURL(schema_file, 'SCHEMA_FILE')
        if xsd_resp:
            schema_file = xsd_resp.text
            #xsd_from_url = True

    except Exception as error:
        click.echo(error)
        return

    try:
        xmlschema.validate(xml_file, schema=schema_file)
        # When validation succeeds
        if xml_from_url:
            click.echo(f"The XML from the URL:\n{xml_resp.url}")
            click.secho("is valid.\n", fg='green')
        else:
            click.echo("The XML file: " +
                       click.format_filename(xml_file, shorten=True))
            click.secho("is valid.\n", fg='green')

    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        # When validation does not succeed
        if xml_from_url:
            click.echo(f"The XML from the URL:\n{xml_resp.url}")
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
