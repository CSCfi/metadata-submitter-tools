import unittest
from click.testing import CliRunner
from pathlib import Path

from validator.__main__ import cli


class TestXMLValidator(unittest.TestCase):
    """Test for XML validator tool.

    Testing the command line functions.
    """
    TESTFILES_ROOT = Path(__file__).parent / 'test_files'

    def setUp(self):
        """Initialise CLI runner and set paths to test files."""
        self.runner = CliRunner()

        # XML files and Schemas as published by ENA
        self.xml_path = self.TESTFILES_ROOT / 'xml'
        self.xsd_path = self.TESTFILES_ROOT / 'schemas'

    def tearDown(self):
        """Remove setup variables."""
        pass

    def test_no_args(self):
        """Test case where no args are passed."""
        result = self.runner.invoke(cli, [])

        # Exit with code 2 (UsageError)
        self.assertEqual(result.exit_code, 2)
        # The specific error message in output
        self.assertIn("Error: Missing argument 'XML_FILE'", result.output)

    def test_one_arg(self):
        """Test case where only one arg is passed."""
        filename = "SUBMISSION.xml"
        testfile = (self.xml_path / filename).as_posix()
        result = self.runner.invoke(cli, [testfile])

        # Exit with code 2 (UsageError)
        self.assertEqual(result.exit_code, 2)
        # The specific error message in output
        self.assertIn("Error: Missing argument 'SCHEMA_FILE'", result.output)

    def test_too_many_args(self):
        """Test case where three args are passed."""
        xml_name = "SUBMISSION.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd, xsd])

        # Exit with code 2 (UsageError)
        self.assertEqual(result.exit_code, 2)
        # The specific error message in output
        self.assertIn("Error: Got unexpected extra argument", result.output)

    def test_bad_filepath(self):
        """Test case where an incorrect file path is given as an arg."""
        xml_name = "no_xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The specific error message in output
        self.assertIn("Error: Invalid value for XML_FILE", result.output)

    def test_faulty_xml_file(self):
        """Test case for xml with incorrect xml syntax."""
        xml_name = "bad_syntax.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertEqual("Faulty XML or XSD file was given.\n\n",
                         result.output)

    def test_valid_sample_file(self):
        """Test case for a valid sample xml file."""
        xml_name = "SAMPLE.xml"
        xsd_name = "SRA.sample.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertEqual("The XML file: SAMPLE.xml\nis valid.\n\n",
                         result.output)

    def test_valid_study_file(self):
        """Test case for a valid study xml file."""
        xml_name = "STUDY.xml"
        xsd_name = "SRA.study.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertEqual("The XML file: STUDY.xml\nis valid.\n\n",
                         result.output)

    def test_valid_submission_file(self):
        """Test case for a valid submission xml file."""
        xml_name = "SUBMISSION.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertEqual("The XML file: SUBMISSION.xml\nis valid.\n\n",
                         result.output)

    def test_invalid_submission_file(self):
        """Test case for an invalid submission xml file."""
        xml_name = "invalid_SUBMISSION.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertIn("The XML file: invalid_SUBMISSION.xml\nis invalid.",
                      result.output)

    def test_valid_xml_against_wrong_schema(self):
        """Test case for a valid xml file against the wrong schema."""
        xml_name = "SUBMISSION.xml"
        xsd_name = "SRA.sample.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertEqual("The XML file: SUBMISSION.xml\nis invalid.\n\n",
                         result.output)

    def test_valid_xml_from_url(self):
        """Test validating XML from URL."""
        xml_url = "https://www.ebi.ac.uk/ena/browser/api/xml/SAMEA2620084"
        xsd_name = "SRA.sample.xsd"
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml_url, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertIn("The XML from the URL:\n" + xml_url + "\nis valid.\n\n",
                      result.output)

    def test_xml_error(self):
        xml_url = "https://www.ebi.ac.uk/ena/browser/api/xml/wrong_indicator"
        xsd_name = "SRA.sample.xsd"
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml_url, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertIn("HTTP Error 400", result.output)

    def test_url_to_non_xml(self):
        xml_url = "https://www.example.com"
        xsd_name = "SRA.sample.xsd"
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml_url, xsd])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertIn("Error: Content of the URL", result.output)

    def test_schema_from_ftp_url(self):
        xml_name = "SUBMISSION.xml"
        xsd_url = ("ftp://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/"
                   "SRA.submission.xsd")
        xml = (self.xml_path / xml_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd_url])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertEqual("The XML file: SUBMISSION.xml\nis valid.\n\n",
                         result.output)

    def test_both_args_as_urls(self):
        xml_url = "https://www.ebi.ac.uk/ena/browser/api/xml/SAMEA2620084"
        xsd_url = ("ftp://ftp.ebi.ac.uk/pub/databases/ena/doc/xsd/sra_1_5/"
                   "SRA.sample.xsd")

        result = self.runner.invoke(cli, [xml_url, xsd_url])

        # Exit correctly with code 0
        self.assertEqual(result.exit_code, 0)
        # The correct output is given
        self.assertIn("The XML from the URL", result.output)
        self.assertIn("is valid.", result.output)

    # TODO add inline comments


if __name__ == '__main__':
    unittest.main()
