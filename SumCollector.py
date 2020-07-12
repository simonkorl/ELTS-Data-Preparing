#encoding=utf8

from CorpusStat import CorpusStat
import json
import time

class SumCollector:
    def __init__(self, minimum_words=0):
        self.stat = CorpusStat()
        self.data = []
        self.minimum_words = minimum_words
        self.removed = False

    def add_summ_pair(self, summary, text):
        if(len(text) >= self.minimum_words):
            tmp_dict = {}
            tmp_dict["summary"] = summary
            tmp_dict["text"] = text
            self.data.append(tmp_dict)
            self.stat.stat_once(summary, text)

    def print_stats(self):
        if(self.removed):
            print("Re-calculating statistics...")
            self.stat.clear()
            for dict in self.data:
                self.stat.stat_once(dict["summary"], dict["text"])
        self.stat.print_all()

    def clear(self):
        self.data.clear()
        self.stat.clear()
    
    def pop(self, index=-1):
        self.removed = True
        return self.data.pop(index)

    def load_data(self, path):
        '''load data from SumCollector dump data'''
        with open(path, 'r', encoding='utf-8') as file:
            print("loading from file: " + path)
            self.clear()
            start = time.clock()
            line = file.readline().strip('\r\n')
            while line:
                jsonline = json.loads(line)
                self.data.append(jsonline)
                self.stat.stat_once(jsonline["summary"], jsonline["text"])
                line = file.readline().strip('\r\n')
            end = time.clock()
            print("loading finished. Time: %d" % (end - start))
    
    def dump_data(self, path):
        with open(path, 'w', encoding="utf-8") as file:
            print("writing into file: " + path)
            start = time.clock()
            for dict in self.data:
                jsonline = json.dumps(dict)
                file.write(jsonline)
                file.write('\n')
            end = time.clock()
            print("writing finished. Time: %d" % (end - start))

