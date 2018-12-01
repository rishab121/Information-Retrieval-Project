from Helper import Helper
import math
from collections import defaultdict
import re
import operator


class TfIdf:
	def __init__(self):
		self.dfDict = defaultdict(int)
		self.tfIdfDict = defaultdict(dict)
		self.idfDict = defaultdict(int)
		self.number_of_documents = len(r.number_of_terms_doc)
		# self.printTF()
		self.calculateDocumentFrequency()
		self.calculateInverseDocumentFrequency()
		self.calculateTFIdfScore()
		self.writeTfIdfScoreToFile()


	def printTF(self):
		for entry in r.unigram_inverted_index:
			for en in r.unigram_inverted_index[entry]:
				print entry
				print en
				print r.unigram_inverted_index[entry][en]
		# number_terms_doc

	def calculateDocumentFrequency(self):
		for term in r.unigram_inverted_index:
			self.dfDict[term] = len(r.unigram_inverted_index[term])
			# print term
			# print self.dfDict[term]

	def calculateInverseDocumentFrequency(self):
		for term in self.dfDict:
			self.idfDict[term] = math.log(self.number_of_documents/self.dfDict[term])
			# print term
			# print self.idfDict[term]

	def calculateTFIdfScore(self):
		for term in r.unigram_inverted_index:
			for doc_id in r.unigram_inverted_index[term]:
				self.tfIdfDict[term][doc_id] = r.unigram_inverted_index[term][doc_id] * self.idfDict[term]
		# print self.tfIdfDict

		self.tfIdfDict = sorted(self.tfIdfDict.items(), key=operator.itemgetter(1))
		print self.tfIdfDict

	def writeTfIdfScoreToFile(self):
		file_name = "tfIdfScore.txt"
		f = open(file_name,'w')
		count = 1
		for key, value in self.tfIdfDict:
			if count < 101:
				f.write(str(key) +" : " + str(value) +'\n')
				count+=1
		f.close()

r = Helper()
t = TfIdf()
