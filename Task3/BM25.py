from Helper import Helper
from collections import defaultdict
import math
import operator


class BM25:
    def __init__(self, k1,k2, b):
        self.helper = Helper()
        self.k1 = k1
        self.k2 = k2
        self.b = b
        self.stopwords_file = "../test-collection/common_words"
        self.prepare_stoplist()
        self.calcAVDL()
        self.queryFrequencyDict = defaultdict(int)
        self.docScoreDict = defaultdict(int)
        self.main()


    def initializeDocScoreDict(self):
        for key in self.helper.number_of_terms_doc.keys():
            self.docScoreDict[key] = 0

    def calculateK(self, doc_id):
        retVal = self.k1*((1-self.b) + self.b*(self.helper.number_of_terms_doc[doc_id]/self.avdl))
        return retVal

    def calcAVDL(self):
        sum = 0
        for key in self.helper.number_of_terms_doc.keys():
            sum += self.helper.number_of_terms_doc[key]
            self.avdl = sum/len(self.helper.number_of_terms_doc.keys())



    def calculateDocumentScore(self,term, doc_id):
        r = 0
        R = 0
        n = 0
        K = self.calculateK(doc_id)
        docScore = \
            math.log(((r + 0.5)/(R - r + 0.5))/((n-r+0.5)/(len(self.helper.number_of_terms_doc.keys()) - n - R + r +0.5))
                     *(((self.k1+1)*self.helper.unigram_inverted_index[term][doc_id])/(K + self.helper.unigram_inverted_index[term][doc_id]))
                     *(((self.k2 + 1)*self.queryFrequencyDict[term])/(self.k2 + self.queryFrequencyDict[term])))

        self.docScoreDict[doc_id] += docScore


    def createQueryFrequencyDict(self):
        for term in self.query.split():
            if term in self.queryFrequencyDict.keys():
                self.queryFrequencyDict[term] += 1
            else:
                self.queryFrequencyDict[term] = 1


    def calculateTermScore(self, term):
        for key1 in self.helper.unigram_inverted_index.keys():
            if key1 == term:
                for doc_id in self.helper.unigram_inverted_index[key1].keys():
                    self.calculateDocumentScore(term, doc_id)


    def score(self):
        for term in self.query.split():
            self.calculateTermScore(term)

    def printScores(self, qId):
        sortedDict = sorted(self.docScoreDict.items(), key=operator.itemgetter(1), reverse=True)
        file = open("BM_Output/"+str(qId)+"-score.txt", "w")
        rank = 0
        for tup in sortedDict:
            rank += 1
            file.write(str(tup[0]) + " " + str(tup[1]) + " \n")
            if rank == 100:
                break

    def prepare_stoplist(self):
        with open(self.stopwords_file, 'r') as f:
            text_data = f.read().split()
            self.stop_words = text_data

    def main(self):
        queries = self.helper.get_queries()
        for q in queries.keys():
            self.query = queries[q]
            self.query = self.helper.parse_query(self.query)
            self.query = self.query.split()
            self.query = [x for x in self.query if x not in self.stop_words]
            self.query = ' '.join(self.query)
            print "query is", self.query
            self.queryFrequencyDict = defaultdict(int)
            self.docScoreDict = defaultdict(int)
            self.createQueryFrequencyDict()
            self.score()
            self.printScores(q)

b = BM25(1.2,100,0.75)