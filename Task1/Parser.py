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
        self.parse()

    def parse(self):
        for file in os.listdir(self.raw_pages_dir):
            file_path = self.raw_pages_dir + file
            f = open(file_path, 'r+')
            raw_data = f.read()
            bs = BeautifulSoup(raw_data, 'html.parser')            
            #self.remove_all_external_and_media_links(bs)
            self.text_data = []
            # get title text
            pre = bs.find('pre')
            pre_text = pre.get_text()
            self.text_data.append(pre_text)

            # convert list to string
            self.text_data = u' '.join(self.text_data).encode('utf-8')

            # transformations
            if self.remove_punctuation:
                self.remove_punctuation_in_data()

            if self.perform_casefolding:
                self.text_data = self.text_data.lower()

            # store data
            self.save_to_file(file)

    def remove_punctuation_in_data(self):
        regex = r"(?!\d)[.,;](?!\d)"
        regex2 = r"[(){}\"#~\[\]<>=:?!@&'|*]"
        regex3 = r"(?!\d|\w)[-/$](?!\d|\w)"
        self.text_data = re.sub(regex, "", self.text_data, 0)
        self.text_data = re.sub(regex2, "", self.text_data, 0)
        self.text_data = re.sub(regex3, "", self.text_data, 0)

    def save_to_file(self, file_name):
        file_name = file_name.replace('html', 'txt')
        file_name = './parsed_pages/' + file_name
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