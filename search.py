#!/usr/bin/python3
import re
from ssl import cert_time_to_seconds
import nltk
import sys
import getopt
import json

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

                f2.write(evaluate_exp(postfix_exp, dict_file, postings_file)) # write the result of each query into the results-file
    
def get_postings_list(term, term_to_termID_dict, dict_file, postings_file,):
    # returns list of docIDs

    with open(term_to_termID_dict) as f:
        mapping = f.read()
        mapping = json.loads(mapping)

    with open(dict_file) as f:
        dictionary = f.read()
        dictionary = json.loads(mapping)

    termID = mapping[term]
    byte_location = dictionary[termID]

    
    pass

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
    pass

def logical_or(postings_one, postings_two):
    # returns the merged postings lists using the or operator
    pass

def logical_not(postings_list, full_postings_list):
    # returns the merged postings lists using the not operator
    pass

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
