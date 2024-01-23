"""
tree:

    
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: hw2.py
Due: Wed, Jan 31st [22:00]

Brief: Implementation of functions to process times in a given text file, 
       counting their occurrences and performing additional processing.
       Involves custom error raising and handling.

Env: Python 3.11.2 64-bit
Submission Dir: /home/fac/bdiazacosta/submit/cpsc3400/hw3_submit

Condoning to pep8 formatting standards.
"""

"""__imports__"""
import gc
import logging
import traceback
import os
import sys

import csv

"""__constants__"""
LOG = True
TRACEBACK = False

LOGGER_NAME: str = "[FILE]: hw3.py"
LOG_FILE_PATH: str = os.getcwd() + "/logs/hw3_logfile.log" if LOG else None

class CustomGarboCollector():
  pass
      
def clear_log_file() -> None:
    """
    Clears the hw3_logfile.log file.
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

def main(filename: str) -> None:
  garbo_collector: CustomGarboCollector = CustomGarboCollector()
  garbo_collector.process_file(filename)
  garbo_collector.debug()

if __name__ == "__main__":
    clear_log_file() if LOG else None
    filename: str = fetch_filename()
    main(filename)
    
    filename = None
    
    logger.info(f"[(STATUS): garbo collector stats {gc.get_stats()}]") if LOG else None
    logger = None
    gc.collect()
