import unittest
# import click
# from pathlib import Path
from click.testing import CliRunner

from validator.__main__ import cli


class TestXMLValidator(unittest.TestCase):
    """Test for XML validator tool.

    Testing the command line functions.
    """
    # TESTFILES_ROOT = Path(__file__).parent / 'test_files'

    def setUp(self):
        """Initialise CLI runner."""
        self.runner = CliRunner()

    def tearDown(self):
        """Remove setup variables."""
        pass

    def test_no_args(self):
        """If no args are passed"""
        result = self.runner.invoke(cli, [])
        assert result.exception  # finding any exception
        assert result.exit_code == 2  # finding specifically a usage error

    def test_one_arg(self):
        """If only one arg is passed"""
        # filename = "SUBMISSION.xml"
        testfile = "./test_files/SUBMISSION.xml"
        result = self.runner.invoke(cli, [testfile])
        assert result.exception  # finding any exception
        assert result.exit_code == 2  # finding specifically a UsageError


if __name__ == '__main__':
    unittest.main()
