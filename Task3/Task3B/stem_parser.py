# references
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
# https://www.regular-expressions.info/alternation.html
# https://regexone.com/

from bs4 import BeautifulSoup
import os
import string
import re


class Parser:
    def __init__(self):
        self.perform_casefolding = True
        self.remove_punctuation = True
        # Path to raw documents
        self.raw_pages_dir = "../test-collection/corpus/"

    def run(self):
        print "running parser"
        with open('../../test-collection/cacm_stem.txt', 'r') as f:
            raw_data = f.read().split('#')
            raw_data = raw_data[1:]
            for file_data in raw_data:
                lines = file_data.splitlines()
                document_number = lines.pop(0).strip()
                self.text_data = '\n'.join(lines).encode('utf-8')
                if 'pm' in self.text_data:
                    pm_split = self.text_data.split('pm')
                    self.text_data = pm_split[0] + 'pm'
                elif 'am' in self.text_data:
                    self.text_data = self.text_data.split('am')[0]
                    self.text_data += 'am'
                if self.perform_casefolding:
                    self.text_data = self.text_data.lower()
                self.save_to_file(document_number)
                

    def save_to_file(self, file_name):
        file_name = './stemmed_parsed_pages/' + 'cacm-' + file_name.strip() + '.txt'
        file_name = file_name.lower()
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as err:
                pass

        with open(file_name, 'w') as f:
            f.write(self.text_data)


p = Parser()
p.run()
