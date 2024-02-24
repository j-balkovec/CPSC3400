""" 
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: hw6.py
Due: Wed, Feb 28 at [22:00]

Brief: Python Regexes and Definite Finite Automata

Env: Python 3.11.2 64-bit
Submission Dir: /home/fac/bdiazacosta/submit/cpsc3400/hw6_submit

Condoning to pep8 formatting standards.
"""

"""__imports__"""
import gc
import logging
import traceback
import os

"""__constants__"""
LOG = True
TRACEBACK = False

LOGGER_NAME: str = "[FILE]: hw6.py"
LOG_FILE_PATH: str = os.getcwd() + "/logs/hw6_logfile.log" if LOG else None


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

'''
def clear_log_file() -> None:
    """
    Clears the hw6_logfile.log file.
    """
    with open(LOG_FILE_PATH, "w") as logfile:
        logfile.seek(0)
        logfile.write("")

    return None
'''

########




########


def main():
  logger.info("Hello world!")
  pass

if __name__ == "__main__":
    clear_log_file = lambda: (lambda logfile: [logfile.seek(0), logfile.write(''), logfile.close()])(open(LOG_FILE_PATH, 'w'))()
    main()
    
    gc.collect()
    logger.info(f"[(STATUS): (gc module) garbo collector stats {gc.get_stats()}]") if LOG else None