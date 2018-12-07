import math
from collections import defaultdict
import re
import operator
from bs4 import BeautifulSoup

class SnippetGeneration:
    def __init__(self, q):
        self.query = "What articles exist which deal with TSS (Time Sharing System), an operating system for IBM computers?"



    def create_term_array_dict(self):
        term_array_dict = {}
        #for i in range(1, 65):
        with open('BM_Output/'+str(1)+'-score.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                ar = line.split()
                with open('parsed_pages/' + ar[0] + '.txt', 'r') as f:
                    reader = f.read()
                    term_array_dict[ar[0]] = reader.split()
        return term_array_dict

    def createSnippetDict(self):
        snippetList = []
        term_array_dict = {}
        term_array_dict = self.create_term_array_dict()
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
                    snippetList.append(snippet)
            snippetDict[key] = snippetList

        return snippetDict

    def calcScore(self):
        finalSnippetDict = {}
        snippetDict = {}
        snippetDict = self.createSnippetDict()
        for key in snippetDict.keys():
            for snippetList in snippetDict[key]:
                maxScore = 0
                maxSnippet = snippetList[0]
                for snippet in snippetList:
                    score = 0
                    for term in snippet:
                        if term in self.query:
                            score += 1
                    if maxScore < score:
                        maxScore = score
                        maxSnippet = snippet
                finalSnippetDict[key] = maxSnippet
        for key in finalSnippetDict.keys():
            print(finalSnippetDict[key])




