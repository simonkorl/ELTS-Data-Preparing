class CorpusStat:
    def __init__(self, rank=21):
        self.rank = rank
        self.clear()
    
    def clear(self):
        # total
        self.total_sum_len = 0
        self.total_text_len = 0

        self.text_stat = [0 for i in range(self.rank)] # the number of texts longer or equal than (1000 * index)

        # max and min
        self.max_len = 0
        self.min_len = 2147483647

    def stat_once(self, summary, text):
        sum_len = len(summary)
        text_len = len(text)
        # total
        self.total_sum_len += sum_len
        self.total_text_len += text_len
        for i in range(self.rank):
            if(text_len >= i * 1000):
                self.text_stat[i] += 1

        # max and min
        if(text_len > self.max_len):
            self.max_len = text_len
        
        if(text_len < self.min_len):
            self.min_len = text_len

    def print_avrg_len(self):
        print("---------------average length --------------")
        print("summary: %f" % (self.total_sum_len / self.text_stat[0]))
        print("text: %f" % (self.total_text_len / self.text_stat[0]))
    
    def print_stat(self):
        print("----------------------text number statistics ---------------")
        for i in range(self.rank):
            print("%d+:\t%d\t%.2f" % (i * 1000, self.text_stat[i], self.text_stat[i] / self.text_stat[0] * 100))
    
    def print_max_min_len(self):
        print("-----------------------max min length --------------")
        print("max text length: %d" % self.max_len)
        print("min text length: %d" % self.min_len)

    def print_all(self):
        self.print_avrg_len()
        self.print_max_min_len()
        self.print_stat()