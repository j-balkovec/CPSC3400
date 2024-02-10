//{
//  @course: CPSC 3400
//  @author: Jakob Balkovec
//  @instructor: B. Diaz Acosta
//
//  @file: hw4.fsx
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

// Function: exists
// Description: Checks if any element in the list satisfies the given predicate.
// Parameters:
//   - predicate: A function that takes an element of type 'a and returns a boolean indicating whether the element satisfies a condition.
//   - list: The list of elements of type 'a to search.
// Returns: true if any element in the list satisfies the predicate, false otherwise.
let rec exists (predicate: 'a -> bool) (list: 'a list) =
    match list with
    | [] -> false
    | head::tail when predicate head -> true
    | _::tail -> exists predicate tail

// Function: replace
// Description: Replaces all occurrences of a value in a list with a new value.
// Parameters:
//   - list: The list of elements of type 'a.
//   - origVal: The value to be replaced.
//   - newVal: The new value to replace the original value.
// Returns: A new list with all occurrences of origVal replaced by newVal, or the original list if origVal is not found.
let rec replace (list: 'a list) (origVal: 'a) (newVal: 'a) =
    match list with
    | [] -> []
    | _ when not (exists (fun x -> x = origVal) list) -> list
    | head::tail when head = origVal -> newVal :: replace tail origVal newVal
    | head::tail -> head :: replace tail origVal newVal

// [Problem 2]

// Function: mergeList
// Description: Merges two lists in alternating fashion.
// Parameters:
//   - listA: The first list of elements of type 'a.
//   - listB: The second list of elements of type 'a.
// Returns: A new list obtained by merging listA and listB in alternating fashion.
//   - The first element of the result is the first element of listA,
//     the second element is the first element of listB,
//     the third element is the second element of listA,
//     and so on, until one of the lists is exhausted.
//   - If one list is longer than the other, the remaining elements of the longer list are appended to the result.
let rec mergeList (listA: 'a list) (listB: 'a list) =
    match listA, listB with
    | [], [] -> []
    | [], second -> second
    | first, [] -> first
    | firstHead::firstTail, secondHead::secondTail -> firstHead :: secondHead :: mergeList firstTail secondTail

// [Problem 3]

// Function: search
// Description: Searches for a key in the dictionary and returns its associated value.
// Parameters:
//   - dict: The dictionary implemented as a list of key-value pairs.
//   - key: The key to search for in the dictionary.
// Returns: Some value if the key is found, None if the key is not found.
let search dict key =
    let rec searchHelper dict key =
        match dict with
        | [] -> None 
        | (k, v)::tail -> if k = key then Some v else searchHelper tail key
    searchHelper dict key

// Function: insert
// Description: Inserts a key-value pair into the dictionary if the key does not already exist.
// Parameters:
//   - dict: The dictionary implemented as a list of key-value pairs.
//   - key: The key to insert.
//   - value: The value associated with the key.
// Returns: The dictionary with the key-value pair inserted, or the original dictionary if the key already exists.
let insert dict key value =
    //[NOTE]: returns an option (Some value is key is found else None), hence the use of Option.isSome
    if Option.isSome (search dict key) then 
        dict
    else
        (key, value) :: dict

// Function: reverseList
// Description: Reverses a list.
// Parameters:
//   - list: The list to be reversed.
// Returns: A new list with the elements of the input list in reverse order.
let reverseList list =
    let rec reverseHelper acc list =
        match list with
        | [] -> acc
        | head::tail -> reverseHelper (head :: acc) tail
    reverseHelper [] list

// Function: remove
// Description: Removes a key-value pair from the dictionary if the key exists.
// Parameters:
//   - dict: The dictionary implemented as a list of key-value pairs.
//   - key: The key to remove from the dictionary.
// Returns: The dictionary with the key-value pair removed, or the original dictionary if the key does not exist.
let remove dict key =
    let rec removeHelper acc dict key =
        match dict with
        | [] -> reverseList acc
        | (k, v)::tail ->
            if k = key then
                reverseList acc @ tail 
                // "optimized" by IDE
                //[link] https://learn.microsoft.com/en-us/dotnet/fsharp/language-reference/symbol-and-operator-reference/
            else
                removeHelper ((k, v)::acc) tail key 
    removeHelper [] dict key

// Function: count
// Description: Counts the number of key-value pairs that satisfy a given condition.
// Parameters:
//   - dict: The dictionary implemented as a list of key-value pairs.
//   - func: A function that takes a value and returns true or false.
// Returns: The number of key-value pairs in the dictionary for which func returns true.
let count dict func =
    let rec countHelper count dict func =
        match dict with
        | [] -> count 
        | (_, v)::tail -> 
            if func v then
                countHelper (count + 1) tail func
            else
                countHelper count tail func
    countHelper 0 dict func

// Function: twoDigitCount
// Description: Counts the number of key-value pairs with a two-digit positive integer value.
// Parameters:
//   - dict: The dictionary implemented as a list of key-value pairs.
// Returns: The number of key-value pairs in the dictionary with a value between 10 and 99 (inclusive).
let twoDigitCount dict =
    count dict (fun v -> v >= 10 && v <= 99)