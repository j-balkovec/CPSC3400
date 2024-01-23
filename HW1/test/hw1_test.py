"""
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: hw1_test.py
Due: Wed, Jan 17th [22:00]

Brief: Unit tests for the HW1 script
       
Env: Python 3.11.2 64-bit
Pckg Manager on cs1: yum
Submission Dir: None
"""

import unittest
import tempfile
import os
import sys
import unittest.mock
import gc
    
from hw1 import countPairs, getTopFivePairs, createFollowsDict, process_vowels, fetch_filename

class TestHW1Functions(unittest.TestCase):
    """
    A test suite for the functions in the HW1 script.

    Attributes:
        test_file_content (str): Sample content for the temporary test file.
        test_file (file): A temporary file for testing.
    """
    def setUp(self):
        """
        Set up the necessary resources for each test case.
        """
        self.test_file_content = "hello world\npython is great\n"
        self.test_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.test_file.write(self.test_file_content)
        self.test_file.close()

    def tearDown(self):
        """
        Clean up the resources after each test case.
        """
        os.unlink(self.test_file.name)
        gc.collect()

    def test_countPairs(self):
        """
        Test the countPairs function.

        Verifies if the function correctly counts two-letter pairs in a given file.
        """
        expected_result = {'el': 1, 'th': 1, 'ho': 1, 'on': 1, 're': 1, 'wo': 1, 'ld': 1, 'is': 1, 'rl': 1, 'lo': 1, 'or': 1, 'gr': 1, 'll': 1, 'he': 1, 'ea': 1, 'at': 1, 'py': 1, 'yt': 1}
        result = countPairs(self.test_file.name)
        self.assertEqual(result, expected_result)

    def test_getTopFivePairs(self):
        """
        Test the getTopFivePairs function.

        Verifies if the function correctly retrieves the top five pairs from a given data dictionary.
        """
        data = {'el': 1, 'th': 1, 'ho': 1, 'on': 1, 're': 1, 'wo': 1, 'ld': 1, 'is': 1, 'rl': 1, 'lo': 1, 'or': 1, 'gr': 1, 'll': 1, 'he': 1, 'ea': 1, 'at': 1, 'py': 1, 'yt': 1}
        expected_result = [('at', 1), ('ea', 1), ('el', 1), ('gr', 1), ('he', 1), ('ho', 1), ('is', 1), ('ld', 1), ('ll', 1), ('lo', 1), ('on', 1), ('or', 1), ('py', 1), ('re', 1), ('rl', 1), ('th', 1), ('wo', 1), ('yt', 1)]
        result = getTopFivePairs(data)
        self.assertEqual(result, expected_result)

    def test_createFollowsDict(self):
        """
        Test the createFollowsDict function.

        Verifies if the function correctly creates a follows dictionary for a given data dictionary and vowel.
        """
        data = {'el': 1, 'th': 1, 'ho': 1, 'on': 1, 're': 1, 'wo': 1, 'ld': 1, 'is': 1, 'rl': 1, 'lo': 1, 'or': 1, 'gr': 1, 'll': 1, 'he': 1, 'ea': 1, 'at': 1, 'py': 1, 'yt': 1}
        expected_result = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 1, 'o': 0, 'p': 0, 'q': 0, 'r': 1, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}
        result = createFollowsDict(data, 'o')
        self.assertEqual(result, expected_result)

    def test_process_vowels(self):
        """
        Test the process_vowels function.

        Verifies if the function correctly processes vowels for a given data dictionary.
        """
        data = {'el': 1, 'th': 1, 'ho': 1, 'on': 1, 're': 1, 'wo': 1, 'ld': 1, 'is': 1, 'rl': 1, 'lo': 1, 'or': 1, 'gr': 1, 'll': 1, 'he': 1, 'ea': 1, 'at': 1, 'py': 1, 'yt': 1}
        with unittest.mock.patch('builtins.print') as mock_print:
            process_vowels(data)
            mock_print.assert_called_with([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def test_fetch_filename(self):
        """
        Test the fetch_filename function.

        Verifies if the function correctly retrieves the input filename from command line arguments.
        """
        sys.argv = ['hw1.py', 'test_file.txt']
        result = fetch_filename()
        self.assertEqual(result, 'test_file.txt')

if __name__ == '__main__':
    unittest.main()
