""" 
Course: CPSC 3400
Author: Jakob Balkovec
Instructor: B. Diaz Acosta

File: improved_dfa.py
Brief: Definite Finite Automata
Env: Python 3.11.2 64-bit
"""

import sys
from typing import List, Tuple, Dict, Set, NoReturn

def read_dfa(filename: str) -> Tuple[List[str], List[Dict[str, int]], Set[int]]:
    """
    Reads a DFA (Deterministic Finite Automaton) from a file.

    Args:
        filename (str): The name of the file containing the DFA.

    Returns:
        tuple: A tuple containing the following:
            - alpha (list): The input alphabet of the DFA.
            - dfa (list): A list of dictionaries representing the DFA transitions.
            - accepting_states (set): A set containing the accepting states of the DFA.
    """
    dfa: List[Dict[str, int]] = [] 
    accepting_states: Set[int] = set()
    with open(filename, 'r') as file:
        alpha: List[str] = file.readline().split()
        for line in file:
            line: str = line.strip().split()  
            state: int = int(line[0])  
            if '+' in line:
                accepting_states.add(state)  
                line.remove('+')  
            transitions: Dict[str, int] = {alpha[i]: int(line[i]) for i in range(len(alpha))} 
            dfa.append(transitions)
    return alpha, dfa, accepting_states

def simulate_dfa(alpha: List[str], dfa: List[Dict[str, int]], accepting_states: Set[int], string: str) -> str:
    """
    Simulates a DFA (Deterministic Finite Automaton) on an input string.

    Args:
        alpha (List[str]): The input alphabet of the DFA.
        dfa (List[Dict[str, int]]): A list of dictionaries representing the DFA transitions.
        accepting_states (Set[int]): A set containing the accepting states of the DFA.
        string (str): The input string to be processed by the DFA.

    Returns:
        str: The result of the DFA simulation, either "ACCEPTED" or "REJECTED".
    
    Raises:
        ValueError: If any character in the input string is not in the DFA's input alphabet.
    """
    state: int = 0  
    for c in string:
        if c not in alpha:
            raise ValueError(f"Character '{c}' is not in the alphabet.")
        state: int = dfa[state][c]
    return "ACCEPTED" if state in accepting_states else "REJECTED"

def main() -> NoReturn:
    """
    The main function of the DFA (Deterministic Finite Automaton) simulator.

    Parses command-line arguments, reads the DFA and input strings from files, 
    simulates the DFA on each input string, and prints the results.

    Args:
        None

    Returns:
        None
    """
    if len(sys.argv) != 3:
        print("Usage: python dfa_simulator.py <dfa_file> <string_file>")
        sys.exit(1)

    dfa_file: str = sys.argv[1]
    str_file: str = sys.argv[2]

    try:
        alpha, dfa, accepting_states = read_dfa(dfa_file)
        with open(str_file, 'r') as file:
            for line in file:
                line: str = line.strip()
                result: str = simulate_dfa(alpha, dfa, accepting_states, line)
                print(f"String: {line} Final state: {result}")
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
