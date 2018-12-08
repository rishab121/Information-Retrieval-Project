from Helper import Helper
from query_matcher import QueryMatcher
from collections import defaultdict
import math
import operator


class BM25WithFeedback:
    def __init__(self, k1=1.2, k2=100, b=0.75):
        self.helper = Helper()
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.calcAVDL()
        self.queryMatcher = QueryMatcher()
        self.queryFrequencyDict = defaultdict(int)
        self.docScoreDict = defaultdict(int)

    def initializeDocScoreDict(self):
        for key in self.helper.number_of_terms_doc.keys():
            self.docScoreDict[key] = 0

    def calculateK(self, doc_id):
        retVal = self.k1*((1-self.b) + self.b *
                          (self.helper.number_of_terms_doc[doc_id]/self.avdl))
        return retVal

    def calcAVDL(self):
        sum = 0
        for key in self.helper.number_of_terms_doc.keys():
            sum += self.helper.number_of_terms_doc[key]
            self.avdl = sum/len(self.helper.number_of_terms_doc.keys())

    def calculateDocumentScore(self, term, doc_id, qId):
        r = 0
        R = 0
        n = len(self.helper.unigram_inverted_index[term].keys())
        # N total number of docs
        N = len(self.helper.number_of_terms_doc.keys())
        K = self.calculateK(doc_id)
        if doc_id not in self.helper.unigram_inverted_index[term]:
            f = 0
            docScore = 0
        else:
            f = self.helper.unigram_inverted_index[term][doc_id]
            qf = self.queryFrequencyDict[term]
            docScore = \
                math.log(((r + 0.5)/(R - r + 0.5))/((n-r+0.5)/(N - n - R + r + 0.5))
                         * (((self.k1+1)*f)/(K + f))
                         * (((self.k2 + 1)*qf)/(self.k2 + qf)))

        self.docScoreDict[doc_id] += docScore

    def createQueryFrequencyDict(self, queryAr):
        for term in queryAr:
            if term in self.queryFrequencyDict.keys():
                self.queryFrequencyDict[term] += 1
            else:
                self.queryFrequencyDict[term] = 1

    def calculateTermScore(self, term, qId, find_type, k):
        # get doc from query matcher
        # 1 exact match
        # 2 best match
        # 3 best match with proximity
        if find_type == 1:
            for doc_id in self.queryMatcher.get_exact_match_docs(self.query):
                self.calculateDocumentScore(term, doc_id, qId)
        elif find_type == 2:
            for doc_id in self.queryMatcher.get_best_match_docs(self.query):
                self.calculateDocumentScore(term, doc_id, qId)
        else:
            for doc_id in self.queryMatcher.get_ordered_best_match_docs(self.query, k):
                self.calculateDocumentScore(term, doc_id, qId)

    def score(self, qId, queryAr, find_type, k):
        for term in queryAr:
            self.calculateTermScore(term, qId, find_type, k)

    def printScores(self, qId):
        sortedDict = sorted(self.docScoreDict.items(),
                            key=operator.itemgetter(1), reverse=True)

        # file = open("Extra_Output/"+str(qId) +
        #             ".txt", "w")
        rank = 0
        for tup in sortedDict:
            rank += 1
            print(str(
                qId) + " Q0 " + str(tup[0]) + " " + str(rank) + " " + str(tup[1]) + " BM25NoStem\n")
            if rank == 100:
                break

    def main(self, q, find_type, k=0):
        self.query = q
        self.query = self.helper.parse_query(self.query)
        queryAr = self.query.split()
        self.queryFrequencyDict = defaultdict(int)
        self.docScoreDict = defaultdict(int)
        self.createQueryFrequencyDict(queryAr)
        self.score(q, queryAr, find_type, k)
        self.printScores(q)

b = 'k'
while b != 'N' and b != 'n':
    print "Enter Query:"
    query = raw_input()
    print 'Enter 1 for exact match 2 for best match 3 for best match ordered'
    find_type = int(raw_input())
    if find_type == 3:
        print "Enter proximity value"
        k = int(raw_input())
    if find_type not in [1, 2, 3]:
        print "invalid input"
    else:
        print "Fetching results......"
        bm = BM25WithFeedback()
        if find_type != 3:
            bm.main(query, find_type)
        else:
            bm.main(query, find_type, k)
    print "Press N to break or any char to continue making queries"
    b = raw_input()
