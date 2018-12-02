import os
class Stopper:

    def __init__(self):
        self.parsed_pages_dir = "../Task1/parsed_pages/"
        self.stopwords_file = "../test-collection/common_words"
        self.output_dir = "./stopped_pages_output/"
        self.prepare_stoplist()
    
    def stopper(self):
        for file in os.listdir(self.parsed_pages_dir):
            file_path = self.parsed_pages_dir + file
            with open(file_path, 'r') as f:
                text_data = f.read().split()
                new_data = []
                for word in text_data:
                    if word not in self.stop_words:
                        new_data.append(word)
                new_data = ' '.join(new_data)
                output_file = self.output_dir + file
                with open(output_file, 'w') as o:
                    o.write(new_data)

    def prepare_stoplist(self):
        with open(self.stopwords_file, 'r') as f:
            text_data = f.read().split()
            self.stop_words = text_data

s = Stopper()
s.stopper()