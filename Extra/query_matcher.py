from Helper import Helper
from collections import defaultdict


class QueryMatcher:
    def __init__(self):
        self.helper = Helper()
        self.temp_dict = {}
        self.unigram_inverted_index = self.helper.unigram_inverted_index
        # print self.helper.unigram_inverted_index_with_positions

    def get_docs_with_exact_query(self, query):
        terms = query.split()
        all_terms_docs = []
        for term in terms:
            term_docs = self.helper.unigram_inverted_index_with_positions[term].keys(
            )
            all_terms_docs.append(term_docs)
            self.temp_dict[term] = self.helper.unigram_inverted_index_with_positions[term]
        common_docs = set(all_terms_docs[0]).intersection(*all_terms_docs)
        return common_docs

    def get_exact_match_docs(self, query):
        common_docs = self.get_docs_with_exact_query(query)
        #print "comman docs are", common_docs
        doc_term_position = defaultdict(dict)
        exact_match_docs = set()
        terms = query.split()
        for doc in common_docs:
            for term in query.split():
                doc_term_position[doc][term] = self.temp_dict[term][doc][1]
        for doc in common_docs:
            term_positions = []
            for i in range(len(terms)-1):
                flag = False
                first_term = terms[i]
                second_term = terms[i+1]
                if not len(term_positions):
                    first_term_positions = doc_term_position[doc][first_term]
                else:
                    first_term_positions = [
                        term_positions[-1]]
                second_term_positions = doc_term_position[doc][second_term]
                for fpos in first_term_positions:
                    for spos in second_term_positions:
                        if spos - fpos == 1:
                            flag = True
                            term_positions.append(fpos)
                            term_positions.append(spos)
                if not flag:
                    #print "breaking"
                    break
                elif i == len(terms)-2:
                    exact_match_docs.add(doc)
        return list(exact_match_docs)

    def get_best_match_docs(self, query):
        doc_list = []
        terms = query.split()
        for term in terms:
            if term in self.unigram_inverted_index.keys():
                inverted_list = self.unigram_inverted_index[term]
                for doc_id in inverted_list.keys():
                    if doc_id not in doc_list:
                        doc_list.append(doc_id)
            else:
                print term
                print "term ignored not in corpus"
        return doc_list

    # not sure whether to inculde single term docs
    # or not, remove exactly one term docs to
    # get proper result
    def get_ordered_best_match_docs(self, query, k):
        atleast_one_term_docs = self.get_best_match_docs(query)
        terms = query.split()
        good_docs = []
        for doc in atleast_one_term_docs:
            term_positions = []
            for i in range(len(terms)-1):
                flag = False
                first_term = terms[i]
                second_term = terms[i+1]
                if doc not in self.unigram_inverted_index[first_term].keys() or doc not in self.unigram_inverted_index[second_term].keys():
                    break
                if not len(term_positions):
                    first_term_positions = self.helper.unigram_inverted_index_with_positions[
                        first_term][doc][1]
                else:
                    first_term_positions = [
                        term_positions[-1]]
                second_term_positions = self.helper.unigram_inverted_index_with_positions[
                    second_term][doc][1]

                for fpos in first_term_positions:
                    #print "fpos is", fpos
                    for spos in second_term_positions:
                        #print "spos is", spos
                        if spos - fpos > 0 and spos - fpos <= k:
                            flag = True
                            #print "-----------------------match-----------------------------"
                            term_positions.append(fpos)
                            term_positions.append(spos)
                            if doc not in good_docs:
                                good_docs.append(doc)
                            break
                if flag:
                    #print "breaking"
                    break
        exactly_one_term_docs = self.get_exactly_one_term_documents(terms)
        #print "exactly one term docs are", exactly_one_term_docs
        return good_docs + exactly_one_term_docs

    def get_exactly_one_term_documents(self, terms):
        exactly_one_term_docs = defaultdict(int)
        for term in terms:
            term_docs = self.unigram_inverted_index[term].keys()
            for doc in term_docs:
                exactly_one_term_docs[doc] += 1
        return [x for x in exactly_one_term_docs.keys() if exactly_one_term_docs[x] == 1]

# Test
# e = QueryMatcher()
# query = "operating systems"
# print "Exact match documents"
# print e.get_exact_match_docs(query)
# print "--------------------------------------------------------------"
# print "Best match documents"
# print e.get_best_match_docs(query)
# print "--------------------------------------------------------------"
# print "Ordered best match documents"
# print e.get_ordered_best_match_docs(query,3)

#print [x for x in e.get_ordered_best_match_docs(query,3) if x not in  e.get_exact_match_docs(query)]
