import click
import os
import requests
import xml
import xmlschema
import ftplib
from urllib.parse import urlparse
from io import StringIO

# Change environment variables for Click commands to work
os.environ['LC_ALL'] = 'en_US.utf-8'
os.environ['LANG'] = 'en_US.utf-8'


def xmlFromURL(url, arg_type):
    """Deterimine if argument is an URL and return content from the URL."""
    try:
        # Handle FTP or file URLs
        scheme = urlparse(url).scheme
        if scheme == 'file':
            raise ValueError
        elif scheme == 'ftp':
            host = urlparse(url).netloc
            path = urlparse(url).path
            ftp = ftplib.FTP(host)
            ftp.login()
            r = StringIO()
            ftp.retrlines('RETR ' + path, r.write)
            content = r.getvalue()
            r.close()
            # Remove null bytes from the output to avoid unexpected errors
            if '\x00' in content:
                content = content.replace('\x00', '')
            return content

        # Handle HTTP and HTTPS URLs
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            resp.raise_for_status()
        elif 'http' in scheme and 'xml' not in resp.headers['Content-Type']:
            error = (f"Error: Content of the URL ({resp.url})\n" +
                     "is not in XML format. " +
                     "Make sure the URL is correct.\n")
            raise Exception(error)
        else:
            return resp

    except ValueError:
        # If argument is a file URL type or not an URL at all
        if scheme == 'file':
            url = url.replace('file://', '')
        if not os.path.isfile(url):
            error = (f"Error: Invalid value for {arg_type}\n" +
                     f"Path {url} does not exist.\n")
            raise Exception(error)
        else:
            return None

    except requests.exceptions.HTTPError as err:
        # If request responds with HTTP error
        error = (str(err) + "" + url + "\nMake sure the URL is correct.\n")
        raise Exception(error)

    except ftplib.Error as err:
        # If request responds with FTP error
        error = (str(err) + f" ({url})\nMake sure the URL is correct.\n")
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
            xml_file = xml_resp.text
            xml_from_url = True

        xsd_resp = xmlFromURL(schema_file, 'SCHEMA_FILE')
        if xsd_resp:
            schema_file = str(xsd_resp)

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
    # Revert environment variables back
    os.unsetenv['LC_ALL']
    os.unsetenv['LANG']
