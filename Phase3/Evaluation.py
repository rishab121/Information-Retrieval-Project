from __future__ import division
import os
from os.path import exists
from collections import defaultdict
import collections


relevant_documents = defaultdict()
output_relevant_documents = defaultdict()
totalQueries = 0
precisionDict=defaultdict()
recallDict=defaultdict()
mean_average_precision=0
mean_reciprocal_rank = 0
documents_with_no_relevance_judgements=0

def populateRelevantDictionary():
	relDocsFile = open('cacm.rel.txt','r')
	for entry in relDocsFile.readlines():
		queryId = entry.split(' ')[0]
		queryId = int(queryId)
		if queryId in relevant_documents.keys():
			values = relevant_documents[queryId]
			values.append(entry.split(' ')[2].lower())
		else:
			relevant_documents[queryId] = [entry.split(' ')[2].lower()]

	relDocsFile.close()
	# print relevant_documents.keys()

def populateOutputRelevantDictionary(path):
	count = 1
	for filename in os.listdir(path):
		# print filename
	# while count<=64:
		# print str(count)
		file = open(str(path) + '/'+ filename,'r')
		# print file
		for entry in file.readlines():
			# print entry
			queryId = entry.split(' ')[0]
			queryId = int(queryId)
			if queryId in output_relevant_documents.keys():
				values = output_relevant_documents[queryId]
				values.append(entry.split(' ')[2])
				# print str(entry.split(' ')[2])
			else:
				output_relevant_documents[queryId] = [entry.split(' ')[2]]
				# print str(entry.split(' ')[2])
			count+=1

	totalQueries = len(output_relevant_documents.keys())
	# print totalQueries

	# print output_relevant_documents.keys()

	# for query in output_relevant_documents:
	# 	print "\n"
	# 	print query
	# 	print output_relevant_documents[query]

	file.close()


def populateResponseList(path):
	global relevant_documents
	responseDict = defaultdict()
	# print relevant_documents
	for queryId in range(1,65):
		docsConsidered=[]
		# print queryId
		if queryId in relevant_documents.keys():
			relDocs = relevant_documents[queryId]
		else:
			relDocs=[]
		outDocs = output_relevant_documents[queryId]
		responseList=[]
		for doc in outDocs:
			if doc in relDocs:
				responseList.append('R')
			else:
				responseList.append('N')
		responseDict[queryId] = responseList

	calculatePrecisionAndRecall(responseDict,docsConsidered,path)

def calculatePrecisionAndRecall(responseDict,docsConsidered,path):
	for query in responseDict:
		responseList = responseDict[query]
		# print responseList
		reciprocal_rank_of_first_relevant_document=0
		recallList=[]
		precisionList=[]
		average_precision = 0
		no_of_relevant_docs_retrieved = 0
		no_of_docs_retrieved = 0
		no_of_relevant_docs = 0
		if 'R' in responseList:
			rank = responseList.index('R') + 1
		else:
			global documents_with_no_relevance_judgements
			documents_with_no_relevance_judgements+=1
			continue
		# print rank
		reciprocal_rank_of_first_relevant_document = float(1/rank)
		# print reciprocal_rank_of_first_relevant_document
		global mean_reciprocal_rank
		mean_reciprocal_rank+=reciprocal_rank_of_first_relevant_document
		for item in responseList:
			if item == 'R':
				no_of_relevant_docs+=1
		for item in responseList:
			if item == 'R':
				no_of_relevant_docs_retrieved+=1
			no_of_docs_retrieved+=1
			if no_of_relevant_docs == 0:
				recallList.append(0.0)
			else:
				recallList.append(float(no_of_relevant_docs_retrieved)/float(no_of_relevant_docs))
				# recallList.append(float(no_of_relevant_docs_retrieved)/float(no_of_relevant_docs))
			# precisionList.append(float(no_of_relevant_docs_retrieved)/float(no_of_docs_retrieved))
			if item == 'R':
				average_precision+=float(no_of_relevant_docs_retrieved)/float(no_of_docs_retrieved)
			precisionList.append(float(no_of_relevant_docs_retrieved)/float(no_of_docs_retrieved))
		precisionDict[query] = precisionList
		recallDict[query] = recallList
		if no_of_relevant_docs==0:
			average_precision = 0.0
		else:
			average_precision = average_precision/no_of_relevant_docs
		global mean_average_precision
		mean_average_precision+= average_precision
		writeOutputToFile(responseList,precisionList,recallList,query,docsConsidered,average_precision,reciprocal_rank_of_first_relevant_document,path)

def writeOutputToFile(responseList,precisionList,recallList,queryId,docsConsidered,average_precision,reciprocal_rank,path):
		count = 1
		file_name = str(path) + str(queryId) + '.txt'
		docs = output_relevant_documents[queryId]
		# print "writing " + str(file_name)
		with open(file_name, 'w') as f:
			f.write("QueryId")
			f.write(" 	")
			f.write("Document")
			f.write(" 		")
			f.write("Ranking")
			f.write(" 	")
			f.write("R/N")
			f.write(" 			")
			f.write("Precision")
			f.write(" 		")
			f.write("Recall")
			f.write("\n")
			for x in range (0, len(recallList)):
				f.write(str(queryId))
				f.write(" 		")
				f.write(str(docs[x]))
				f.write(" 		")
				f.write(str(count))
				f.write(" 		")
				f.write(str(responseList[x]))
				f.write(" 			")
				f.write(str(precisionList[x]))
				f.write(" 			")
				f.write(str(recallList[x]))
				f.write("\n")
				count += 1
			f.write("P@5: " + str(precisionList[4])+"\n")
			f.write("P@20: " + str(precisionList[19])+"\n")
			f.write("Average precision: " + str(average_precision)+"\n")
			f.write("Reciprocal rank: " + str(reciprocal_rank) + "\n")
			if queryId == 64:
				global documents_with_no_relevance_judgements
				dmr = queryId-documents_with_no_relevance_judgements
				f.write("Mean Average precision: " + str(mean_average_precision/dmr)+"\n")
				f.write("Mean Reciprocal rank: " + str(float(mean_reciprocal_rank/dmr)) + "\n")


populateRelevantDictionary()
# populateOutputRelevantDictionary('TF-IDF_output')
# populateResponseList('TF-IDF_EvaluationOutput/')

# populateOutputRelevantDictionary('TF-IDF_Output_Stopping')
# populateResponseList('TF-IDF_Evaluation_Stopping_Output/')

# populateOutputRelevantDictionary('BM_Output')
# populateResponseList('BM_EvaluationOutput/')

# populateOutputRelevantDictionary('JM_Output')
# populateResponseList('JM_EvaluationOutput/')

# populateOutputRelevantDictionary('JM_Output_Stopping')
# populateResponseList('JM_Evaluation_Stopping_Output/')

# populateOutputRelevantDictionary('BM_OutputWithFeedback')
# populateResponseList('BM_QueryEnrichmentEvaluationOutput/')

populateOutputRelevantDictionary('BM_Output_Stopping')
populateResponseList('BM_Evaluation_Stopping_Output/')




