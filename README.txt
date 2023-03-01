This is the README file for A0267818M-A0267993E's submission
Email(s): e1100338@u.nus.edu, e1100705@u.nus.edu

== Python Version ==

We're using Python Version 3.9.13 for this assignment.

== General Notes about this assignment ==

The index.py file uses the SPIMI model to build the index with an assumed memory limit of 2 MB. 
The file contains the build_index function, which firsts begins with organizing all the files 
from the training/ directory into new dictionary and postings files of size <= 2 MB. Then, once 
these files with the appropriate block sizes are created, it is time to merge them in steps into 
one final dictionary file and one final postings file given by the parameters of the build_index 
function. The way the function merges the files is through two-way merging. If the 
dictionary/postings were organized into a binary tree, we loop the number of times that is the 
height of the binary tree, continually creating merged intermediate files and deleting 
previous files in the loop. Once all the files have been merged into the dictionary file and 
postings file, the function implements skip pointers and adds the document frequency for each
item in the dictionary file. 

The search.py file contains firstly the run_search function. This function processes each 
query in the query file one by one and writes the resulting merged postings list to the 
output file. The file also has a get_postings_list function that retrieves the postings list
for a specific term. The next two functions are the create_postfix_exp and evaluate_exp
functions. The create_postfix_exp function uses the Dijkstra's shunting yard algorithm to
process the query into a postfix expression, meaning the operators are present after the
operands, rather than in between, making the expression easier to evaluate. This postfix 
query is then fed into the evaluate_exp function, which merges the postings lists together
and returns the final result. The final three functions in this file are logical_and, 
logical_or, and logical_not, which follow the algorithms seen in class to merge two postings
lists together based on the operator.

== Files included with this submission ==

README.txt - contains information about the submission
index.py - contains the logic for indexing
search.py - contains the logic for searching the index
dictionary.txt - contains the dictionary that includes each term, pointer to postings list (byte location), and doc frequency
postings.txt - contains the postings lists, one after the others
alldocIDs.txt - contains a full listing of all document IDs

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] We, A0267818M-A0267993E, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

Stack Overflow - Looking up syntax for working with disk/files in Python
Piazza - Posted questions online and used answers from prof, tutors, and peers 