import codecs
import os
from tqdm import tqdm # 一个进度条
from bs4 import BeautifulSoup
from opencc import OpenCC # 一个简体中文和繁体中文互相转换的文件
import shutil # 高阶文件处理单元，可以进行文件的拷贝等工作
import json
import numpy as np
class ted_passage():
    def __init__(self):
        self.title = ""
        self.whole_sum = ""
        self.transcript = []
        self.footnote = []

abs_len = []
document_len = []
document_len_big_sent = []
document_len_small_sent = []
whole_p = 0
all_data = []
coverage = 0
big_punc = ["。","？","！", "?", "!"]
small_punc = ["，","；",",",";"]


cc = OpenCC('tw2sp')
list_dir_path = "www.ted.com"
list_dir = os.listdir(list_dir_path)
print(len(list_dir))
ted_map = {}
if not os.path.exists("ted_zh"):
    os.mkdir("ted_zh")
if not os.path.exists("ted_en"):
    os.mkdir("ted_en")

with tqdm(total= len(list_dir)) as pbar:
    for html_file in list_dir:
        pbar.update(1)
        htmlfile_reader = open(os.path.join(list_dir_path, html_file), 'r', encoding='utf-8')
        htmlhandle = htmlfile_reader.read()
        soup = BeautifulSoup(htmlhandle, 'html.parser')
        all_text = soup.text
        if "\"language\":\"en\"" in all_text:
            shutil.copy(os.path.join(list_dir_path, html_file), os.path.join("ted_en", html_file))
            continue
        shutil.copy(os.path.join(list_dir_path, html_file), os.path.join("ted_zh", html_file))
        if "transcript" in html_file:
            ted_name = html_file.replace("_transcript", "")
            if ted_name not in ted_map:
                ted_map[ted_name] = ted_passage()
            title = cc.convert(soup.head.title.text.replace("| TED Talk Subtitles and Transcript | TED", ""))
            ted_map[ted_name].transcript.append(title)
            description = cc.convert(soup.find(attrs={"name": "description"})['content'])
            ted_map[ted_name].title = title
            ted_map[ted_name].whole_sum = description.replace("TED Talk Subtitles and Transcript: ", "")
            for m in soup.body.findAll('div', attrs={'class': 'Grid__cell flx-s:1 p-r:4'}):
                trans = cc.convert(m.text.strip().replace("\n", "").replace("\t",""))
                trans = trans.replace("（笑声）","")
                if len(trans)>6:
                    ted_map[ted_name].transcript.append(trans)
        '''
        else:
            ted_name = html_file
            if ted_name not in ted_map:
                ted_map[ted_name] = ted_passage()
            title = cc.convert(soup.head.title.text.replace(" | TED Talk", ""))

            description = cc.convert(soup.find(attrs={"name": "description"})['content'])
            ted_map[ted_name].title=title
            ted_map[ted_name].whole_sum = description
        '''
#save this content
print(len(ted_map))
ted_json = []

for key, values in ted_map.items():
    if len(values.transcript)>1:
        small_punc_abs_number = 0
        big_punc_abs_number = 0
        small_punc_doc_number = 0
        big_punc_doc_number = 0
        abs_char_list = list(set(values.whole_sum))
        doc_char_list = list(set(" ".join(values.transcript)))
        not_in_doc = list(set(list(set(abs_char_list).difference(set(doc_char_list)))))
        if len(not_in_doc)>10:
            print(not_in_doc)
            coverage+=1

            continue
        abs_len.append(len(values.whole_sum))
        document_len.append(len("".join(values.transcript)))
        for char in values.whole_sum:
            if char in big_punc:
                small_punc_abs_number+=1
                big_punc_abs_number+=1
            if char in small_punc:
                small_punc_abs_number+=1
        for char in "".join(values.transcript):
            if char in big_punc:
                small_punc_doc_number+=1
                big_punc_doc_number+=1
            if char in small_punc:
                small_punc_doc_number+=1
        document_len_big_sent.append(big_punc_doc_number)
        document_len_small_sent.append(small_punc_doc_number)
        json_content = {"title": values.title, "full_abs": values.whole_sum, "document":values.transcript}
        ted_json.append(json.dumps(json_content, ensure_ascii=False))

print("mean abstract char number:")
print(np.mean(abs_len))

print("mean document char number:")
print(np.mean(document_len))

print("small sen mean number:")
print(np.mean(document_len_small_sent))

print("big sen mean number:")
print(np.mean(document_len_big_sent))

print("not contain in abs:")
print(coverage)

write_path_ted = codecs.open("ted_zh_json", "w", "utf-8")
for ted_j in ted_json:
    write_path_ted.write(ted_j + "\n")
