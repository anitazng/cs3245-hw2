#!/usr/bin/python3
from importlib.resources import contents
import re
import nltk
import sys
import getopt
import os
import math
import string
import json
import ast 
from nltk.stem.porter import *

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    starting_file_index = 0
    iterations = 0
    os.mkdir("disk/")
    os.mkdir("disk/dictionaries/")
    os.mkdir("disk/postingslists/")
    files = sorted(os.listdir(in_dir), key=int) # grab all filenames in in_directory in sorted order

    while starting_file_index < 7769:
        term_and_postings_dictionary = {}
        term_docID_pairs_lst = []
        iterations += 1
        total_size = 0

        for filename in files[starting_file_index:]: # grab all filenames in in_directory
            if total_size <= 2:
                file_stats = os.stat('training/' + filename)
                total_size += file_stats.st_size / (1024 * 1024)
                starting_file_index += 1
                with open(os.path.join(in_dir, filename), 'r') as f: # open each file
                    content = (f.read()).lower() # apply case-folding
                    content = content.translate(str.maketrans('', '', string.punctuation)) # remove punctuation
                    words = nltk.tokenize.word_tokenize(content) # tokenize into words

                    stemmer = PorterStemmer()
                    words = [stemmer.stem(word) for word in words] # apply stemming

                    for word in words:
                        term_docID_pairs_lst.append((word, int(filename)))
            else:
                break

        term_docID_pairs_lst = list(dict.fromkeys(term_docID_pairs_lst)) # remove duplicates from list of term-docID pairs
        sorted_lst = sorted(term_docID_pairs_lst)

        for (term, docID) in sorted_lst:
            if term not in term_and_postings_dictionary:
                term_and_postings_dictionary[term] = [docID]
            else:
                term_and_postings_dictionary[term].append(docID)

        sorted_dict = dict(sorted(term_and_postings_dictionary.items()))
        postings_file = open("disk/postingslists/postingslist" + str(iterations) + ".txt", "a")
        dictionary_file = open("disk/dictionaries/dictionary" + str(iterations) + ".txt", "a")
        dictionary = {}
        for term, postings in sorted_dict.items():
            dictionary.update({term: postings_file.tell()})
            postings_file.write(str(postings))
        dictionary_file.write(str(dictionary))
        postings_file.close()
        dictionary_file.close()

    lst_of_dictionaries = []
    lst_of_postings_lists_files = []
    lst_of_all_files = []
    for filename in os.listdir('disk/dictionaries/')[:]:
        f = open('disk/dictionaries/' + filename, 'r')
        data = f.read()
        dictionary = ast.literal_eval(data)
        lst_of_dictionaries.append(dictionary)
        lst_of_all_files.append(f)
    for filename in os.listdir('disk/postingslists/')[:]:
        lst_of_all_files.append(open('disk/postingslists/' + filename, 'r'))
        lst_of_postings_lists_files.append(open('disk/postingslists/' + filename, 'r'))

    def get_postings_list(term, dictionary, postings_file):
        # returns list of docIDs
        postings = ""
        char = ""
        byte_location = dictionary[term]
        postings_file.seek(byte_location)
        while char != "]":
            char = postings_file.read(1)
            postings += char
        postings_list = list(ast.literal_eval(postings))
        return postings_list

    # Merge disk/ directory files 
    num_dictionaries = len(lst_of_dictionaries)
    for x in range(int(num_dictionaries / 2)):
        y = (x * 2) + 1
        f_d12 = open('disk/dictionaries/dictionary' + str(x * 2 + 1) + str(y + 1) + '.txt', 'a')
        f_p12 = open('disk/postingslists/postingslist' + str(x * 2 + 1) + str(y + 1) + '.txt', 'a')
        d1 = lst_of_dictionaries[x * 2]
        d2 = lst_of_dictionaries[y]
        p1 = lst_of_postings_lists_files[x * 2]
        p2 = lst_of_postings_lists_files[y]
        d3 = {}
        d3.update(d1)
        d3.update(d2)
        d3 = dict(sorted(d3.items()))
        for (k, v) in d3.items():
            if k in d1.keys() and k not in d2.keys():
                postings_list = get_postings_list(k, d1, p1)
                d3[k] = f_p12.tell()
                f_p12.write(str(postings_list))
            elif k in d2.keys() and k not in d1.keys():
                postings_list = get_postings_list(k, d2, p2)
                d3[k] = f_p12.tell()
                f_p12.write(str(postings_list))
            else:
                postings_list_1 = get_postings_list(k, d1, p1)
                postings_list_2 = get_postings_list(k, d2, p2)
                postings_list_1 += postings_list_2
                postings_list = sorted(postings_list_1)
                d3[k] = f_p12.tell()
                f_p12.write(str(postings_list))
        f_d12.write(str(d3))

    for filename in lst_of_all_files:
        filename.close()

    # Add in the skip pointers after the postings lists have been finalized (see temp.py for code)
    # Add document frequency to dictionary at the end of merging

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
