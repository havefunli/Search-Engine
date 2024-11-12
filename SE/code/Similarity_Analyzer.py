import jieba
from MyLogging import logger

with open("../src/StopWords.txt", encoding="utf-8") as file:
    stopwords = [line.strip() for line in file]


def preprocess_text(text):
    """分词并且剔除停用词"""
    words = list(jieba.cut(text))
    words = [word for word in words if word not in stopwords]
    return set(words)

def jaccard_similarity(set1, set2):
    """计算两个文本的 Jaccard 相似度"""

    # 计算交集和并集的大小
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    # 计算 Jaccard 相似度
    similarity = len(intersection) / len(union) if len(union) > 0 else 0
    return similarity


