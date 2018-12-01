
from Helper import Helper
import math
from collections import defaultdict
import operator

class JM_Retreiver:
    def __init__(self):
        self.helper = Helper()
        self.unigram_inverted_index = self.helper.unigram_inverted_index
        self.corpus_term_count = self.helper.corpus_frequency(
            self.unigram_inverted_index)
        self.CONSTANT = 0.35
        self.number_of_ranked_docs = 100

    def run(self, query, query_id):
        query = self.helper.parse_query(query)
        terms = query.split()
        print "query is", query
        print "terms are", terms
        doc_scores = defaultdict(float)
        doc_list = []
        for term in terms:
            if term in self.unigram_inverted_index.keys():
                inverted_list = self.unigram_inverted_index[term]
                for doc_id in inverted_list.keys():
                    if doc_id not in doc_list:
                        doc_list.append(doc_id)
            else:
                print term
                print "term ignored not in corpus"

        for term in terms:
            if term in self.unigram_inverted_index.keys():
                for doc_id in doc_list:
                    score = self.calculate_document_score(doc_id, term)
                    doc_scores[doc_id] += score

            self.sort_scores(query, query_id, doc_scores)

    def sort_scores(self, query, query_id, doc_scores):
        sorted_scores = sorted(
            doc_scores.items(), key=operator.itemgetter(1), reverse=True)
        self.save_to_file(query, query_id, sorted_scores)

    

    def save_to_file(self, query, query_id, tf_dict):
        count = 1
        file_name = 'JM_output/' + str(query_id) + '.txt'
        
        with open(file_name, 'w') as f:
            for word in tf_dict:
                if count <= self.number_of_ranked_docs:
                    f.write(str(query_id))
                    f.write(" ")
                    f.write("Q0")
                    f.write(" ")
                    f.write(word[0])
                    f.write(" ")
                    f.write(str(count))
                    f.write(" ")
                    f.write(str(word[1]))
                    f.write(" ")
                    f.write("LM_JM_Unigram_Casefolding_PunctuationHandling")
                    f.write("\n")
                    count += 1
                else:
                    break

    def calculate_document_score(self, doc_id, term):
        first_term = (1 - self.CONSTANT) * (self.get_number_of_occurence_in_document(term,doc_id) / self.get_total_number_of_terms_in_document(doc_id))
        second_term = self.CONSTANT * ( self.number_of_occurence_in_corpus(term) / self.get_total_number_of_terms_in_corpus())
        score = math.log((first_term + second_term))
        return score
        
    # Cqi
    def number_of_occurence_in_corpus(self, term):
        return self.corpus_term_count[term] * 1.0

    # |C|
    def get_total_number_of_terms_in_corpus(self):
        return self.helper.total_number_of_terms_corpus * 1.0

    # |D|
    def get_total_number_of_terms_in_document(self, doc_id):
        return self.helper.number_of_terms_doc[doc_id] * 1.0

    # fqi, D
    def get_number_of_occurence_in_document(self, term, doc_id):
        documents_dict = self.unigram_inverted_index[term]
        if doc_id in documents_dict.keys():
            return documents_dict[doc_id] * 1.0
        return 0

    def JM_test(self):
        queries = self.helper.get_queries()
        for key in queries.keys():
            self.run(queries[key], key)


j = JM_Retreiver()
j.JM_test()