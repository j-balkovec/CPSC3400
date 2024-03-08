""" 
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: hw6.py
Due: Wed, Feb 28 at [22:00]

Brief: Python Regex and Definite Finite Automata

Env: Python 3.11.2 64-bit
Submission Dir: /home/fac/bdiazacosta/submit/cpsc3400/hw6_submit

Condoning to pep8 formatting standards.
"""

"""__imports__"""
import gc
import logging
import traceback
import os

import re
from typing import Pattern
import json
from datetime import datetime

"""__constants__"""
LOG = True
TRACEBACK = False
DEBUG = False

LOGGER_NAME: str = "[FILE]: hw6.py"
LOG_FILE_PATH: str = os.getcwd() + "/logs/hw6_logfile.log" if LOG else None
TEST_FILE_PATH: str = os.getcwd() + "/tests/test_output.json"

def logger_init() -> logging.Logger:
    """
    Returns:
        logging.Logger: The configured logger instance.

    Notes:
        This function sets up a logger with a specified logger name and configures it to log messages
        at the INFO level and above. It adds a FileHandler to the logger, directing log messages to a
        specified log file.
    """
    log_directory = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_directory, exist_ok=True)
  
    try:
        logger: logging.Logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        formatter: logging.Formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        file_handler: logging.FileHandler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    except Exception as e:
        print(f"[ERROR]: failed to initialize -> {e}")
        logger.error(
            f"[ERROR]: failed to initialize",
            exc_info=e,
            stack_info=True)
        logger.debug(f"[Traceback]: {traceback.print_exc()}")
        gc.collect()

    return logger

"""__init__"""
logger: logging.Logger = logger_init() if LOG else None


#----------------------------------------------------------
def strings_with_substrings() -> Pattern:
    """
    Brief: 
        Returns a compiled regular expression pattern that 
        matches strings containing both "qu" and "zz".
        
    Args: None
        
    Note:
        Regex Lookahead assertions -> 
            https://www.geeksforgeeks.org/python-regex-lookahead/
    """
    pattern: str = r"^(?=.*qu)(?=.*zz)[a-zA-Z]*$"
    logger.info(f"[(PATTERN): {pattern}") if LOG else None
    
    return re.compile(pattern)


def test_regex_pattern_a() -> list:
    """
    Brief: 
        Tests the compiled regular expression pattern returned by strings_with_substrings() 
        against a list of test strings and returns a dictionary of test results.
        
    Args: None
    
    Returns:
        dict: A dictionary containing test strings as keys and boolean match results as values.
    """
    compiled_pattern: Pattern = strings_with_substrings()
    test_results: list = []
    
    test_strings: list = [
        "quizzical",   # Valid
        "quzziical",   # Valid
        "zzquizzical", # Valid
        "aaquapizza",  # Valid
        "aquataco",    # Invalid (missing zz)
        "quizz1cal",   # Invalid (numeric characters)
        "QUIZZICAL",   # Invalid (uppercase)
    ]
    
    for test_string in test_strings:
        match: bool = bool(compiled_pattern.match(test_string))
        test_results.append({"string": test_string, "match": match})
        if LOG:
            logger.info(f"[(TEST) test_string: '{test_string}', match: {match}]")
       
    if LOG:
        logger.info(f"[(TEST_RESULTS) results:\n{json.dumps(test_results, indent=4)}]")
        
    return test_results

def phone_numbers() -> Pattern:
    """
    Biref: 
        Returns a compiled regular expression pattern that matches phone numbers in 
        the formats:
            - (###)###-#### or 
            - (###) ###-#### or
            - ###-###-#### 
    
    Args: None
    """
    pattern: str = r"^\(\d{3}\)\s?\d{3}-\d{4}$|^\d{3}-\d{3}-\d{4}$"
    logger.info(f"[(PATTERN): {pattern}") if LOG else None
    
    return re.compile(pattern)

