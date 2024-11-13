from pathlib import Path
import json
import networkx as nx

SrcPath = "../src/WebPage/"


def ReadFile():
    # 所有的连接和子连接
    links = dict()

    # 创建 Path 对象
    directory = Path(SrcPath)

    # 使用 iterdir() 获取目录下所有的文件和文件夹
    files_path = [SrcPath + f.name for f in directory.iterdir() if f.is_file()]

    for path in files_path:
        with open(path, encoding='utf-8') as file:
            link = json.load(file)
        links[link["url"]] = link["urls"]

    return links


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


if __name__ == '__main__':
    links = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': ['G'],
        'E': ['H'],
        'F': [],
        'G': [],
        'H': []
    }

    print(CalPageRank(links))
