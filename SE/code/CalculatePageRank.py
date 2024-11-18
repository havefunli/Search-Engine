import json
from pathlib import Path
import networkx as nx

SrcPath = "../src/WebPage/"
# 创建 Path 对象
directory = Path(SrcPath)
# 使用 iterdir() 获取目录下所有的文件和文件夹
files_path = [SrcPath + f.name for f in directory.iterdir() if f.is_file()]

# 读取文件的 url 以及 urls
def ReadFile():
    # 所有的连接和子连接
    links = dict()

    for path in files_path:
        with open(path, 'r', encoding='utf-8') as file:
            link = json.load(file)
        links[link["url"]] = link["urls"]

    return links

# 计算每一个网页的 pagerank
def CalPageRank(links: dict):
    # 生成图
    G = nx.Graph()
    # 添加边和点
    for url, sub_links in links.items():
        # url 为点，子链接为边
        G.add_node(url)
        # 若该子链接为被爬取直接丢弃
        for link in sub_links:
            if link in links.keys():
                G.add_edge(link, url)

    return nx.pagerank(G)

# 将网页的 pagerank 写回文件
def WriteBack(pagerank):
    for path in files_path:
        with open(path, 'r+', encoding='utf-8') as file:
            link = json.load(file)
            link['pagerank'] = pagerank.get(link['url'], 0)  # 如果没有pagerank，默认为0
            file.seek(0)  # 将文件指针移动到文件开头
            file.truncate()  # 清空文件内容
            json.dump(link, file, ensure_ascii=False)


if __name__ == '__main__':
    links = ReadFile()
    pr = CalPageRank(links)
    WriteBack(pr)
