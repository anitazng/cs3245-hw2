#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    nltk.download('punkt')
    dictionary = {}

    for filename in os.listdir(in_dir): # grab all filenames in in_directory
        with open(os.path.join(in_dir, filename), 'r') as f: # open each file
            content = f.read()
            sentences = nltk.tokenize.sent_tokenize(content)
            words = []
            
            for sentence in sentences:
                for word in nltk.tokenize.word_tokenize(sentence):
                    words.append(word)
            
            for word in words:
                if word not in dictionary:
                    dictionary[word] = [filename]
                else:
                    dictionary[word] = dictionary[word].append(filename)
    
    print(dictionary)

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
