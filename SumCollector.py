#encoding=utf8

from CorpusStat import CorpusStat
import json

class SumCollector:
    def __init__(self, minimum_words=0):
        self.stat = CorpusStat()
        self.data = []
        self.minimum_words = minimum_words

    def add_summ_pair(self, summary, text):
        if(len(text) >= self.minimum_words):
            tmp_dict = {}
            tmp_dict["summary"] = summary
            tmp_dict["text"] = text
            self.data.append(tmp_dict)
            self.stat.stat_once(summary, text)

    def print_stats(self):
        self.stat.print_all()

    def clear(self):
        self.data.clear()
        self.stat.clear()

    def load_data(self, path):
        '''load data from SumCollector dump data'''
        with open(path, 'r', encoding='utf-8') as file:
            print("loading from file: " + path)
            self.data = json.load(file)
            self.stat.clear()
            for dict in self.data:
                self.stat.stat_once(dict["summary"], dict["text"])
            print("loading finished")
    
    def dump_data(self, path):
        with open(path, 'w', encoding="utf-8") as file:
            print("writing into file: " + path)
            json.dump(self.data, file)
            print("writing finished")

