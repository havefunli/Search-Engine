import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, id, url):
        self.__Id = id
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
            return Response.status_code
        self.__Html = Response.text
        with open("test.txt", "w+", encoding="utf-8") as file:
            file.write(self.__Html)

    def ParseTitle(self, soup: BeautifulSoup):
        title = soup.find("title")
        return title.string

    def ParseContent(self, soup: BeautifulSoup):
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            return meta_tag['content']
        else:
            return "None..."

    def ParseUrls(self, soup):
        a_tags = soup.findAll("a")
        print(a_tags)

    def Parser(self):
        soup = BeautifulSoup(self.__Html, 'lxml')

        self.__Title = self.ParseTitle(soup)
        print(f"Title: {self.__Title}")
        self.__Content = self.ParseContent(soup)
        print(f"Content: {self.__Content}")
        self.ParseUrls(soup)

    def Work(self):
        self.Downloader()
        self.Parser()
