import jieba
import time
import matplotlib.pyplot as plt
import numpy as np
import json

plt.style.use("fivethirtyeight")
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

DefaultBookPath = "./src/sanguo.txt"
DefaultNamePath = "./src/character.txt"


def ReadFile(Path):
    with open(Path, 'r', encoding="utf-8") as Reader:
        content = Reader.read()
    return content


def SplitWords(FileContent):
    words = list(jieba.cut(FileContent, cut_all=False))
    return words


def InitTable(NameStr):
    NameList = NameStr.split('\n')

    NameDict = {}
    for name in NameList:
        NameDict[name] = []

    return NameDict


def BuildTable(words, NameDict):
    # 遍历分词结果
    index = 0
    for word in words:
        # 若该单词存在于键中，怎添加相应位置
        if word in NameDict.keys():
            NameDict[word].append(index)
        index += len(word)


def InitIndexTable(FileContent, CharacterName):
    # split words
    words = SplitWords(FileContent)
    print(words[:50])

    # 初始化索引表
    IndexTable = InitTable(CharacterName)

    # 遍历分词结果，建立索引表
    BuildTable(words, IndexTable)

    return IndexTable


def BuildNext(patt):
    next = [0]
    PrefixLen = 0

    index = 1
    while index < len(patt):
        if patt[PrefixLen] == patt[index]:
            PrefixLen += 1
            next.append(PrefixLen)
            index += 1
        else:
            if PrefixLen == 0:
                next.append(0)
                index += 1
            else:
                PrefixLen = next[PrefixLen - 1]
    return next


# 顺序查找
def KmpSearch(File, word):
    IndexList = []
    next = BuildNext(word)

    i = 0
    j = 0
    while i < len(File):
        if File[i] == word[j]:
            i += 1
            j += 1
        elif j > 0:
            j = next[j - 1]
        else:
            i += 1
        if j == len(word):
            IndexList.append(i - j)
            j = 0

    return IndexList


def IndexSearch(IndexTable, word):
    return IndexTable[word]


class TimeHelper:
    def __init__(self):
        self.__start = 0
        self.__end = 0

    def start(self):
        self.__start = time.time()
        self.__end = 0

    def stop(self):
        self.__end = time.time()

    def elapsed_time(self):
        if self.__end == 0:
            return time.time() - self.__start
        else:
            return self.__end - self.__start


# 计算索引查找的平均时间
def AverSearchTime(src, tar, Func, times=5):
    TotalTime = 0

    # 计时
    timer = TimeHelper()
    for i in range(times):
        timer.start()
        Func(src, tar)
        timer.stop()
        TotalTime += timer.elapsed_time()

    return TotalTime / times


def CmpSearch(NameList):
    TimeByKMP = []
    for name in NameList:
        TimeByKMP.append(AverSearchTime(FileContent, name, KmpSearch, 10))

    TimeByIS = []
    for name in NameList:
        TimeByIS.append(AverSearchTime(IndexTable, name, IndexSearch, 10))

    plt.figure(figsize=(12, 9))

    pos = np.arange(len(NameList))
    barwidth = 0.3

    plt.bar(pos - barwidth / 2, TimeByIS, color="blue", width=barwidth, label="IndexSearch")
    plt.bar(pos + barwidth / 2, TimeByKMP, color="red", width=barwidth, label="KMPSearch")

    plt.xticks(pos, NameList)

    plt.xlabel('Name')
    plt.ylabel('Time')
    plt.title("查询比较图")
    plt.legend()

    plt.show()


def CmpOverall(InitTime, NameStr):
    NameList = NameStr.split('\n')

    TimeByKMP = [0]
    timer = TimeHelper()
    timer.start()
    for i, name in enumerate(NameList):
        KmpSearch(FileContent, name)
        if (i + 1) % 10 == 0:
            TimeByKMP.append(timer.elapsed_time())

    TimeByIS = [InitTime]
    timer = TimeHelper()
    timer.start()
    for i, name in enumerate(NameList):
        IndexSearch(IndexTable, name)
        if (i + 1) % 10 == 0:
            TimeByIS.append(timer.elapsed_time() + InitTime)

    plt.figure(figsize=(12, 9))

    pos = np.arange(0, 101, 10)

    plt.plot(pos, TimeByKMP, label='KMP Search', marker='o', color="blue")
    plt.plot(pos, TimeByIS, label='IndexSearch Search', marker='x', color="red")

    plt.xlabel("查询次数")
    plt.ylabel("耗时")
    plt.title("累计耗时比较")
    plt.legend()

    plt.show()

if __name__ == '__main__':
    # read file
    FileContent = ReadFile(DefaultBookPath)
    CharacterName = ReadFile(DefaultNamePath)

    # 建立索引表
    timer = TimeHelper()
    timer.start()
    IndexTable = InitIndexTable(FileContent, CharacterName)
    timer.stop()
    InitTime = timer.elapsed_time()

    # 输入需要查找的人物，频率为 高 中 低
    NameList = ["曹操", "荀彧", "张角"]

    # 查询比较
    CmpSearch(NameList)

    # 整体比较
    CmpOverall(InitTime, CharacterName)
