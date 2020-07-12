# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
from SumCollector import SumCollector

data_path = '/search/odin/data/summarization_data/'

summ1k_path = data_path + 'custom_data/integrated_train_data_1k'
summ5k_path = data_path + 'custom_data/integrated_train_data_5k'
summ10k_path = data_path + 'custom_data/integrated_train_data_10k'

summ_paths = [summ1k_path, summ5k_path, summ10k_path]


# %%
# Auxiliary functions
def calcNonChineseRate(text):
    non_chinese_sum = 0
    for char in text:
        if not ('\u4e00' <= char <= '\u9fa5'):
            non_chinese_sum += 1
    return (non_chinese_sum) / len(text)


# %%
# washing pipeline
def wash_data(collector):
    # discard data if it has too many non-Chinese charactors
    for i in range(len(collector.data) - 1, -1, -1):
        if(calcNonChineseRate(collector.data[i]["text"]) > 0.25):
            collector.pop(i)

#%%
i = 0
for path in summ_paths:
    if(i == 0):
        i = 1
    elif(i == 1):
        i = 5
    elif(i == 5):
        i = 10
    collector = SumCollector()
    collector.load_data(path)
    wash_data(collector)
    output_path = '/search/odin/data/summarization_data/custom_data/washed_train_data_%dk' % i
    collector.dump_data(output_path)
    