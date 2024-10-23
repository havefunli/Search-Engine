import re


def get_shingles(text, k):
    """生成 k-shingles."""
    return {text[i:i + k] for i in range(len(text) - k + 1)}


def jaccard_similarity(shingles_a, shingles_b):
    """计算 Jaccard 相似度."""
    intersection = shingles_a.intersection(shingles_b)
    union = shingles_a.union(shingles_b)
    return len(intersection) / len(union) if union else 0, intersection


def highlight_duplicates(text, duplicates):
    """高亮显示重复字符串（控制台使用 ANSI 转义码）。"""
    for dup in sorted(duplicates, key=len, reverse=True):
        text = text.replace(dup, f'\033[1;31m{dup}\033[0m')  # 红色高亮
    return text



def analyze_texts(text_a, text_b, k):
    """分析文本并打印 Jaccard 相似度，并高亮重复的 k-shingles."""
    if k <= 0 or k > min(len(text_a), len(text_b)):
        raise ValueError("k 必须是一个正整数，并且不超过最短文本的长度")

    shingles_a = get_shingles(text_a, k)
    shingles_b = get_shingles(text_b, k)
    similarity, duplicates = jaccard_similarity(shingles_a, shingles_b)

    highlighted_a = highlight_duplicates(text_a, duplicates)
    highlighted_b = highlight_duplicates(text_b, duplicates)

    print(f'k={k} 的 Jaccard 相似度: {similarity:.2f}\n')
    print("文本 A:\n", highlighted_a, "\n")
    print("文本 B:\n", highlighted_b, "\n")


# 示例文本
text_a = "中国古代史，始于大约170万年前的元谋人，止于1840年的鸦片战争前，是中国原始社会、奴隶社会和封建社会的历史。中国近代史的时间为，从1840年鸦片战争到1949年中华人民共和国成立前，这也是中国半殖民地半封建社会的历史。中国近代史分为前后两个阶段，从1840年鸦片战争到1919年五四运动前夕，是旧民主主义革命阶段；从1919年五四运动到1949年中华人民共和国成立前夕，是新民主主义革命阶段。1949年10月1日中华人民共和国的成立，标志着中国进入了社会主义革命和建设时期。"
text_b = "从1840年鸦片战争到1919年五四运动前夕，是旧民主主义革命阶段；从1919年五四运动到1949年中华人民共和国成立前夕，是新民主主义革命阶段。1949年10月1日中华人民共和国的成立，标志着中国进入了社会主义革命和建设时期。"

# 进行分析
analyze_texts(text_a, text_b, 3)