#!/usr/bin/python3
from importlib.resources import contents
import re
import nltk
import sys
import getopt
import os
import math
import string
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
    lst_of_files = []
    for filename in os.listdir('disk/dictionaries/')[:]:
        f = open('disk/dictionaries/' + filename, 'r')
        data = f.read()
        dictionary = ast.literal_eval(data)
        lst_of_dictionaries.append(dictionary)
        lst_of_files.append(f)
    for filename in os.listdir('disk/postingslists/')[:]:
        lst_of_files.append(open('disk/postingslists/' + filename, 'r'))

    # Merge disk/ directory files 
    # for term in termID_dict.keys():
    #     for dictionary in lst_of_dictionaries:
    #         if term is in dictionary.keys():

    for filename in lst_of_files:
        filename.close()

    # Add in the skip pointers after the postings lists have been finalized (see temp.py for code)

    # with open(out_dict, "w+") as f1:
    #     with open(out_postings, "w+") as f2:
    #         for termID, postings in sorted_dict.items():
    #             postings.sort()

    #             f1.write(str(termID) + "\n")
    #             postings_list = ""
                
    #             for posting in postings:
    #                 postings_list += str(posting) + " "
    #                 f2.write(postings_list.strip())
                
    #             f2.write("\n")

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
