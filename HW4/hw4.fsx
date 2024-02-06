//{
//  @course: CPSC 3400
//  @author: Jakob Balkovec
//  @instructor: B. Diaz Acosta
//
//  @file: hw2.py
//  @due: Mon, Feb 12th [22:00]
//
//  @submission_dir: /home/fac/bdiazacosta/submit/cpsc3400/hw4_submit
//
//  @brief
//
//  This file contains three F# exercises for homework 4:
//  1. replace list origVal newVal
//    Replace each occurrence of origVal in list with newVal.
//  2. mergeList listA listB
//    Merge two lists alternately.
//  3. Dictionary functions:
//    - search: Returns the value corresponding to a given key.
//    - insert: Inserts a key-value pair into the dictionary if the key is not already present.
//    - remove: Removes a key-value pair from the dictionary if the key is present.
//    - count: Counts the number of elements satisfying a given condition.
//    - twoDigitCount: Counts the number of entries with a two-digit positive integer value.
//}


// [Problem 1]

let rec replace (list: int list) (origVal: int) (newVal: int) =
    match list with
    | [] -> []
    | firstElement::restOfList when firstElement = origVal -> newVal :: replace restOfList origVal newVal
    | firstElement::restOfList -> firstElement :: replace restOfList origVal newVal



// [Problem 2]

let rec mergeList (listA: int list) (listB: int list) =
    match listA, listB with
    | [], [] -> []
    | [], remainingList -> remainingList          // unnecessary, but makes the program faster
    | remainingList, [] -> remainingList          // unnecessary, but makes the program faster
    | headA::tailA, headB::tailB -> headA :: headB :: mergeList tailA tailB