def test_regex_pattern_b() -> list:
    """
    Brief:
        Tests the compiled regular expression pattern returned by phone_numbers() 
        against a list of test strings and returns a dictionary of test results.
    
    Args: None
    
    Returns:
        dict: A dictionary containing test strings as keys and boolean match results as values.
    """
    compiled_pattern: Pattern = phone_numbers()
    test_results: list = []
    
    test_strings: list = [
        "(555)123-4567",   # Valid
        "(555) 123-4567",  # Valid
        "555-123-4567",    # Valid
        "555123-4567",     # Invalid (missing parentheses)
        "555 123-4567",    # Invalid (incorrect space)
        "555-1234-567",    # Invalid (incorrect number of digits)
        "555-123-456",     # Invalid (incorrect number of digits)
        "abc-def-ghij",    # Invalid (non-numeric characters)
    ]
    
    for test_string in test_strings:
        match: bool = bool(compiled_pattern.match(test_string))
        test_results.append({"string": test_string, "match": match})
        if LOG:
            logger.info(f"[(TEST) test_string: '{test_string}', match: {match}]")
    
    if LOG:
        logger.info(f"[(TEST_RESULTS) results:\n{json.dumps(test_results, indent=4)}]")
        
    return test_results


def f_sharp_list() -> Pattern:
    """
    Brief: 
        Returns a compiled regular expression pattern that matches a list of 
        integers in F# list syntax.
        
    Args: None
    """
    pattern: str = r"^\[(?:[1-9]\d*|0)(?:\s*;\s*(?:[1-9]\d*|0))*]$"  
    logger.info(f"[(PATTERN): {pattern}") if LOG else None
    
    return re.compile(pattern)

def test_regex_pattern_c() -> list:
    """
    Brief: /home/st/jbalkovec/3400CPSC/HW6/pdf
        Tests the compiled regular expression pattern returned by f_sharp_list() 
        against a list of test strings and returns a list of test results.
        
    Args: None
    
    Returns:
        list: A list containing dictionaries with test string and boolean match results.
    """
    compiled_pattern: Pattern = f_sharp_list()
    test_results: list = []
    
    test_strings: list = [
        "[1]",                        # Valid
        "[1; 4; 6; 12; 3; 70]",       # Valid
        "[1;4;6;12;3;70]",            # Valid 
        "[0; 10; 20; 30; 40; 50]",    # Valid 
        "[1 ; 4 ; 6 ; 12 ; 3 ; 70]",  # Valid
        "[1;                 4]",     # Valid
        "[1; 4; 6; 12; 3; 70;]",      # Invalid (semicolon after the last integer) 
        "[1; 4; 06; 12; 3; 70]",      # Invalid (leading zero)
        "[1; 4; 6; 12; 3; abc]",      # Invalid (non-numeric character)
        "[]",                         # Invalid (empty list)
        "[1; 2; 3; 4]  ",             # Invalid (space after the list def)
        "[string; int; 4]",           # Invalid (not an integer list)
        "[1, 2, 3, 4, 5]",            # Invalid (Python style list)
    ]
    
    for test_string in test_strings:
        match: bool = bool(compiled_pattern.match(test_string))
        test_results.append({"string": test_string, "match": match})
        if LOG:
            logger.info(f"[(TEST) test_string: '{test_string}', match: {match}]")
    
    if LOG:
        logger.info(f"[(TEST_RESULTS) results:\n{json.dumps(test_results, indent=4)}]")
        
    return test_results
 
def ternary_operator_cpp_to_python(expression: str) -> str:
    """
    Brief: 
        Converts a ternary operator expression from C++ syntax to Python syntax.
    
    Args:
        expression (str): The ternary operator expression in C++ syntax.
    
    Returns:
        str: The ternary operator expression converted to Python syntax.
    """
    pattern: str = r"\s*([^?]+?)\s*\?\s*([^:]+?)\s*:\s*([^?]+?)\s*$"
    logger.info(f"[(PATTERN): {pattern}") if LOG else None
    
    re.compile(pattern)
    return re.sub(pattern, r' \2 if \1 else \3', expression)

