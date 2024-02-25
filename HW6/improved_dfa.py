""" 
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: improved_dfa.py
Brief: Definite Finite Automata
Env: Python 3.11.2 64-bit
"""

import sys
import json

"""__file_constants__"""
DFA0: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/sample-dfa.txt"
DFA0_TESTS: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/sample-tests.txt"

DFA1: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/dfa1.txt"
DFA1_TESTS: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/dfa1_test_strings.txt"

DFA2: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/dfa2.txt"
DFA2_TESTS: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/dfa2_test_strings.txt"

DFA3: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/dfa3.txt"
DFA3_TESTS: str = r"/home/st/jbalkovec/3400CPSC/HW6/data/dfa3_test_strings.txt"

DFA_FILES = {
    "test0": (DFA0, DFA0_TESTS),
    "test1": (DFA1, DFA1_TESTS),
    "test2": (DFA2, DFA2_TESTS),
    "test3": (DFA3, DFA3_TESTS),            
}

def read_dfa(filename):
    """
    Reads the DFA file and returns the input alphabet, DFA transitions, and accepting states.

    Args:
        filename (str): The filename of the DFA file.

    Returns:
        tuple: A tuple containing the input alphabet, DFA transitions, and accepting states.
    """
    with open(filename, 'r') as dfa_file:
        alpha_line = dfa_file.readline()
        alpha = alpha_line.split()
        dfa = []
        accepting = []
        state = 0
        for line in dfa_file:
            entry = {}
            line_list = line.split()
            if line_list[0] == '+':
                accepting.append(state)
            line_list = line_list[1:]
            line_list = [int(x) for x in line_list]
            dfa.append(dict(zip(alpha, line_list)))
            state += 1
    return alpha, dfa, accepting

def process_strings(alpha, dfa, accepting, filename):
    """
    Processes strings using the DFA and returns the results.

    Args:
        alpha (list): The input alphabet.
        dfa (list): The DFA transitions.
        accepting (list): The list of accepting states.
        filename (str): The filename of the strings file.

    Returns:
        list: A list of dictionaries representing the results for each string.
    """
    results = []
    with open(filename, 'r') as str_file:
        for line in str_file:
            line = line.strip()
            state = 0
            for c in line:
                state = dfa[state][c]
            result = "[ACCEPTED]" if state in accepting else "[REJECTED]"
            results.append({"string": line, "final_state": state, "result": result})
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python improved_dfa.py <test>")
        return

    test = sys.argv[1]
    if test not in DFA_FILES:
        print("Invalid test name.")
        return

    dfa_filename, strings_filename = DFA_FILES[test]

    try:
        alpha, dfa, accepting = read_dfa(dfa_filename)
        results = process_strings(alpha, dfa, accepting, strings_filename)
        print(json.dumps({f"{test}": results}, indent=4))
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

