import json
import requests
from MyLogging import logger
from bs4 import BeautifulSoup

'''''
本模块只是负责对数据的爬取
并对区区的数据提取标题正文链接等之后返回
'''''
PrefixUrl = "https://baike.baidu.com"

class MyItem:
    def __init__(self):
        self.Id = -1
        self.Url = ""
        self.Html = ""
        self.Title = ""
        self.Content = ""
        self.IncludedUrl = []

    def toJson(self):
        item_dict = {
            "id": self.Id,
            "url": self.Url,
            "title": self.Title,
            "content": self.Content,
            "urls": self.IncludedUrl
        }

        json_str = json.dumps(item_dict, ensure_ascii=False)
        return json_str

class Crawler:
    def __init__(self, url):
        self.__Url = url
        self.__Html = ""
        self.__Title = ""
        self.__Content = ""
        self.__IncludedUrl = []

    # 该功能主要用于爬取数据
    def Downloader(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"}

        Response = requests.get(self.__Url, headers=headers, stream=True)
        if not Response.ok:
            status_code = Response.status_code
            logger.warning(f"{self.__Url} 未正常连接，返回错误码 {status_code}")
            return status_code
        logger.debug(f"{self.__Url} 成功爬取该网页")
        self.__Html = Response.text

    def ParseTitle(self, soup: BeautifulSoup):
        title = soup.find("title")
        logger.debug(f"已解析标题: {title}")
        if title:
            return title.string
        else:
            return "None"

    def ParseContent(self, soup: BeautifulSoup):
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            content = meta_tag['content']
            logger.debug(f"成功解析正文: {content}")
            return content
        else:
            logger.warning("该正文内容为空")
            return ""

    def ParseUrls(self, soup):
        a_tags = soup.findAll("a", href=True)
        for a in a_tags:
            href = a['href']
            # 去除片段标识符
            if "#" not in href:
                self.__IncludedUrl.append(a['href'])

        # 简单的链接处理添加资源路径
        self.__IncludedUrl = [PrefixUrl + url if not url.startswith(("http://", "https://")) else url
                              for url in self.__IncludedUrl]
        logger.debug("成功解析所有子链接")

    def Parser(self):
        soup = BeautifulSoup(self.__Html, 'lxml')

        self.__Title = self.ParseTitle(soup)
        self.__Content = self.ParseContent(soup)
        self.ParseUrls(soup)
        logger.debug(f"{self.__Url} 的解析任务完成")

    def Work(self):
        self.Downloader()
        self.Parser()

        item = MyItem()
        item.Title = self.__Title
        item.Html = self.__Html
        item.Content = self.__Content
        item.IncludedUrl = self.__IncludedUrl

        return item
