import math
from collections import defaultdict
import re
import operator
from bs4 import BeautifulSoup


class Helper:
    def __init__(self):
        self.unigram_inverted_index = defaultdict(dict)
        self.number_of_terms_doc = defaultdict(int)
        self.total_number_of_terms_corpus = 0
        self.create_inverted_index()
        self.create_number_of_terms_doc_dict()
        self.postion_file = "unigram_with_position.txt"
        self.unigram_inverted_index_with_positions = defaultdict(dict)
        self.create_position_dict_from_file()

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
        #print self.number_of_terms_doc

    def corpus_frequency(self, unigram_inverted_index):
        corpus_term_count_dictionary = {}
        for key1 in unigram_inverted_index.keys():
            corpus_term_count_dictionary[key1] = 0
            for key2 in unigram_inverted_index[key1].keys():
                corpus_term_count_dictionary[key1] += unigram_inverted_index[key1][key2]

        return corpus_term_count_dictionary

    def parse_query(self, query):
        query = query.lower()
        regex = r"(?!\d)[.,;](?!\d)"
        regex2 = r"[(){}\"#~\[\]<>=:?!@&'|*]"
        regex3 = r"(?!\d|\w)[-/$](?!\d|\w)"
        query = re.sub(regex, "", query, 0)
        query = re.sub(regex2, "", query, 0)
        query = re.sub(regex3, "", query, 0)
        return query

    def get_queries(self):
        queries = {}
        with open('../test-collection/cacm.query.txt', 'r') as f:
            raw_data = f.read()
            bs = BeautifulSoup(raw_data, 'html.parser')
            docs = bs.find_all('doc')
            for doc in docs:
                doc_text = doc.get_text()
                lines = doc_text.replace("\n", ' ')
                lines = lines.split("\n")
                for line in lines:
                    line_list = line.split()
                    query_id = int(line_list.pop(0))
                    query = ' '.join(line_list)
                    queries[query_id] = query
        return queries

    def create_position_dict_from_file(self):
        with open(self.postion_file, 'r') as f:
            for line in f.read().splitlines():
                index = line.split('=')
                term = index.pop(0)
                inverted_list_term = ''.join(index).split()
                df = inverted_list_term.pop(0)
                df = int(df.replace(',', ''))
                try:
                    for entry in inverted_list_term:
                        doc_id = ''
                        for i in range(len(entry)):
                            ch = entry[i]
                            if ch == ',' and unicode(entry[i+1], 'utf-8').isnumeric():
                                break
                            else:
                                doc_id += ch
                        entry = entry.replace(doc_id, '')

                        doc_id = doc_id[1:]
                        tf = ''
                        for x in entry:
                            if x != '[':
                                tf += x
                            else:
                                break

                        length_tf = len(tf)
                        tf = tf.replace(',', '')
                        tf = int(tf)
                        entry = entry[(1+length_tf):]
                        entry = entry.replace(']),', '')
                        postion_list = entry.split(',')
                        postion_list.pop(len(postion_list)-1)
                        position_list = map(int, postion_list)
                        self.add_entry_to_dict(term, doc_id, tf, position_list)
                except Exception as e:
                    print "line is", line
                    print "entry is",entry
                    print "term is", term
                    print "inverted list ", inverted_list_term
                    exit()

    def add_entry_to_dict(self, term, doc_id, tf, position_list):
        self.unigram_inverted_index_with_positions[term][doc_id] = [
            tf, position_list]
