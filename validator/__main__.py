import click
import os
import urllib
import xml
import xmlschema


def xmlFromURL(url, arg_type):
    """Deterimine if argument is an URL and return content from the URL."""
    try:
        resp = urllib.request.urlopen(url)
        scheme = urllib.parse.urlparse(url).scheme
        if 'http' in scheme and 'xml' not in resp.info().get_content_type():
            error = (f"Error: Content of the URL ({resp.geturl()})\n" +
                     "is not in an XML format. " +
                     "Make sure the URL is correct.\n")
            raise Exception(error)
        elif scheme == 'file':
            file_path = url.replace("file://", "")
            return file_path
        else:
            return resp

    except ValueError:
        # If argument is not entered as an URL
        if not os.path.isfile(url):
            error = (f"Error: Invalid value for {arg_type}\n" +
                     f"Path {url} does not exist.\n")
            raise Exception(error)
        else:
            return None

    except urllib.error.HTTPError as err:
        # If request responds with HTTP error
        error = (str(err) + "" + url + "\nMake sure the URL is correct.\n")
        raise Exception(error)

    except urllib.error.URLError:
        error = (f"Error: Invalid value for {arg_type}\n" +
                 f"Path {url.replace('file://', '')} does not exist.\n")
        raise Exception(error)


@click.command()
@click.argument('xml_file')
@click.argument('schema_file')
@click.option('-v', '--verbose', is_flag=True,
              help="Verbose printout for XML validation errors.")
def cli(xml_file, schema_file, verbose):
    """Validates an XML against an XSD SCHEMA."""

    xml_from_url = False
    try:
        xml_resp = xmlFromURL(xml_file, 'XML_FILE')
        if xml_resp:
            xml_file = xml_resp
            xml_from_url = True

        xsd_resp = xmlFromURL(schema_file, 'SCHEMA_FILE')
        if xsd_resp:
            schema_file = xsd_resp

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

    except xmlschema.exceptions.XMLSchemaException as err:
        if not verbose:
            click.echo("\nValidation ran into an unexpected error." +
                       " Run command with --verbose option for more details\n")
        else:
            click.echo(f"Error: {err}")


if __name__ == "__main__":
    cli()
