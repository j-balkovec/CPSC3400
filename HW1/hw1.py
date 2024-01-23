"""
tree:
.
├── backup
│   └── hw1.py~
├── data
│   ├── py.txt
│   ├── sample_1.txt
│   ├── sample_2.txt
│   ├── sample_3.txt
│   └── sample.txt
├── hw1.py
├── logs
│   └── hw1_logfile.log
├── output
│   ├── output_2.txt
│   ├── output.txt
│   └── x_output.txt
├── __pycache__
│   ├── hw1.cpython-36.pyc
│   └── unittest.cpython-36.pyc
└── test
    └── hw1_test.py

Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: hw1.py
Due: Wed, Jan 17th [22:00]

Brief: Implementation of functions to process two-letter pairs in a given text file, 
       counting their occurrences and performing additional processing.
       
Enviroment: Python 3.11.2 64-bit
Pckg Manager on cs1: yum
Submission Dir: /home/fac/bdiazacosta/submit/cpsc3400/hw1_submit
"""

"""__imports__"""
import sys
import gc
import os
import logging
import traceback

"""__constants__"""
LOG: bool = True

LOG_FILE_PATH: str = os.getcwd() + "/logs/hw1_logfile.log" if LOG else None
LOGGER_NAME: str = "[file]: hw1.py"

def clear_log_file() -> None:
  """
  Clears the hw1_logfile.log file if it exists.
  """
  if LOG and os.path.exists(LOG_FILE_PATH):
    with open(LOG_FILE_PATH, "w") as logfile:
      logfile.seek(0)
      logfile.write("")
  else:
    pass
  
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
    logger.setLevel(logging.INFO)
    
    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    file_handler: logging.FileHandler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
  
  except FileNotFoundError as fnfe:
    print(f"[FAIL]\n[Error]: file not found -- {fnfe}")
    gc.collect()
    sys.exit()
    
  except Exception as e:
    print(f"[FAIL]\n[Error]: -- {e}")
    gc.collect()
    sys.exit()

  return logger

"""__init__"""
logger: logging.Logger = logger_init() if LOG else None

def countPairs(filename: str) -> dict:
  """
    Parameters: 
      - Name of the input file (string)
    Returns: 
      - A dictionary that has two letter strings as keys and the frequency as the value
      
    Description: 
      - Reads a text file and returns a dictionary that has two letter pairs as keys and the
        frequency as the value. The dictionary only contains pairs that appear in the file.
    Assumptions: 
      - The input file exists and contains at least one pair 
  """
  pairs: list = []
  pairs_count: dict = {}
  
  try:
    if os.stat(filename).st_size == 0:
      raise ValueError(f"{filename} is empty")

    with open(filename, 'r') as file:    
      logger.info(f"[(STATUS) file opened: {not file.closed}]") if LOG else None
      
      data = [line.strip().lower() for line in file]
      logger.info(f"[(STATUS) data read: {data is not None}]") if LOG else None
      
      pairs = [line[i : i + 2] for line in data for i in range(len(line) - 1) if line[i : i + 2].isalpha()]
      pairs_count = {pair: pairs.count(pair) for pair in set(pairs)}
      logger.info(f"[(STATUS) pairs set: {pairs is not None}]") if LOG else None
          
  except FileNotFoundError as fnfe:
    print(f"[File]: {filename} not found!")
    logger.error(f"[File]: {filename} not found!", exc_info=fnfe, stack_info=True) if LOG else None
    logger.debug(f"[Traceback]: {traceback.print_exc()}") if LOG else None
    gc.collect()
    sys.exit()
  
  except ValueError as ve:
    print(f"Error: {ve}")
    logger.error(f"{filename} is empty", exc_info=ve, stack_info=True) if LOG else None
    logger.debug(f"[Traceback]: {traceback.print_exc()}") if LOG else None
    gc.collect()
    sys.exit()
    
  finally:
    #file.close() -- No need to explicitly call close() due to the use of 'with open(...)'
    pass
  
  logger.info(f"[pairs]: {pairs}") if LOG else None
  logger.info(f"[pairs_count]: {pairs_count}") if LOG else None

  return pairs_count

