"""
tree:
.
├── backup
│   └── hw2.py~
├── data
│   ├── empty_file.txt
│   ├── improper_time_format.txt
│   ├── invalid_number_of_fields.txt
│   ├── mocked_file.txt
│   ├── sample.txt
│   └── wrong_field_types.txt
├── hw2.py
├── logs
│   └── hw2_logfile.log
├── output
│   ├── actual.txt
│   └── expected.txt
├── pdf
│   └── Homework 2.pdf
├── __pycache__
│   └── hw2.cpython-36.pyc
└── test
    └── hw2_test.py
    
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: hw2.py
Due: Wed, Jan 24th [22:00]

Brief: Implementation of functions to process times in a given text file, 
       counting their occurrences and performing additional processing.
       Involves custom error raising and handling.

Env: Python 3.11.2 64-bit
Submission Dir: /home/fac/bdiazacosta/submit/cpsc3400/hw2_submit

Condoning to pep8 formatting standards.

Overview: The output has been redirected to the "actual_output.txt" file, and a comparison was made with the expected output. 
          The command shell did not yield any results

          The custom defined errors were tested through a unit-test script and with multiple files that should raise those errors
          10/10 tests passed, with the appropriate error being thrown

          Script can be found at
"""

"""__imports__"""
import gc
import logging
import traceback
import os
import sys
from abc import ABC, abstractmethod
from typing import Any

"""__constants__"""
LOG = True
TRACEBACK = False

LOGGER_NAME: str = "[FILE]: hw2.py"
LOG_FILE_PATH: str = os.getcwd() + "/logs/hw2_logfile.log" if LOG else None


