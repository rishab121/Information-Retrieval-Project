import math
from collections import defaultdict
from Helper import *
import re
import operator
from bs4 import BeautifulSoup

class SnippetGeneration:
    def __init__(self):
        self.query = []
        self.helper = Helper()



    def create_term_array_dict(self,qId):
        term_array_dict = {}
        with open('BM_Output/'+str(qId)+'-score.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                ar = line.split()
                with open('parsed_pages/' + ar[0] + '.txt', 'r') as f:
                    reader = f.read()
                    term_array_dict[ar[0]] = reader.split()
        return term_array_dict

    def createSnippetDict(self, qId):
        snippetList = []
        term_array_dict = {}
        term_array_dict = self.create_term_array_dict(qId)
        snippetDict = {}
        for key in term_array_dict.keys():
            i = 0;
            snippet = []
            for term in term_array_dict[key]:
                if i < 4:
                    snippet.append(term)
                    if term not in self.query:
                        i += 1
                    else:
                        i = 0
                else:
                    i = 0
                    snippetList.append(snippet)
                    snippet = []
            snippetDict[key] = snippetList
            snippetList = []
        return snippetDict

    def calcScore(self,qId):
        finalSnippetDict = {}
        snippetDict = {}
        snippetDict = self.createSnippetDict(qId)
        for key in snippetDict.keys():
            maxScore = 0
            maxSnippet = snippetDict[key][0]
            for snippet in snippetDict[key]:
                score = 0
                for term in snippet:
                    if term in self.query:
                        score += 1
                if maxScore < score:
                    maxScore = score
                    maxSnippet = snippet
            finalSnippetDict[key] = maxSnippet

        with open('snippet_output/'+str(qId)+'-snippet.txt', 'w') as f:
            for key in finalSnippetDict.keys():
                f.write(key+" : ")
                for term in finalSnippetDict[key]:
                    if term in self.query:
                        f.write("<b>"+ term + "</b> ")
                    else:
                        f.write(term + " ")
                f.write("\n")


    def main(self):
        queries = self.helper.get_queries();
        for qId in queries.keys():
            self.query = queries[qId].split()
            self.calcScore(qId)

