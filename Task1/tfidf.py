from Helper import Helper
import math
from collections import defaultdict
import re
import operator


class TfIdf:
	def __init__(self):
		self.dfDict = defaultdict(int)
		self.tfIdfDict = defaultdict(dict)
		self.idfDict = defaultdict(float)
		self.number_of_documents = len(r.number_of_terms_doc.keys())
		# self.printTF()
		self.calculateDocumentFrequency()
		self.calculateInverseDocumentFrequency()
		# self.calculateTFIdfScore()
		# self.writeTfIdfScoreToFile()
		self.performQueryTfIdf()


	def printTF(self):
		for entry in r.unigram_inverted_index:
			for en in r.unigram_inverted_index[entry]:
				print entry
				print en
				print r.unigram_inverted_index[entry][en]
		# number_terms_doc

	def calculateDocumentFrequency(self):
		for term in r.unigram_inverted_index:
			self.dfDict[term] = len(r.unigram_inverted_index[term].keys())

			# print term
			# print self.dfDict[term]

	def calculateInverseDocumentFrequency(self):
		for term in self.dfDict:
			self.idfDict[term] = 1.0 + math.log(float(self.number_of_documents)/float(self.dfDict[term]))
			# print term
			# print self.idfDict[term]

	def calculateTFIdfScore(self,doc_id,term):
		# for term in r.unigram_inverted_index:
		# 	for doc_id in r.unigram_inverted_index[term]:
		if term in r.unigram_inverted_index.keys():
			values = defaultdict(int)
			values = r.unigram_inverted_index[term]
			if doc_id in values.keys():
				return (float(r.unigram_inverted_index[term][doc_id])/float(r.number_of_terms_doc[doc_id]))* self.idfDict[term]
			else:
				return 0
		# print self.tfIdfDict

		# self.tfIdfDict = sorted(self.tfIdfDict.items(), key=operator.itemgetter(1))
		# print self.tfIdfDict

	def writeTfIdfScoreToFile(self,query,queryId,sorted_scores):
		count = 1
		file_name = 'TF-IDF_output/' + str(queryId) + '.txt'
		print 'writing' + str(queryId)
		
		with open(file_name, 'w') as f:
			for word in sorted_scores:
				if count <= 100:
					f.write(str(queryId))
					f.write(" ")
					f.write("Q0")
					f.write(" ")
					f.write(word[0])
					f.write(" ")
					f.write(str(count))
					f.write(" ")
					f.write(str(word[1]))
					f.write(" ")
					f.write("TF-IDF_Unigram_Casefolding_PunctuationHandling")
					f.write("\n")
					count += 1
				else:
					break

	def getTfIdf(self, query, queryId):
		queryTerms = query.split(' ')
		documents_containing_term = []
		documentScores = defaultdict(float)
		for term in queryTerms:
			if term in r.unigram_inverted_index.keys():
				inverted_list = r.unigram_inverted_index[term]
				for doc_id in inverted_list.keys():
					if doc_id not in documents_containing_term:
						documents_containing_term.append(doc_id)
			else:
				print term
				print "Term is not present in corpus"

		for term in queryTerms:
			if term in r.unigram_inverted_index.keys():
				for doc_id in documents_containing_term:
					score = self.calculateTFIdfScore(doc_id, term)
					documentScores[doc_id] += score
		self.sort_scores(query, queryId,documentScores)


	def sort_scores(self, query, query_id, doc_scores):
		sorted_scores = sorted(
			doc_scores.items(), key=operator.itemgetter(1), reverse=True)
		self.writeTfIdfScoreToFile(query, query_id, sorted_scores)


	def performQueryTfIdf(self):
		self.queries = r.get_queries()
		for query in self.queries:
			self.queries[query] = r.parse_query(self.queries[query])

		for query in self.queries:
			self.getTfIdf (self.queries[query],query)

r = Helper()
t = TfIdf()
