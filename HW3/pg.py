# Kevin Bui
# hw3.py
# 4/26/23
# This program simulates a mark-sweep algorithm using sets and lists

import sys

def mark(heap, roots): # function to mark all accessible blocks
    marked = set()
    
    while roots != []:
        temp = roots.pop() # sorts through all named pointers first
        for ptr, pointed in heap:
            if ptr == temp: # if the pointer is accessible, the heap block is accessible
                marked.add(pointed)
                roots.append(pointed)
    return marked

def sweep(size, marked):
    swept = set(range(size)) - marked # the swept set is determined using set operations
    return swept

# Main

inFile = open(sys.argv[1])

heap = []

heapPtrs = []

size = int(inFile.readline().rstrip())

for line in inFile:
    pointer, pointed = line.rstrip().split(',') # splits input line into two with comma as delimiter
    if pointer[0].isalpha() or pointer[0] == "_": # possible first characters for a variable name
        heap.append((pointer, int(pointed)))
        heapPtrs.append(pointer) # stores variable names in a list for marking
    else:
        heap.append((int(pointer), int(pointed)))

marked = mark(heap, heapPtrs)
swept = sweep(size, marked)


print("Marked nodes: " + " ".join(str(value) for value in sorted(marked))) # sorts the set and returns a sorted list
print("Swept nodes: "+ " ".join(str(value) for value in sorted(swept)))

inFile.close()