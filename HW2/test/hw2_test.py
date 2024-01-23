"""
Test Script for HW2 Functions

Overview:
- This script contains unit tests for the functions defined in the 'hw2' module.
- The tests cover various scenarios to ensure the correct behavior of the functions.

Test Cases:
1.  'test_createTimeList_valid_input': Tests the 'createTimeList' function with valid input data.
2.  'test_createTimeList_empty_file': Tests the 'createTimeList' function with an empty input file.
3.  'test_createTimeList_invalid_number_of_fields': Tests the 'createTimeList' function with invalid input due to an incorrect number of fields.
4.  'test_createTimeList_wrong_field_types': Tests the 'createTimeList' function with input containing fields of the wrong data type.
5.  'test_createTimeList_improper_time_format': Tests the 'createTimeList' function with input containing improperly formatted time.
6.  'test_cast_to_int': Tests the 'cast_to_int' function to ensure correct casting of time values to integers.
7.  'test_format_times': Tests the 'format_times' function to verify the correct formatting of time values.
8.  'test_latest_time': Tests the 'latest_time' function to identify the latest time in a given list.
9.  'test_sort_times': Tests the 'sort_times' function to ensure proper sorting of time values.
10. 'test_compare_times': Tests the 'compare_times' function to validate the correct calculation of time differences.

Usage:
- Run this script to execute all defined unit tests for the 'hw2' module.
"""

import unittest
from unittest.mock import patch, mock_open
from hw2 import *

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')

class TestHW2Functions(unittest.TestCase):
    
    def test_createTimeList_valid_input(self):
        with patch('builtins.open', side_effect=lambda fname, mode: mock_open(read_data='12 30 PM\n8 45 AM\n')(fname, mode)):
            result = createTimeList(os.path.join(DATA_FOLDER, 'mocked_file.txt'))
        expected = [('12', '30', 'PM'), ('8', '45', 'AM')]
        self.assertEqual(result, expected)

    def test_createTimeList_empty_file(self):
        with patch('builtins.open', side_effect=lambda fname, mode: mock_open(read_data='')(fname, mode)):
            with self.assertRaises(CustomExceptionSuper):
                createTimeList(os.path.join(DATA_FOLDER, 'empty_file.txt'))

    def test_createTimeList_invalid_number_of_fields(self):
        with patch('builtins.open', side_effect=lambda fname, mode: mock_open(read_data='12 30 PM invalid\n8 45 AM\n')(fname, mode)):
            with self.assertRaises(InvalidNumberOfFields):
                createTimeList(os.path.join(DATA_FOLDER, 'invalid_number_of_fields.txt'))

    def test_createTimeList_wrong_field_types(self):
        with patch('builtins.open', side_effect=lambda fname, mode: mock_open(read_data='12 30 PM\n8 wrong_type AM\n')(fname, mode)):
            with self.assertRaises(WrongFieldTypes):
                createTimeList(os.path.join(DATA_FOLDER, 'wrong_field_types.txt'))

    def test_createTimeList_improper_time_format(self):
        with patch('builtins.open', side_effect=lambda fname, mode: mock_open(read_data='12 30 invalid\n8 45 AM\n')(fname, mode)):
            with self.assertRaises(ImproperTimeError):
                createTimeList(os.path.join(DATA_FOLDER, 'improper_time_format.txt'))

    def test_cast_to_int(self):
        time_list = [('12', '30', 'PM'), ('8', '45', 'AM')]
        result = cast_to_int(time_list)
        expected = [(12, 30, 'PM'), (8, 45, 'AM')]
        self.assertEqual(result, expected)

    def test_format_times(self):
        time_list = [(12, 30, 'PM'), (8, 45, 'AM')]
        result = format_times(time_list)
        expected = ['12:30 PM', '8:45 AM']
        self.assertEqual(result, expected)

    def test_latest_time(self):
        time_list = [(12, 30, 'PM'), (8, 45, 'AM'), (4, 0, 'PM')]
        result = latest_time(time_list)
        expected = (4, 0, 'PM')
        self.assertEqual(result, expected)

    def test_sort_times(self):
        time_list = [(12, 30, 'PM'), (8, 45, 'AM'), (4, 0, 'PM')]
        result = sort_times(time_list)
        expected = [(8, 45, 'AM'), (12, 30, 'PM'), (4, 0, 'PM')]
        self.assertEqual(result, expected)

    def test_compare_times(self):
        time_list = [(1, 00, 'AM'), (8, 0, 'AM'), (4, 0, 'PM'), (2, 30, 'AM')]
        result = compare_times(time_list)
        expected = [(0, 0), (7, 0), (15, 0), (1, 30)]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
