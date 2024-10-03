import jieba
import time

DefaultBookPath = "./src/sanguo.txt"
DefaultNamePath = "./src/character.txt"


def ReadFile(Path):
    with open(Path, 'r', encoding="utf-8") as Reader:
        content = Reader.read()
    return content


def SplitWords(FileContent):
    words = jieba.cut(FileContent, cut_all=False)
    return list(words)


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
        self.__start = time.time()
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


if __name__ == '__main__':
    # read file
    FileContent = ReadFile(DefaultBookPath)
    CharacterName = ReadFile(DefaultNamePath)

    # 建立索引表
    IndexTable = InitIndexTable(FileContent, CharacterName)

    timer = TimeHelper()

    timer.start()
    print(IndexSearch(IndexTable, "曹操"))
    timer.stop()
    print(timer.elapsed_time())

    st = time.time()
    print(KmpSearch(FileContent, "曹操"))
    et = time.time()
    print(et - st)



