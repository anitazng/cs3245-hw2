#!/usr/bin/python3
import re
from ssl import cert_time_to_seconds
import nltk
import sys
import getopt
import json
import ast

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # open queries file and process each query
    with open(queries_file) as f1:
        with open(results_file) as f2:
            lines = f1.readlines()

            for line in lines:
                postfix_exp = create_postfix_exp(line)

                # modify this so that it writes only the docIDs to the results_file and not the tuples with the docID and skip pointer
                f2.write(evaluate_exp(postfix_exp, dict_file, postings_file, "all_docIDs.txt")) # write the result of each query into the results-file
    
def get_postings_list(term, dict_file, postings_file,):
    # returns list of docIDs
    postings = ""

    with open(dict_file) as f: # load dictionary into memory
        dictionary = f.read()
        dictionary = json.loads(dictionary)

    byte_location = dictionary[term]

    with open(postings_file) as f:
        f.seek(byte_location)
        char = f.read(1) # skip the "[" character
        char = f.read(1) # read first postings list char

        while char != "]":
            postings += char
            char = f.read(1)
    
    postings_list = list(ast.literal_eval(postings))

    return postings_list

def create_postfix_exp(query):
    # use shunting-yard algorithm to turn in-fix query into a post-fix query
    operators = ["AND", "NOT", "OR"]
    op_precedence = {"OR": 0, "AND": 1, "NOT": 2} # order of precedence is NOT, then AND, then OR
    buffer = []
    op_stack = []
    tokens = re.findall("AND|OR|NOT|\(|\)|\w+", query) # tokenize the query, i.e. get all words and operators
    
    # https://aquarchitect.github.io/swift-algorithm-club/Shunting%20Yard/
    for token in tokens:
        if token == "OR" or token == "AND" or token == "NOT":
            while len(op_stack) != 0 and op_stack[-1] in operators and op_precedence[op_stack[-1]] > op_precedence[token]:  
                buffer.append(op_stack.pop())
            op_stack.append(token)
        elif token == "(":
            op_stack.append(token)
        elif token == ")":
            while op_stack[-1] != "(":
                buffer.append(op_stack.pop())
            op_stack.pop() # pop ( character
        else:
            buffer.append(token)
        
    while len(op_stack) != 0:
        buffer.append(op_stack.pop())
    
    return buffer

def evaluate_exp(query, dict_file, postings_file, full_postings_list):
    # given a post-fix query as a list, use a stack to evaluate the query
    # returns string containing the resulting docIDs
    operators = ["AND", "NOT", "OR"]
    stack = []

    for token in query:
        if token not in operators:
            stack.append(get_postings_list(token))
        elif token == "NOT":
            stack.append(logical_not(stack.pop(), full_postings_list))
        elif token == "AND":
            postings_one = stack.pop()
            postings_two = stack.pop()
            stack.append(logical_and(postings_one, postings_two))
        else:
            postings_one = stack.pop()
            postings_two = stack.pop()
            stack.append(logical_or(postings_one, postings_two))

    return stack[0]

def logical_and(postings_one, postings_two):
    # returns the merged postings lists using the and operator

    result = []
    p1 = 0
    p2 = 0

    while p1 != len(postings_one) and p2 != len(postings_two):
        if postings_one[p1][0] == postings_two[p2][0]:
            result.append(postings_one[p1])
            p1 += 1
            p2 += 1
        elif postings_one[p1][0] < postings_two[p2][0]:
            if postings_one[p1][1] != None and postings_one[p1][1] <= postings_two[p2][0]:
                while postings_one[p1][1] != None and postings_one[p1][1] <= postings_two[p2][0]:
                    p1 = postings_one[p1][1]
                else:
                    p1 += 1
            elif postings_two[p2][1] != None and postings_two[p2][1] <= postings_one[p1][0]:
                while postings_two[p2][1] != None and postings_two[p2][1] <= postings_one[p1][0]:
                    p2 = postings_two[p2][1]
                else:
                    p2 += 1
    
    return result

def logical_or(postings_one, postings_two):
    # returns the merged postings lists using the or operator

    result = []
    p1 = 0
    p2 = 0

    while p1 != len(postings_one) and p2 != len(postings_two):
        if postings_one[p1][0] < postings_two[p2][0]:
            result.append(postings_one[p1])
            p1 += 1
        elif postings_one[p1][0] == postings_two[p2][0]:
            result.append(postings_one[p1])
            p1 += 1
            p2 += 1
        else:
            result.append(postings_two[p2])
            p2 += 1

    if p1 != len(postings_one):
        for posting in postings_one[p1:]:
            result.append(posting[0])
    
    if p2 != len(postings_two):
        for posting in postings_two[p2:]:
            result.append(posting[0])

    return result

def logical_not(postings_list, full_postings_list):
    # returns the merged postings lists using the not operator

    result = []
    p1 = 0
    p2 = 0

    while p1 != len(postings_list):
        if postings_list[p1][0] != full_postings_list[p2][0]:
            result.append(full_postings_list[p2][0])
            p2 += 1
        else:
            p1 += 1
            p2 += 1

    result.append(full_postings_list[p2][0])

    return result

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
