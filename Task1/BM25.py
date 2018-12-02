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
        self.calcAVDL()
        self.queryFrequencyDict = defaultdict(int)
        self.docScoreDict = defaultdict(int)
        self.relevanceDict = defaultdict()
        self.fetchRelevanceInfo()
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


    def fetchRelevanceInfo(self):
        with open('../test-collection/cacm.rel.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                ar = line.split()
                if int(ar[0]) in self.relevanceDict.keys():
                    self.relevanceDict[int(ar[0])].append(ar[2])
                else:
                    self.relevanceDict[int(ar[0])] = [ar[2]]

    def calculateR(self, term, qId):
        r = 0
        if qId not in self.relevanceDict.keys():
            return 0
        for doc_id in self.relevanceDict[qId]:
            if doc_id in self.helper.unigram_inverted_index[term].keys():
                r += 1
        return r

    def calculateDocumentScore(self,term, doc_id, qId):
        r = self.calculateR(term, qId)
        if qId in self.relevanceDict.keys():
            R = len(self.relevanceDict[qId])
        else:
            R = 0
        n = len(self.helper.unigram_inverted_index[term].keys())
        N = len(self.helper.number_of_terms_doc.keys())
        K = self.calculateK(doc_id)
        f = self.helper.unigram_inverted_index[term][doc_id]
        qf = self.queryFrequencyDict[term]
        docScore = \
            math.log(((r + 0.5)/(R - r + 0.5))/((n-r+0.5)/(N - n - R + r +0.5))
                     *(((self.k1+1)*f)/(K + f))
                     *(((self.k2 + 1)*qf)/(self.k2 + qf)))

        self.docScoreDict[doc_id] += docScore


    def createQueryFrequencyDict(self):
        for term in self.query.split():
            if term in self.queryFrequencyDict.keys():
                self.queryFrequencyDict[term] += 1
            else:
                self.queryFrequencyDict[term] = 1


    def calculateTermScore(self, term, qId):
        for doc_id in self.helper.unigram_inverted_index[term]:
            self.calculateDocumentScore(term, doc_id, qId)


    def score(self, qId):
        for term in self.query.split():
            self.calculateTermScore(term, qId)

    def printScores(self, qId):
        sortedDict = sorted(self.docScoreDict.items(), key=operator.itemgetter(1), reverse=True)
        file = open("BM_Output/"+str(qId)+"-score.txt", "w")
        rank = 0
        for tup in sortedDict:
            rank += 1
            file.write(str(tup[0]) + " " + str(tup[1]) + " \n")
            if rank == 100:
                break

    def main(self):
        queries = self.helper.get_queries()
        for q in queries.keys():
            self.query = queries[q]
            self.query = self.helper.parse_query(self.query)
            self.queryFrequencyDict = defaultdict(int)
            self.docScoreDict = defaultdict(int)
            self.createQueryFrequencyDict()
            self.score(q)
            self.printScores(q)