def test_regex_pattern_d() -> list:
    """
    Brief:
        Tests the function ternary_operator_cpp_to_python() with a list of test expressions 
        and their expected results, returning a list of test results.
    
    Args: None
    
    Returns:
        list: A list of dictionaries containing test results with four fields.
    """
    test_expressions: list = [
        ("a < b ? x : 3 + y", " x if a < b else 3 + y"),
        ("1 > 2 ? 'a' : 'b'", " 'a' if 1 > 2 else 'b'"),
        ("condition ? result1 : result2", " result1 if condition else result2"),
        ("foo ? 'bar' : 'baz'", " 'bar' if foo else 'baz'"),
        ("a == b ? 1 : 2", " 1 if a == b else 2"),
        ("(a + b) < (c - d) ? x : y", " x if (a + b) < (c - d) else y"),
        ("x > 0 ? 1 : 0", " 1 if x > 0 else 0"),
    ]
    
    test_results: str = []
    for expression, expected_result in test_expressions:
        actual_result: str = ternary_operator_cpp_to_python(expression)
        match: bool = actual_result == expected_result
        test_results.append({
            "expression": expression,
            "expected_result": expected_result,
            "actual_result": actual_result,
            "match": match
        })
        if LOG:
            logger.info(f"\n[(TEST) expression: '{expression}', expected_result: {expected_result}, actual_result: {actual_result}, match: {match}\n]")
    
    if LOG:
        logger.info(f"[(TEST_RESULTS) results:\n{json.dumps(test_results, indent=4)}]")
        
    return test_results

def test_results() -> None:
    """
    Runs a series of test functions related to regex patterns and saves the results in a JSON file.

    Args:
        None

    Returns:
        None
    """
    
    meta_data = {
    "author": "Jakob Balkovec",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    test_functions: list = [
        test_regex_pattern_a,
        test_regex_pattern_b,
        test_regex_pattern_c,
        test_regex_pattern_d,
    ]

    all_test_results: dict = {}
    
    for counter, test_function in enumerate(test_functions, start=1):
        test_results: list = test_function()
        all_test_results[test_function.__name__] = test_results
        
        if DEBUG:
            print(f"\n*** TEST-[{counter}] *** [{test_function.__name__}]")
            print(json.dumps(test_results, indent=4))
            
    
    tests_directory: str = os.path.join(os.getcwd(), "tests")
    os.makedirs(tests_directory, exist_ok=True)
    
    data = [meta_data, all_test_results]
    
    with open(TEST_FILE_PATH, "w") as test_file:
        json.dump(data, test_file, indent=4)
        logger.info(f"[(TEST) test results written to the file: {TEST_FILE_PATH}]")


def clear_file(file_path: str) -> None:
    """
    Clears the contents of a file.
    """
    with open(file_path, "w") as logfile:
        logfile.seek(0)
        logfile.write("")

    return None

# As discussed over email, I attached the initial skeleton

a = re.compile(r"^(?=.*qu)(?=.*zz)[a-zA-Z]*$")

b = re.compile(r"^\(\d{3}\)\s?\d{3}-\d{4}$|^\d{3}-\d{3}-\d{4}$")

c = re.compile(r"^\[(?:[1-9]\d*|0)(?:\s*;\s*(?:[1-9]\d*|0))*]$")

d = re.compile(r"\s*([^?]+?)\s*\?\s*([^:]+?)\s*:\s*([^?]+?)\s*$")
subStr = r' \2 if \1 else \3'


# TESTS

print("----Part a tests that match:")
print(a.search("aquapizza"))

print("----Part a tests that do not match:")
print(a.search("aquataco"))

print("----Part b tests that match:")
print(b.search("(555) 123-4567"))

print("----Part b tests that do not match:")
print(b.search("(555)-123-4567"))

print("----Part c tests that match:")
print(c.search("[1; 4; 6; 12; 3; 70]"))

print("----Part c tests that do not match:")
print(c.search("[1; 4; hi; 12; 3; 70]"))

print("----Part d tests:")
print(d.sub(subStr, "a < b ? x : 3 + y"))

if __name__ == "__main__":
    clear_file(LOG_FILE_PATH)
    clear_file(TEST_FILE_PATH)
    #test_results()
    
    gc.collect()
    logger.info(f"[(STATUS): (gc module) garbo collector stats {gc.get_stats()}]") if LOG else None