#Unit tests for Judoon

import unittest
from mock import patch, mock_open
import sys

from StringIO import StringIO
import argparse
from judoon import Judoon


class JudoonOutput(unittest.TestCase):
    """
    Tests the output from Judoon
    """
    def setUp(self):
        self.stdoutActual = sys.stdout
        sys.stdout = StringIO()
        self.args = ['judoon.py', '-h']
        self.argvActual = sys.argv
        sys.argv = self.args
        self.retval = ''
        pass

    def tearDown(self):
        sys.stdout = self.stdoutActual
        print("Captured stdout: '%s'" % self.retval)


    @patch.object(argparse.ArgumentParser, 'exit')
    def test_noOptions_returns_help(self, mockParser):
        cli = Judoon()
        cli.roTroNo()
        self.retval = sys.stdout.getvalue().strip()
        expected = 'usage:'
        self.assertRegexpMatches(self.retval, expected)

    """@patch('__main__.open', mock_open(), create=True)
    def test_fromFile_imports_file(self):
        self.args = ['judoon.py', 'fakeFile.txt', 'faketest']
        cli=Judoon()
        cli.roTroNo()
        self.retVal"""



if __name__ == "__main__":
    unittest.main()
