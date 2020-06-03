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
        assert result.exception  # catch any exception
        assert result.exit_code == 2  # catch specifically a usage error
        # self.assertRaisesRegex(SystemExit, "2", cli, [])

    def test_one_arg(self):
        """Test case where only one arg is passed."""
        filename = "SUBMISSION.xml"
        testfile = (self.xml_path / filename).as_posix()
        result = self.runner.invoke(cli, [testfile])
        assert result.exception  # catch any exception
        assert result.exit_code == 2  # catch specifically a UsageError
        # self.assertRaisesRegex(SystemExit, "2", cli, [testfile])

    def test_too_many_args(self):
        """Test case where three args are passed."""
        xml_name = "SUBMISSION.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd, xsd])
        assert result.exception  # catch any exception
        assert result.exit_code == 2  # catch specifically a UsageError
        #  self.assertRaisesRegex(SystemExit, "2", cli, [xml, xsd, xsd])

    def test_valid_submission_file(self):
        """Test case for a valid submission xml file."""
        xml_name = "SUBMISSION.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])
        assert result.exit_code == 0  # script exits correctly
        assert result.output == xml + " is valid.\n\n"  # correct output
        # self.assertRaisesRegex(SystemExit, "0", cli, [xml, xsd])
        # self.assertEqual(result.output, xml + " is valid.\n\n")

    def test_invalid_submission_file(self):
        """Test case for an invalid submission xml file."""
        xml_name = "invalid_SUBMISSION.xml"
        xsd_name = "SRA.submission.xsd"
        xml = (self.xml_path / xml_name).as_posix()
        xsd = (self.xsd_path / xsd_name).as_posix()
        result = self.runner.invoke(cli, [xml, xsd])
        assert result.exit_code == 0  # script exits correctly
        assert result.output == xml + " is invalid.\n\n"  # correct output
        # self.assertRaisesRegex(SystemExit, "0", cli, [xml, xsd])
        # self.assertEqual(result.output, xml + " is valid.\n\n")


if __name__ == '__main__':
    unittest.main()
