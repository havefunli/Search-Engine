import json
import jieba
from pathlib import Path


# 读取停用词文件
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set([line.strip() for line in f.readlines()])

# 停用词列表
stopwords = load_stopwords("../src/StopWords.txt")

SrcPath = "../src/WebPage/"
# 创建 Path 对象
directory = Path(SrcPath)
# 使用 iterdir() 获取目录下所有的文件和文件夹
files_path = [SrcPath + f.name for f in directory.iterdir() if f.is_file()]

# 遍历所有文件
for path in files_path:
    with open(path, 'r+', encoding='utf-8') as file:
        web = json.load(file)
        content = web['content']
        # 分词
        words = jieba.cut(content)
        # 去除停用词
        words = [word for word in words if word not in stopwords]

        # 写回文件
        web['words'] = words
        file.seek(0)  # 将文件指针移动到文件开头
        file.truncate()  # 清空文件内容
        json.dump(web, file, ensure_ascii=False)
