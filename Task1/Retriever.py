import math
from collections import defaultdict
import re
import operator


class Retreiver:
    def __init__(self):
        self.unigram_inverted_index = defaultdict(dict)
        self.number_of_terms_doc = defaultdict(int)
        self.total_number_of_terms_corpus = 0
        self.create_inverted_index()
        self.create_number_of_terms_doc_dict()

    def create_inverted_index(self):
        with open('unigram_index.txt', 'r') as f:
            for line in f.read().splitlines():
                line_list = line.split()
                term = line_list.pop(0)
                term = term.replace(':', '')
                for element in line_list:
                    try:
                        element = element.replace('(', '')
                        element = element.replace(')', '')
                        doc_id = element.split(':')[0]
                        tf_doc = int(element.split(':')[1].strip())
                        self.unigram_inverted_index[term][doc_id] = tf_doc
                    except IndexError as e:
                        print line_list
                        print element

    def create_number_of_terms_doc_dict(self):
        with open('number_of_terms_unigram.txt', 'r') as f:
            for line in f.read().splitlines():
                doc_id = line.split(':')[0]
                number_of_terms = int(line.split(':')[1].strip())
                self.number_of_terms_doc[doc_id] = number_of_terms
                self.total_number_of_terms_corpus += number_of_terms
        print self.number_of_terms_doc

r = Retreiver()
