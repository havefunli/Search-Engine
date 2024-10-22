import networkx as nx
from matplotlib import pyplot as plt


class MyPageRank:
    def __init__(self, ):
        self._iter = 0
        self._tol = 1e-1
        self._alpha = 0.85
        self._graph = {}

    def Init(self, iteration=100, tolerance=1e-5):
        """
        :param iteration: 最大迭代次数
        :param tolerance: 最小收敛值
        """
        self._iter = iteration
        self._tol = tolerance

    def PageRank(self, graph: dict, fac=0.85):
        num_nodes = len(graph)

        if num_nodes == 0:
            return {}

        pagerank = {node: 1 / num_nodes for node in graph}

        for _ in range(self._iter):
            new_pr = {node: (1 - fac) / num_nodes for node in graph}

            for node in graph:
                for other_node in graph:
                    if node in graph[other_node]:
                        len_links = len(graph[other_node])
                        new_pr[node] += fac * pagerank[other_node] / len_links

            # 检查收敛
            if all(abs(new_pr[node] - pagerank[node]) < self._tol for node in graph):
                break

            pagerank = new_pr

        return pagerank


def ReadGraph(Path: str):
    graph = {}

    # 处理文本数据
    with open(Path, 'r') as file:
        while True:
            content = file.readline()
            if not content:
                break

            nodes = content.strip().split(" ")
            source = nodes[0]  # 起始节点
            target = nodes[1]  # 目标节点

            # 确保源节点存在于图中
            if source not in graph:
                graph[source] = []
            # 添加目标节点到源节点的邻接列表
            graph[source].append(target)

    return graph


if __name__ == '__main__':
    graph = ReadGraph("../Src/pagerank_seven_nodes.txt")

    cal = MyPageRank()
    cal.Init()
    result1 = cal.PageRank(graph)
    print(f"result1: {result1}")

    G = nx.DiGraph()
    for url, links in graph.items():
        for link in links:
            G.add_edge(url, link)
    result2 = nx.pagerank(G, alpha=0.85)
    print(f"result2: {result2}")



