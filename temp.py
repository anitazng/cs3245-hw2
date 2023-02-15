sorted_dict = dict(sorted(word_and_postings_dictionary.items()))
postings_file = open("disk/postingslist" + str(iterations) + ".txt", "a")
dictionary_file = open("disk/dictionary" + str(iterations) + ".txt", "a")
dictionary = {}
for word, postings in sorted_dict.items():
    postings_list = []
    postings.sort()
    skip_length = math.floor(math.sqrt(len(postings)))
    if skip_length >= 2:
        curr_skip_length = 0
        for index, posting in enumerate(postings):
            skip_pointer_index = curr_skip_length + skip_length
            if index % skip_length == 0 and skip_pointer_index < len(postings):
                postings_list.append((posting, skip_pointer_index))
                curr_skip_length += skip_length
            else:
                postings_list.append((posting, None))
    else:
        for posting in postings:
            postings_list.append((posting, None))
    postings_file.write(str(postings_list))
    dictionary.update({word: postings_file.tell()})
dictionary_file.write(str(dictionary))
postings_file.close()
dictionary_file.close()
