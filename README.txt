This is the README file for A0267818M-A0267993E's submission
Email(s): e1100338@u.nus.edu, e1100705@u.nus.edu

== Python Version ==

We're using Python Version 3.9.13 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

** index.py summary **

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

<Please list any websites and/or people you consulted with for this
assignment and state their role>