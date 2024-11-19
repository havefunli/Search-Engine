import jieba
import json

with open("../src/StopWords.txt", encoding="utf-8") as file:
    stopwords = [line.strip() for line in file]

with open("../src/InvertedTable.txt", encoding="utf-8") as file:
    inverted_table = json.load(file)


def preprocess_text(text):
    """分词并且剔除停用词"""
    words = list(jieba.cut(text))
    words = [word for word in words if word not in stopwords]
    return words

def GetWordsIndex(words):
    # 集合避免重复
    word_indexes = set()

    for word in set(words):
        index = inverted_table.get(word, None)

        # 防止没有找到对应词，导致集合相交为空
        if index:
            if len(word_indexes) == 0: #
                word_indexes = set(index)
            else:
                word_indexes = word_indexes.intersection(set(index)) # 集合取交集

    return word_indexes


def GetTopWeb(n, indexes):
    web_pages = []

    # 1. 加载网页并计算 PageRank
    for index in indexes:
        with open(f"../src/WebPage/web_{index}.txt", 'r', encoding='utf-8') as file:
            web_page = json.load(file)
            web_pages.append(web_page)

    # 2. 根据 PageRank 排序
    web_pages.sort(key=lambda x: x["pagerank"], reverse=True)  # 降序排序

    # 3. 获取前 200 个网页
    top_web_pages = web_pages[:n]  # 获取前 n 个网页

    # 4. 清理剩余的网页（删除不需要的网页对象，释放内存）
    del web_pages

    return top_web_pages  # 返回前 n 个网页

# def SortedByTFIDF(web_page):


if __name__ == '__main__':
    content = "中国历史有明朝！"
    words = preprocess_text(content)

    # 获取每个词对应的索引集合
    indexes = GetWordsIndex(words)

    top_web_pages = GetTopWeb(10, indexes)

