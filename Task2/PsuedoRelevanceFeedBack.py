from Helper import Helper
from collections import defaultdict
import math
import operator


class PsuedoRelevanceFeedBack:
    def __init__(self):
        self.helper = Helper()
        self.documnetVector = defaultdict(dict)
        self.queryVector = defaultdict(str)
        self.docScoreDict = defaultdict(int)
        self.stopwords_file = "../test-collection/common_words"
        self.output_dir = "./stopped_pages_output/"
        self.prepare_stoplist()
        self.stopwords_file = "../test-collection/common_words"
        self.prepare_stoplist()

    def prepare_stoplist(self):
        with open(self.stopwords_file, 'r') as f:
            text_data = f.read().split()
            self.stop_words = text_data

    def initRelavantDocVector(self, qId):
        with open('BM_Output/'+str(qId)+'-score.txt', 'r') as f:
            i = 1
            lines = f.readlines()
            for line in lines:
                i += 1
                ar = line.split()
                self.documnetVector[ar[0]] = {};
                if i == 12:
                    break

    def populateRelevantDocVector(self):
        for term in self.helper.unigram_inverted_index.keys():
            for docId in self.helper.unigram_inverted_index[term].keys():
                if docId in self.documnetVector.keys():
                    self.documnetVector[docId][term] = self.helper.unigram_inverted_index[term][docId]


    def getQueryVector(self):
        for term in self.query.split():
            if term in self.queryVector.keys():
                self.queryVector[term] += 1
            else:
                self.queryVector[term] = 1

        for t in self.helper.unigram_inverted_index.keys():
            if t not in self.queryVector.keys():
                self.queryVector[t] = 0

    def calculateVectorScore(self, term):
        retVal = 0;
        for docId in self.documnetVector.keys():
            if term in self.documnetVector[docId].keys():
                retVal += self.documnetVector[docId][term]
        return retVal



    def calculateRocchioScore(self, qId, queryAr):
        expansionTerms = []
        a = 0.8
        b = 1
        c = 0
        for t in self.helper.unigram_inverted_index.keys():
            self.queryVector[t] = a*self.queryVector[t] + b*self.calculateVectorScore(t)

        sortedDict = sorted(self.queryVector.items(), key=operator.itemgetter(1), reverse=True)

        i = 0
        for tup in sortedDict:
            if tup[0] not in self.stop_words:
                if tup[0] not in queryAr:
                    expansionTerms.append(tup[0])
                    i += 1
                    print(str(tup[0]))
            if i == 10:
                break

        with open('ExpansionTerms/' + str(qId) + '-ExpTerms.txt', 'w') as f:
            for term in expansionTerms:
                f.write(term+"\n")
        return expansionTerms

    def main(self, qId, queryAr):
        queries = self.helper.get_queries()
        self.query = queries[qId]
        self.documnetVector = defaultdict(dict)
        self.queryVector = defaultdict(str)
        self.getQueryVector()
        self.initRelavantDocVector(qId)
        self.populateRelevantDocVector()
        return self.calculateRocchioScore(qId, queryAr)

