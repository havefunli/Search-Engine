import json
from collections import defaultdict
from pathlib import Path

all_words = defaultdict(list)

SrcPath = "../src/WebPage/"
# 创建 Path 对象
directory = Path(SrcPath)
# 使用 iterdir() 获取目录下所有的文件和文件夹
files_path = [SrcPath + f.name for f in directory.iterdir() if f.is_file()]

for path in files_path:
    with open(path, 'r', encoding='utf-8') as file:
        web_page = json.load(file)

        # 读取文件id和文件中的分词
        id = web_page['id']
        words = set(web_page['words'])  # 避免重复单词

        for word in words:
            all_words[word].append(id)

with open("../src/InvertedTable.txt", 'w', encoding="utf-8") as file:
    json.dump(all_words, file, ensure_ascii=False)





