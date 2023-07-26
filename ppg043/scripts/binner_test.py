import os
import tempfile
import unittest
import numpy as np
import pandas as pd
from binner import find_bins

class TestFindBins(unittest.TestCase):
    def setUp(self):
        # Create temporary input file with test data
        self.input_file = tempfile.NamedTemporaryFile(delete=False)
        self.input_file.write(b'1 2 3\n2 4 6\n3 6 9\n4 8 12\n')
        self.input_file.close()

    def tearDown(self):
        # Remove temporary input file
        os.remove(self.input_file.name)

    def test_find_bins_default_output_file(self):
        # Call find_bins with default output file
        find_bins(self.input_file.name)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.input_file.name.split('.')[0] + '_binned.txt'))

        # Check that output file contains expected data
        expected_output = 'x y y_stat\n1.0 2.0 3.0\n2.0 4.0 6.0\n3.0 6.0 9.0\n'
        with open(self.input_file.name.split('.')[0] + '_binned.txt', 'r') as f:
            self.assertEqual(f.read(), expected_output)

    def test_find_bins_custom_output_file(self):
        # Create temporary output file
        output_file = tempfile.NamedTemporaryFile(delete=False)
        output_file.close()

        # Call find_bins with custom output file
        find_bins(self.input_file.name, output_file.name)

        # Check that output file was created
        self.assertTrue(os.path.exists(output_file.name))

        # Check that output file contains expected data
        expected_output = 'x y y_stat\n1.0 2.0 3.0\n2.0 4.0 6.0\n3.0 6.0 9.0\n'
        with open(output_file.name, 'r') as f:
            self.assertEqual(f.read(), expected_output)

        # Remove temporary output file
        os.remove(output_file.name)

    def test_find_bins_no_output_file(self):
        # Call find_bins with no output file
        find_bins(self.input_file.name)

        # Check that output file was created
        self.assertTrue(os.path.exists(self.input_file.name.split('.')[0] + '_binned.txt'))

        # Remove output file
        os.remove(self.input_file.name.split('.')[0] + '_binned.txt')

    def test_find_bins_missing_input_file(self):
        # Call find_bins with missing input file
        with self.assertRaises(FileNotFoundError):
            find_bins('missing_file.txt')

    def test_find_bins_missing_x_column(self):
        # Create temporary input file with missing 'x' column
        input_file = tempfile.NamedTemporaryFile(delete=False)
        input_file.write(b'1 2\n2 4\n3 6\n4 8\n')
        input_file.close()

        # Call find_bins with missing 'x' column
        with self.assertRaises(ValueError):
            find_bins(input_file.name)

        # Remove temporary input file
        os.remove(input_file.name)

if __name__ == '__main__':
    unittest.main()