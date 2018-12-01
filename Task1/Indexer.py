from collections import deque, defaultdict
import re
import time
import os
import errno
import string
import collections

# inverted_index_unigram = { term : {doc_id: tf, doc_id: tf}, term2: {} }


class SimpleIndexer:

    def __init__(self):
        self.dir = "./parsed_pages/"
        self.doc_words = defaultdict(list)
        self.inverted_index_unigram = defaultdict(dict)
        self.number_of_terms_for_unigram = defaultdict(int)
        self.get_words_for_document()

    def get_words_for_document(self):
        for file in os.listdir(self.dir):
            doc_id = file.split('.txt')[0]
            with open((self.dir + file), 'r') as f:
                for word in f.read().split():
                    self.number_of_terms_for_unigram[doc_id] += 1
                    self.doc_words[doc_id].append(word)
        self.save_number_of_words(
            'number_of_terms_unigram.txt', self.number_of_terms_for_unigram)

    def create_unigram_index(self):
        for doc_id in self.doc_words.keys():
            for word in self.doc_words[doc_id]:
                inverted_list_term = self.inverted_index_unigram[word]
                if len(inverted_list_term.keys()):
                    if doc_id in inverted_list_term.keys():
                        inverted_list_term[doc_id] += 1
                    else:
                        inverted_list_term[doc_id] = 1
                else:
                    inverted_list_term[doc_id] = 1
                    self.inverted_index_unigram[word] = inverted_list_term
        self.sort_inverted_index(
            'unigram_index.txt', self.inverted_index_unigram)

    def sort_inverted_index(self, file_name, inverted_index):
        sorted_inverted_index = collections.OrderedDict(
            sorted(inverted_index.items()))
        for word in sorted_inverted_index.keys():
            inverted_list = sorted_inverted_index[word]
            sorted_inverted_list = collections.OrderedDict(
                sorted(inverted_list.items()))
            sorted_inverted_index[word] = sorted_inverted_list

        self.save_to_file(file_name, sorted_inverted_index)

    def save_to_file(self, file_name, sorted_inverted_index):
        with open(file_name, 'w') as f:
            for word in sorted_inverted_index.keys():
                f.write(word)
                f.write(': ')
                sorted_inverted_list = sorted_inverted_index[word]
                for doc_id in sorted_inverted_list.keys():
                    f.write("(")
                    f.write(doc_id)
                    f.write(":")
                    f.write(str(sorted_inverted_list[doc_id]))
                    f.write(") ")
                f.write("\n")

    def save_number_of_words(self, file_name, number_of_terms):
        with open(file_name, 'w') as f:
            for doc_id in number_of_terms.keys():
                f.write(doc_id)
                f.write(": ")
                f.write(str(number_of_terms[doc_id]))
                f.write("\n")


u = SimpleIndexer()
u.create_unigram_index()
