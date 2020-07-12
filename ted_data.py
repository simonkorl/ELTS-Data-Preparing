# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
# inpect TED data
import json
from SumCollector import SumCollector

ted_zh = "/search/odin/data/summarization_data/ted_data/ted_zh_json"


# %%
# collect data
collector = SumCollector()

with open(ted_zh, 'r', encoding='utf-8') as file:
    line = file.readline().strip('\r\n')
    while(line):
        jsonline = json.loads(line)
        summary = jsonline['full_abs']
        text_list = jsonline['document']
        text = ''.join(text_list)
        collector.add_summ_pair(summary, text)
        line = file.readline().strip('\r\n')
collector.print_stats()


# %%
collector.dump_data("/search/odin/data/summarization_data/custom_data/custom_ted_train_data")