def getTopFivePairs(data: dict) -> list:
  """
  Parameters: 
    - Dictionary returned from countPairs
  Returns: 
    - A list of tuples. Each tuple in the list has two entries: the first entry is a two letter string
      and the second entry is an integer.
      
  Description:
    - Creates and returns a list of that contains the top five most frequent pairs in order
      from the most frequent to the least frequent. The pairs must be tuples like this: ('an', 4). 
      If there is a tie, place the pair that is alphabetically earlier first. If there is a tie such that multiple
      pairs could occupy the last (5th) position, include all such pairs (this means the list could contain
      more than five pairs). If there are fewer than five pairs, simply return the appropriate list with
      fewer than five pairs.
"""
  # Use sorted to sort by freq, and use a lambda(x) to sort by key
  sorted_pairs: list = sorted(data.items(), key=lambda x: (-x[1], x[0]))
  logger.info(f"[sorted pairs]: {sorted_pairs}") if LOG else None
  
  # Find the freq of the 5th element in case there is a tie
  fifth_frequency = sorted_pairs[4][1] if len(sorted_pairs) >= 5 else 0
  logger.debug(f"[fifth_frequency]: {fifth_frequency}") if LOG else None 
  
  # Use a helper lambda to filter
  result: list = list(filter(lambda pair: pair[1] >= fifth_frequency, sorted_pairs))
  
  result = sorted(result, key=lambda x: (-x[1], x[0]))
  logger.info(f"[result]: {result}") if LOG else None
  
  return result 

def createFollowsDict(data: dict, vowel: str) -> dict:
  """
  Parameters: 
    - Dictionary returned from countPairs, a single letter
    - Vowel for which to create the follows dictionary
  Returns:
    - A dictionary where individual letters are the keys and integers are the values.
    
  Description:
    - Creates and returns a dictionary that has each letter in the alphabet as a key and the
      frequency of how often that letter follows the given letter (parameter) in the dictionary. This
      dictionary must have 26 entries in it - one for each letter. If a letter never follows the given letter,
      a dictionary entry of zero must be present.
  """
  DEFAULT_VALUE: int = 0

  # Create the alphabet dictionary
  alphabet_dict: dict = {chr(letter): DEFAULT_VALUE for letter in range(ord('a'), ord('z')+1)}
  logger.info(f"[initial/default alphabet_dict]: {alphabet_dict}") if LOG else None

  # Update values with the corresponding key
  for pair, frequency in data.items():
      first_letter = pair[0]
      if first_letter == vowel:
          alphabet_dict[pair[1]] += frequency

  logger.info(f"[updated alphabet_dict]: {alphabet_dict}") if LOG else None
  return alphabet_dict

def get_dict_info(data: dict) -> None:
  """
  Parameters:
    - Dictionary returned from countPairs
  
  Description:
    - Prints the length of the keys in the dictionary and the sum of the frequencies in the values.
  """
  num_of_keys: int = len(data.keys())
  sum_of_freq: int = sum(freq for _, freq in data.items()) # Use _ to discard
  
  print(num_of_keys)
  print(sum_of_freq)
  logger.info(f"[dict_info]: # of keys: {num_of_keys}\t sum of freq: {sum_of_freq}") if LOG else None

def process_vowels(pairs: dict) -> None:
  """
  Process vowels in the given pairs dictionary.

  For each vowel (a, e, i, o, and u):
  a. Print the vowel used during this iteration (a single character).
  b. Call createFollowsDict with pairs and the vowel for this iteration.
  c. Using a list comprehension on the dictionary returned from part b, create a list of 26
      integers such that the first element of the list is the frequency of 'a', the second element
      is the frequency of 'b', etc.
  d. Print the list from step c.

  Parameters:
  - pairs (dict): Dictionary containing two-letter pairs and their frequencies.
  """
  count: int = 0
  VOWELS = ['a', 'e', 'i', 'o', 'u']
  for vowel in VOWELS:
    print(f"{vowel}")
    
    follows_dict = createFollowsDict(data=pairs, vowel=vowel)
    freq_list = [follows_dict.get(chr(letter), 0) for letter in range(ord('a'), ord('z')+1)]
    print(freq_list)
    
    logger.info(f"[vowel \'{VOWELS[count]}\' processed]: {freq_list}") if LOG else None
    count+=1
  
def fetch_filename() -> str:
  """
  Retrieves the input filename from the command line arguments.

  Returns:
      str: The input filename provided as a command line argument.
  """
  input_filename: str = ""
  try:
    if len(sys.argv) < 2:
      raise UnboundLocalError("[Usage]: python3 hw1.py <file_name>")
    
    input_filename: str = sys.argv[1] 
    logger.info(f"[filename]: {input_filename}") if LOG else None
    
  except UnboundLocalError as argv_error:
    print(f"{argv_error}")
    logger.error(f"[Error]: argv_error", exc_info=argv_error, stack_info=True) if LOG else None
    logger.debug(f"Traceback: {traceback.print_exc()}") if LOG else None
    gc.collect()
    sys.exit()
   
  return input_filename

def main(input_file: str, **kwargs) -> None:
  """
  Main function, entry point fo the script
  """
  pairs: dict = countPairs(filename=input_file)
  get_dict_info(data=pairs)

  print(getTopFivePairs(data=pairs))
  process_vowels(pairs)

    
if __name__ == "__main__":
  clear_log_file()
  filename = fetch_filename()
  main(filename)
  
  # Cleanup
  del logger
  gc.collect()