class CustomExceptionSuper(Exception, ABC):
    """
    Abstract base class for custom exceptions.

    Usage:
        This class is intended to be subclassed by specific custom exception classes.

    Dependencies:
        Exception class
        ABC class (from abc module)

    Attributes:
        message (str): A string representing the error message.

    Methods:
        __init__(self, message="[DEFAULT]"): Initializes the custom exception with an optional error message.
        __repr__(self) -> str: Returns a formal string representation for debugging purposes.
        what(self) -> None: Abstract method to print detailed information about the custom exception.
    """

    def __init__(self, message="[DEFAULT]"):
        super().__init__(message)
        self.message = message

    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns a formal string representation of the object. 

        Attention:
            This method is intended to be used for debugging and logging only.

        Returns:
            str: A string representation of the object suitable for debugging and development purposes.

        Usage:
            >>> print(repr(instance))
        """
        pass

    @abstractmethod
    def what(self) -> str:
        """
        Prints detailed information about the custom exception. Mimics the functionality of the what() method in C++

        This method prints the error message, the number of fields, the expected number of fields,
        and the traceback information. It is designed to provide comprehensive details for debugging purposes.

        Returns:
            None

        Usage:
            >>> instance.what()
        """
        pass


class InvalidNumberOfFields(CustomExceptionSuper):
    """__custom_exception_class__

    Dependencies: 
            Exception class
            CustomExceptionSuper (abstract base class)
    Description: 
            Custom exception class for invalid number of fields in a line of a file.
                 To be invoked upon reaching an invalid number of fields in a line of a file.

    Attributes:
            message (str): A string representing the error message.
            fields_count (int): An integer representing the number of fields in the line.
            expected_fields (int): An integer representing the expected number of fields in the line.

    Usage: 
            raise InvalidNumberOfFields("Custom error message")
    """

    """__ctor__"""

    def __init__(self: object, fields_count: int, expected_fields: int, message: str = "[DEFAULT]") -> None:
        """
        Initializes the custom exception for an invalid number of fields in a line.

        Args:
            fields_count (int): The actual number of fields in the line.
            expected_fields (int): The expected number of fields.
            message (str, optional): An optional error message. Defaults to "[DEFAULT]".

        Attributes:
            fields_count (int): The actual number of fields in the line.
            expected_fields (int): The expected number of fields.
            message (str): A string representing the error message.

        Usage:
            >>> raise InvalidNumberOfFields(fields_count=2, expected_fields=3, message="Custom error message")

        Raises:
            InvalidNumberOfFields: This exception is raised with detailed information about the invalid number of fields.
        """
        self.fields_count: int = fields_count
        self.expected_fields: int = expected_fields

        MESSAGE: str = " Invalid number of fields in line"
        self.message: str = MESSAGE

        super().__init__(self.message)

    def __repr__(self: object) -> str:
        """__repr__
            Documented in AB class.
        """

        return f"[ERROR]: {self.message}"

    def what(self: object) -> str:
        """__what__
            Documented in AB class.
        """
        return f"{self.message}" + ", expected: " + f"[{self.expected_fields}]" + " but found: " + f"[{self.fields_count}]" + "\n"


class WrongFieldTypes(CustomExceptionSuper):
    """__custom_exception_class__

    Dependencies: 
            Exception class
            CustomExceptionSuper (abstract base class)

    Description: 
            Custom exception class for invalid number of fields in a line of a file.
                 To be invoked upon reaching an invalid number of fields in a line of a file.

    Attributes:
            message (str): A string representing the error message.
            fields_count (int): An integer representing the number of fields in the line.
            expected_fields (int): An integer representing the expected number of fields in the line.

    Usage: 
            raise InvalidNumberOfFields("Custom error message")
    """

    def __init__(self: object, filed_type: Any, expected_type: Any, message: str = "[DEFAULT]"):
        """
        Initializes the custom exception for wrong field types.

        Description:
            This exception is raised when there is a mismatch between the actual field type and the expected field type.

        Args:
            field_type (type): The actual type of the field.
            expected_type (type): The expected type of the field.
            message (str, optional): An optional error message. Defaults to "Default error message".

        Attributes:
            message (str): A string representing the error message.
            field_type (type): The actual type of the field.
            expected_type (type): The expected type of the field.
        """
        MESSAGE: str = " Invalid field type in line"
        self.message: str = MESSAGE

        self.filed_type: Any = filed_type
        self.expected_type: Any = expected_type

        super().__init__(self.message)

    def __repr__(self) -> str:
        """__repr__
            Documented in AB class.
        """
        return f"[ERROR]: {self.message}"

    def what(self) -> str:
        """__what__
            Documented in AB class.
        """
        return f"{self.message}" + ", expected: " + f"[{self.expected_type}]" + " but found: " + f"[{self.filed_type}]" + "\n"


class ImproperTimeError(Exception):
    """
    Custom exception class for an improper time format.

    This exception is raised when an invalid time format is encountered in a line.

    Args:
        invalid_line (str): The line containing the invalid time format.
        message (str, optional): An optional error message. Defaults to "[DEFAULT]".

    Attributes:
        invalid_line (str): The line containing the invalid time format.
        message (str): A string representing the error message.
    """

    def __init__(self: object, invalid_line: str, message: str = "[DEFAULT]"):
        """
        Initializes the custom exception for an improper time format.

        Args:
            invalid_line (str): The line containing the invalid time format.
            message (str, optional): An optional error message. Defaults to "[DEFAULT]".

        Attributes:
            invalid_line (str): The line containing the invalid time format.
            message (str): A string representing the error message.
        """
        MESSAGE: str = " Invalid time format"
        self.message: str = MESSAGE

        self.invalid_line: str = invalid_line
        super().__init__(message)

    def __repr__(self) -> str:
        """__repr__
            Documented in AB class.
        """
        return f"[ERROR]: {self.message}"

    def what(self) -> str:
        """__what__
            Documented in AB class.
        """
        return f"{self.message}" + ", expected format: [HH MM (AM/PM)]" + f" but found: [{self.invalid_line}]" + "\n"


class EmptyFileError(Exception):
    """Custom exception class."""

    def __init__(self: object, file_size: int, message: str = "[DEFAULT]"):
        MESSAGE: str = " File is empty"
        self.message: str = MESSAGE

        self.file_size: int = file_size
        super().__init__(message)

    def __repr__(self) -> str:
        """__repr__
            Documented in AB class.
        """
        return f"[ERROR]: {self.message}"

    def what(self) -> str:
        """__what__
            Documented in AB class.
        """
        return f"{self.message}" + ", expected [size > 0], but found size to be: " + f"[{self.file_size}]" + "\n"


def clear_log_file() -> None:
    """
    Clears the hw2_logfile.log file.
    """
    with open(LOG_FILE_PATH, "w") as logfile:
        logfile.seek(0)
        logfile.write("")

    return None


def logger_init() -> logging.Logger:
    """
    Returns:
        logging.Logger: The configured logger instance.

    Notes:
        This function sets up a logger with a specified logger name and configures it to log messages
        at the INFO level and above. It adds a FileHandler to the logger, directing log messages to a
        specified log file.
    """
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


def createTimeList(input_file: str) -> list:
    """_summary_

    Parameters: Name of the input file (string)

    Returns: A list of time tuples. Each time tuple has three elements in this order: (hours- integer,
             minutes - integer, AM / PM - string). The function is also capable of throwing exceptions (see
             description).

    Description: Reads a text file (the name of the file is stored in the parameter filename) consisting
                 of times and returns a list of time tuples. Each line in the file represents a single time, and the order
                of the items in the list must match the order in the file.
    """
    EXPECTED_FIELDS_IN_LINE: int = 3
    AM_CONSTANT: str = "AM"
    PM_CONSTANT: str = "PM"

    time_list: list = []

    with open(input_file, 'r') as file:
        logger.info(f"[(STATUS) file opened: {not file.closed}]") if LOG else None

        """__brief__
            * Check if file is empty using tell() method. If the pointer is at the beginning of the file, 
              the file is empty.

            * Check if the file exists using os.path.exists() method. If not, raise and exit scope.
        """
        if os.stat(input_file).st_size == 0:
            raise EmptyFileError(file_size=os.stat(input_file).st_size)

        elif not os.path.exists(input_file):
            raise FileNotFoundError(f" File: {input_file} not found")

        for line in file:
            fields = line.strip().split()

            num_of_fields = len(fields)

            if num_of_fields != 3:
                raise InvalidNumberOfFields(
                    fields_count=num_of_fields, expected_fields=EXPECTED_FIELDS_IN_LINE)

            elif not fields[0].isdigit() or not fields[1].isdigit() or fields[2].isdigit():
                raise WrongFieldTypes(filed_type=str, expected_type=str)

            elif not (1 <= int(fields[0]) <= 12) or not (0 <= int(fields[1]) <= 59) or not (fields[2] == AM_CONSTANT or fields[2] == PM_CONSTANT):
                raise ImproperTimeError(invalid_line=line)

            hours, minutes, am_pm = fields
            time_list.append((hours, minutes, am_pm))

    logger.info(f"[(STATUS) data read: {time_list is not None}]") if LOG else None
    logger.info(f"[(STATUS) file closed: {file.closed}]") if LOG else None

    return time_list


def timeCompareGen(times: list, target: tuple) -> tuple:
    """
    Generates tuples representing the time differences in hours and minutes between each time in the input list
    and the target time.

    Parameters:
        times (list): A list of time tuples, where each tuple has three elements: (hours - integer,
                             minutes - integer, AM/PM - string).
        target (tuple): A tuple representing the target time (hours - integer, minutes - integer, AM/PM - string).

    Returns:
        tuple: A tuple containing the time differences in hours and minutes for each input time.
    """
    if times is None or target is None:
        logger.error(
            f"[(STATUS) [supposedly None!] times: {times is None}, target: {target is None}]") if LOG else None
        
        raise ValueError(
            f" entries cannot be [None] times: {times is None}, target: {target is None}"
        )

    if len(times) == 0 or target == ():
        logger.error(
            f"[(STATUS) [supposedly empty!] times: {len(times) == 0}, target: {target == ()}]") if LOG else None
        
        raise ValueError(
            f" entries cannot be [empty] times: {len(times) == 0}, target: {target == ()}"
        )

    target_hours, target_minutes, target_am_pm = target
    
    logger.info(
        f"[(STATUS) target set: {target_hours}:{target_minutes} {target_am_pm}]") if LOG else None
    
    for hours, minutes, am_pm in times:
        
        '''__edge_case__
        change to 24hr format "maunally" for edge casses
        '''
        if hours == 12:
            if am_pm == 'PM':
                hours = 24
            else:
                hours = 0
        else:
            pass
        
        hours: int = (int(hours) + 12) % 24 if am_pm == 'PM' else int(hours)
        target_hours_24 = (
            int(target_hours) + 12) % 24 if target_am_pm == 'PM' else int(target_hours)
    
        time_difference_minutes = (
            hours - target_hours_24) * 60 + int(minutes) - int(target_minutes)
        
        logger.info(
            f"[(STATUS)[for {(hours, minutes, am_pm)}] time difference in minutes set: {time_difference_minutes}]") if LOG else None

        hours_difference = time_difference_minutes // 60
        minutes_difference = time_difference_minutes % 60
        
        if hours_difference < 0 or (hours_difference == 0 and minutes_difference < 0):
            hours_difference = 12 if hours_difference == 0 else 24 + hours_difference

        logger.info(
            f"[(STATUS) time difference set (yielded the following): {hours_difference}:{minutes_difference}]") if LOG else None
        
        yield (hours_difference, minutes_difference)

def fetch_filename() -> str:
    """
    Retrieves the input filename from the command line arguments.

    Returns:
        str: The input filename provided as a command line argument.
    """
    try:
        if len(sys.argv) < 2:
            raise ValueError("[Usage]: python3 hw2.py <file_name>")

        input_filename: str = sys.argv[1]

    except ValueError as argv_error:
        print(f"{argv_error}")
        logger.error(
            "[(STATUS) [argv_error] sys.argv:",
            exc_info=argv_error,
            stack_info=True) if LOG else None
        logger.debug(f"Traceback: {traceback.print_exc()}") if TRACEBACK and LOG else None
        gc.collect()

    return input_filename


def cast_to_int(time_list: list) -> list:
    """
    Casts the hours and minutes in the input time list to integers.

    Parameters:
        time_list (list): A list of time tuples, where each tuple has three elements: (hours - integer,
                                 minutes - integer, AM/PM - string).

    Returns:
        list: A list of time tuples with the hours and minutes cast to integers.
    """
    int_list = [(int(hours), int(minutes), am_pm)
                for hours, minutes, am_pm in time_list]
    
    logger.info(f"[(STATUS) casted from str to int: {int_list}]") if LOG else None
    return int_list


def format_times(time_list: list) -> list:
    """
    Returns a list of formatted time strings.

    Parameters:
        time_list (list): A list of time tuples, where each tuple has three elements: (hours - integer,
                                 minutes - integer, AM/PM - string).

    Returns:
        list: A list of formatted time strings.
    """
    formatted_times = [
        f"{hours}:{minutes} {am_pm}" for hours, minutes, am_pm in time_list]
    
    logger.info(f"[(STATUS) formatted times: {formatted_times}]") if LOG else None
    return formatted_times


def latest_time(time_list: list) -> tuple:
    """
    Returns the latest time in the input list.

    Parameters:
        time_list (list): A list of time tuples, where each tuple has three elements: (hours - integer,
                                 minutes - integer, AM/PM - string).

    Returns:
        tuple: A tuple representing the latest time in the input list.
    """
    int_list = cast_to_int(time_list)
    latest_time = max(int_list, key=lambda t: (
        t[0] + 12 if t[2] == 'PM' and t[0] < 12 else t[0], t[1]))
    
    logger.info(f"[(STATUS) latest time: {latest_time}]") if LOG else None
    return latest_time


def sort_times(time_list: list) -> list:
    """
    Returns a sorted list of time tuples.

    Parameters:
        time_list (list): A list of time tuples, where each tuple has three elements: (hours - integer,
                                 minutes - integer, AM/PM - string).

    Returns:
        list: A sorted list of time tuples.
    """
    int_list = cast_to_int(time_list)
    sorted_times = sorted(int_list, key=lambda t: (
        t[0] % 12 + 12 if t[2] == 'PM' and t[0] != 12 else t[0], t[1]))
    
    logger.info(f"[(STATUS) sorted times: {sorted_times}]") if LOG else None
    return sorted_times


def compare_times(time_list: list) -> list:
    """
    Returns a list of time differences in hours and minutes between each time in the input list and the target time.

    Parameters:
        time_list (list): A list of time tuples, where each tuple has three elements: (hours - integer,
                                 minutes - integer, AM/PM - string).
        target (tuple): A tuple representing the target time (hours - integer, minutes - integer, AM/PM - string).

    Returns:
        list: A list of time differences in hours and minutes between each time in the input list and the target time.
    """
    int_list = cast_to_int(time_list)
    target = time_list[0]
    time_differences = list(timeCompareGen(int_list, target))
    logger.info(f"[(STATUS) time differences: {time_differences}]") if LOG else None
    return time_differences


def handle_custom_ab_derived_exceptions(e: CustomExceptionSuper) -> None:
    """
    Handles custom exceptions derived from the CustomExceptionSuper class.

    Parameters:
        e (CustomExceptionSuper): A custom exception derived from the CustomExceptionSuper class.
    """
    print(f"[ERROR]: {e.what()}")
    logger.error(
        f"[(STATUS) [custom_exception] {e.what()}]",
        exc_info=e,
        stack_info=True) if LOG else None
    logger.debug(f"Traceback: {traceback.print_exc()}") if LOG and TRACEBACK else None
    gc.collect()


def handle_default_exceptions(e: Exception) -> None:
    """
    Handles default exceptions.

    Parameters:
        e (Exception): A default exception.
    """
    print(f"[ERROR]: {e}")
    logger.error(
        f"[(STATUS) [default_exception] {e}]",
        exc_info=e,
        stack_info=True) if LOG else None
    logger.debug(f"Traceback: {traceback.print_exc()}") if LOG and TRACEBACK else None
    gc.collect()


def main(filename: str) -> None:
    """
    Main function that processes a file containing time data.

    Args:
        filename (str): The path to the input file.

    Returns:
        None
    """
    try:
        timeList = createTimeList(input_file=filename)
        print(format_times(timeList))
        print(latest_time(timeList))
        print(sort_times(timeList))
        print(compare_times(timeList)) 

    except (InvalidNumberOfFields, WrongFieldTypes, ImproperTimeError, EmptyFileError) as custom_exception:
        handle_custom_ab_derived_exceptions(custom_exception)

    except Exception as default_exception:
        handle_default_exceptions(default_exception)

    finally:
        timeList = None # Help the garbo collector


if __name__ == "__main__":
    clear_log_file() if LOG else None
    filename: str = fetch_filename()
    main(filename)
    
    filename = None
    
    logger.info(f"[(STATUS): garbo collector stats {gc.get_stats()}]") if LOG else None
    logger = None
    gc.collect()
