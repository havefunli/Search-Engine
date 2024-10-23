import jieba.analyse
import jieba

text = "中国古代史，始于大约170万年前的元谋人，止于1840年的鸦片战争前，是中国原始社会、奴隶社会和封建社会的历史。中国近代史的时间为，从1840年鸦片战争到1949年中华人民共和国成立前，这也是中国半殖民地半封建社会的历史。中国近代史分为前后两个阶段，从1840年鸦片战争到1919年五四运动前夕，是旧民主主义革命阶段；从1919年五四运动到1949年中华人民共和国成立前夕，是新民主主义革命阶段。1949年10月1日中华人民共和国的成立，标志着中国进入了社会主义革命和建设时期。"

# 读取停用词
with open("../../Work2/Src/StopWords.txt", 'r', encoding="utf-8") as file:
    lines = file.readlines()
    stopwords = [line.strip() for line in lines]

# 分词，并去除停用词
words = list(jieba.cut_for_search(text))
words = [word if word not in stopwords else "" for word in words]
keywords = jieba.analyse.textrank(text, topK=6)

# 输出关键词
print(keywords)