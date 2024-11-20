import jieba
import json
import pandas as pd
from MyCode.MyLogging import logger
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SrcPath = "C:/Users/acer/PycharmProjects/SEHomeWork/SE/MySrc"

with open(f"{SrcPath}/StopWords.txt", encoding="utf-8") as file:
    stopwords = [line.strip() for line in file]

with open(f"{SrcPath}/InvertedTable.txt", encoding="utf-8") as file:
    inverted_table = json.load(file)


def preprocess_text(text):
    """分词并且剔除停用词"""
    words = list(jieba.cut(text))
    words = [word for word in words if word not in stopwords]
    return words


"""""
获取网页索引的逻辑，原来是按照倒排表获取索引然后取交集
但是如果出现搜索词过于稀少，会导致获取极少的网页索引
所以需要修改逻辑
"""""


def GetWordsIndex(words, threshold=0.25):
    if len(words) == 0: return

    # 已经处理的索引
    handled_indexes = set()
    # 有效的网页内容
    valid_page = []

    for word in set(words):
        # 获取该词对应的索引
        word_index = inverted_table.get(word, None)
        if word_index is None: continue

        for index in word_index:
            # 如果被处理过，直接跳过
            if index in handled_indexes: continue

            handled_indexes.add(index)
            # 处理逻辑，获取该索引对应的内容
            with open(f"{SrcPath}/WebContent/{index}.txt", 'r', encoding='utf-8') as file:
                page = json.load(file)

            # 判断所有关键词的1/2（默认阈值）是否存在于该网页
            # 没有达到要求直接跳过
            if len(set(page['words']).intersection(set(words))) / len(words) < threshold: continue

            valid_page.append(page)

    return pd.DataFrame(valid_page)


def GetTopWeb(n, web_pages):
    if web_pages is None or len(web_pages) == 0: return

    # 1. 根据 PageRank 排序
    web_pages.sort_values('pagerank', ascending=False)

    # 3. 获取前 n 个网页
    top_web_pages = web_pages[:n]  # 获取前 n 个网页

    # 4. 清理剩余的网页（删除不需要的网页对象，释放内存）
    del web_pages

    return top_web_pages  # 返回前 n 个网页


def cal_tfidf_similarities(web_pages, words):
    if web_pages is None or len(web_pages) == 0: return

    # 提取每一个网页的内容
    words_list = web_pages['words']
    documents = [' '.join(words) for words in words_list]

    # 计算 TF-IDF 向量
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 转换查询文本为向量
    query_vec = vectorizer.transform([' '.join(words)])

    # 计算查询与文档的余弦相似度
    cos_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

    return cos_similarities


def GenerateScore(web_pages):
    if web_pages is None or len(web_pages) == 0: return

    df = pd.DataFrame(web_pages)

    # 将值标准化
    scaler = MinMaxScaler()
    df[['pagerank', 'tfidf']] = scaler.fit_transform(df[['pagerank', 'tfidf']])

    # 计算分数 score = 0.6 * tfidf + 0.4 * pagerank
    df['score'] = 0.6 * df['tfidf'] + 0.4 * df['pagerank']

    df = df.sort_values('score', ascending=False)

    return df


def QueryWebPages(content):
    if content is None: return "NULL..."

    # 分词，去除停用词
    key_words = preprocess_text(content)
    logger.info(f"key words = {key_words}")

    # 获取每个词对应的网页集合
    valid_page = GetWordsIndex(key_words)
    if valid_page is not None:
        logger.info(f"len(Indexes)= {len(valid_page)}")

    # 根据 pagerank 获取前 100 个网页
    top_web_pages = GetTopWeb(200, valid_page)
    if top_web_pages is not None:
        logger.info(f"index = {list(top_web_pages['id'])}")

    cosine_similarity = cal_tfidf_similarities(top_web_pages, key_words)
    # print(cosine_similarity)

    # 将对应的tfidf写入文件
    if top_web_pages is not None:
        top_web_pages.loc[:, 'tfidf'] = cosine_similarity

    # 将网页评分排序
    web_page = GenerateScore(top_web_pages)

    if web_page is not None:
        return web_page
    else:
        return "没有找到相关内容...\n"


if __name__ == "__main__":
    while True:
        content = input("请输入搜素内容：")
        print(QueryWebPages(content))
