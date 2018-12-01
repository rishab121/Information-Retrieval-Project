import math
from collections import defaultdict
import re
import operator
class Retreiver:
    def __init__(self):
        self.unigram_inverted_index = defaultdict(dict)
        self.create_inverted_index()


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
        #print self.unigram_inverted_index

r = Retreiver()
