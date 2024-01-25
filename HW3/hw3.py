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

Improvements:
    - Shortened the documentation
"""

"""__imports__"""
import gc
import logging
import traceback
import os
import sys
from typing import Callable # decorator

"""__constants__"""
LOG = True
TRACEBACK = False

LOGGER_NAME: str = "[FILE]: hw3.py"
LOG_FILE_PATH: str = os.getcwd() + "/logs/hw3_logfile.log" if LOG else None


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


def clear_log_file() -> None:
    """
    Clears the hw3_logfile.log file.
    """
    with open(LOG_FILE_PATH, "w") as logfile:
        logfile.seek(0)
        logfile.write("")

    return None


def private_method(func: Callable) -> Callable:
    """
    Brief:
        A decorator to mark a method as private within the CustomGarboCollector (CGC) class.
    Parameters:
        Callable: The method to be decorated.
        
    Returns:
        Callable: A wrapper function that raises an AttributeError when called.
    Note:
        - This method was created because Python does not allow strict access control.
        - The client should not access "internal/private" methods, but should only call the 
          "public" method provided
          
        - Follows the Facade pattern: (https://en.wikipedia.org/wiki/Facade_pattern)
        - Follows POLA (https://en.wikipedia.org/wiki/Principle_of_least_astonishment)
    """
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, CustomGarboCollector):
            raise AttributeError(f"{func.__name__} is a private method in the CGC class and prefers not to be called directly.")
        return func(self, *args, **kwargs)
    
    return wrapper


class CustomGarboCollector:
    """
    A custom garbage collector class for managing heap memory.

    Attributes:
    - heap (list): A list to store heap objects.
    - heap_ptrs (list): A list to store pointers to heap objects.

    Methods:
    - mark(roots): Mark reachable objects in the heap.
    - sweep(size, marked): Sweep unreferenced objects from the heap.
    - read_file(filename): Read a file containing heap information.
    - gb_collect(filename): Perform garbage collection based on the file content.
    """
    def __init__(self):
        """
        Initialize the CustomGarboCollector.

        The constructor initializes the heap and heap_ptrs attributes.
        """
        self.heap: list = []
        self.heap_ptrs: list = []

    @private_method
    def mark(self, roots):
        """
        Mark reachable objects in the heap.

        Args:
        - roots (list): The root objects from which marking starts.

        Returns:
        - set: A set of marked objects.
        """
        marked = set()
        logger.info(f"[(STATUS) marked set to: {marked}") if LOG else None
        
        logger.info(f"[(STATUS) roots: {roots}") if LOG else None
        while roots:
            temp = roots.pop()
            for ptr, pointed in self.heap:
                if ptr == temp:
                    marked.add(pointed)
                    roots.append(pointed)
        
        logger.info(f"[(STATUS) marked updated to: {marked}") if LOG else None
        return marked

    @private_method
    def sweep(self, size, marked):
        """
        Sweep unreferenced objects from the heap.

        Args:
        - size (int): The size of the heap.
        - marked (set): The set of marked objects.

        Returns:
        - set: A set of swept objects.
        """
        swept = set(range(size)) - marked
        logger.info(f"[(STATUS) swept nodes: {swept}]") if LOG else None
        return swept

    @private_method
    def read_file(self, filename) -> bool:
        """
        Read a file containing heap information.

        Args:
        - filename (str): The name of the file to be read.

        Prints:
        - The marked and swept nodes based on heap information.
        """
        if os.stat(input_file).st_size == 0:
            raise ValueError(file_size=os.stat(input_file).st_size)

        elif not os.path.exists(input_file):
            raise FileNotFoundError(f" File: {input_file} not found")
        
        with open(filename) as input_file:
            size = int(input_file.readline().rstrip())
            logger.info(f"[(STATUS) number of nodes {size}]") if LOG else None

            for line in input_file:
                pointer, pointee = map(str.strip, line.rstrip().split(','))
                logger.info(f"[(STATUS) pointer: {pointer}, pointee: {pointee}]") if LOG else None

                if pointer[0].isalpha() or pointer[0] == "_":
                    self.heap.append((pointer, int(pointee)))
                    self.heap_ptrs.append(pointer)
                else:
                    self.heap.append((int(pointer), int(pointee)))

            marked_nodes = self.mark(self.heap_ptrs)
            logger.info(f"[(STATUS) marked_nodes: {marked_nodes}]") if LOG else None
            
            swept_nodes = self.sweep(size, marked_nodes)
            logger.info(f"[(STATUS) swept_nodes: {swept_nodes}]") if LOG else None

            print("[marked nodes]: " + " ".join(map(str, sorted(marked_nodes))))
            print("[swept nodes]:  " + " ".join(map(str, sorted(swept_nodes))))
        return True
    
    def gb_collect(self, filename) -> None:
        """
        Perform garbage collection based on the file content.

        Args:
        - filename (str): The name of the file containing heap information.
        """
        if self.read_file(filename) == True:
            logger.debug("[(SUCCESS)]")
        else:
            logger.debug("[(FAIL)]")    
        
        return None


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
    """
    Brief:
        The main function for executing garbage collection based on a specified file.

    Parameters:
        - filename (str): The name of the file containing heap information.

    Returns:
        None
    """
    clear_log_file() if LOG else None
    
    try:
        custom_gc = CustomGarboCollector()
        custom_gc.gb_collect(filename)
        
    except AttributeError as attr_error:
        print(f"[ERROR] func_call: {attr_error}")
        logger.error(
            f"[(ERROR) func_call: {attr_error}",
            exc_info=attr_error,
            stack_info=True) if LOG else None
        logger.debug(f"Traceback: {traceback.print_exc()}") if TRACEBACK and LOG else None
    
    except ValueError as val_error:
        print(f"[ERROR]: {val_error}")
        logger.error(
            f"[(ERROR) value error: {val_error}",
            exc_info=val_error,
            stack_info=True) if LOG else None
        logger.debug(f"Traceback: {traceback.print_exc()}") if TRACEBACK and LOG else None
        
    except FileNotFoundError as file_error:
        print(f"[ERROR]: {file_error}")
        logger.error(
            f"[(ERROR) file not found error: {file_error}",
            exc_info=file_error,
            stack_info=True) if LOG else None
        logger.debug(f"Traceback: {traceback.print_exc()}") if TRACEBACK and LOG else None
           

if __name__ == "__main__":
    main(filename=fetch_filename())
    
    gc.collect()
    logger.info(f"[(STATUS): (gc module) garbo collector stats {gc.get_stats()}]") if LOG else None
   
