This is the README file for A0267818M-A0267993E's submission
Email(s): e1100338@u.nus.edu, e1100705@u.nus.edu

== Python Version ==

We're using Python Version 3.8.10 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

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

THINGS TO DO:
1. Decide whether we want to use BSBI or SPIMI to implement a scalable index construction
2. Figure out how to implement whichever technique we choose above lol
3. Steps for constructing an index 
    1. Generate the sequence of term, docID pairs (make sure to apply case-folding, tokenizing, and stemming on the document text)
    2. Sort this list by term (alphabetically) and then docID (under the same term) 
    3. Merge repeated term entries by splitting into dictionary and posting list
        a. Write terms and pointer to posting list into dictionary.txt and the posting list itself into postings.txt
4. Add skip pointers to posting list (using math.sqrt(len(posting)))
5. Implement searching method
    1. Figure out how to parse Boolean expressions (take a look at Dijkstra's Shunting yard algo)
    2. Parse each query and use our constructed index to obtain the results (docIDs)
    3. Write the results into the output file, one line per query, each docID separated by a single space

We are using size 2 MB blocks. There is a total of 7769 documents, which has a total size of 6.311 MB.
The block sizes are 2.003 MB, 2.000 MB, 2.000 MB, and 0.308 MB for a total of 4 blocks.