import json
import requests
import validators
from MyLogging import logger
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

'''''
本模块只是负责对数据的爬取
并对解析的数据提取标题正文链接等之后返回
'''''
PrefixUrl = "https://baike.baidu.com"

def IsValidUrl(url):
    if not validators.url(url):
        return False
    else:
        return True


class MyItem:
    def __init__(self):
        self.isvalid = False
        self.Id = -1
        self.Url = ""
        self.Html = ""
        self.Title = ""
        self.Content = ""
        self.IncludedUrl = []
        self.ImgUrl = ""

    def toJson(self):
        item_dict = {
            "id": self.Id,
            "url": self.Url,
            "title": self.Title,
            "content": self.Content,
            "urls": self.IncludedUrl
        }

        return item_dict
        # json_str = json.dumps(item_dict, ensure_ascii=False)
        # return json_str


class Crawler:
    def __init__(self, url):
        self._Url = url
        self._Html = ""
        self._Title = ""
        self._Content = ""
        self._IncludedUrl = []
        self._ImgUrl = ""
        self._ua = UserAgent()

    # 该模块主要用于爬取数据
    def Downloader(self):
        # 先检查链接的正确性
        if not IsValidUrl(self._Url):
            logger.warning(f"{self._Url} is invalid!")
            return -1

        # 随机一个用户代理
        headers = {
            "User-Agent": self._ua.random}

        # 若没成功获取数据直接返回错误码
        try:
            Response = requests.get(self._Url, headers=headers, stream=True)
            Response.raise_for_status()  # 如果响应状态码不是 200，将抛出 HTTPError

            if Response.ok:
                logger.debug(f"{self._Url} 成功爬取该网页")
                self._Html = Response.text
                return 200

        except requests.exceptions.RequestException as e:
            # 捕获所有 requests 相关的异常
            status_code = getattr(e.response, 'status_code', None) if e.response else None
            logger.warning(
                f"{self._Url} 请求时发生异常: {e}, 返回错误码 {status_code if status_code is not None else '未知'}")
            return status_code if status_code is not None else -1  # 返回错误码或自定义的错误码

    # 解析标题
    def ParseTitle(self, soup: BeautifulSoup):
        title = soup.find("title")
        logger.debug(f"已解析标题: {title}")
        if title:
            self._Title = title.string
        else:
            return "None"

    # 解析正文
    def ParseContent(self, soup: BeautifulSoup):
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag:
            content = meta_tag['content']
            logger.debug(f"成功解析正文: {content}")
            self._Content = content
        else:
            logger.warning("该正文内容为空")
            return "None"

    # 获取超链接
    def ParseUrls(self, soup):
        a_tags = soup.findAll("a", href=True)

        for a in a_tags:
            href = a['href']
            # 去除片段标识符
            if "#" not in href and "/s" not in href:
                self._IncludedUrl.append(a['href'])

        # 简单的链接处理添加资源路径
        self._IncludedUrl = [PrefixUrl + url if not url.startswith(("http://", "https://")) else url
                             for url in self._IncludedUrl]

        # 去除其他域下的链接
        self._IncludedUrl = self._IncludedUrl = [url for url in self._IncludedUrl if url.startswith(PrefixUrl)]
        logger.debug("成功获取所有子链接")

    def _ParserImgUrl(self, soup):
        # 查找 meta 标签
        meta_tag = soup.find('meta', property='og:image')

        # 获取 content 属性
        if meta_tag and 'content' in meta_tag.attrs:
            image_url = meta_tag['content']
            logger.info(f'获取到的图片链接是: {image_url}')
            self._ImgUrl = image_url
        else:
            logger.warning('未找到指定的 meta 标签')

    def Parser(self, item):
        soup = BeautifulSoup(self._Html, 'lxml')

        self.ParseTitle(soup)
        self.ParseContent(soup)
        self.ParseUrls(soup)
        self._ParserImgUrl(soup)

        logger.debug(f"{item.Id} 号的解析任务完成")

    def Pack(self, item):
        item.isvalid = True
        item.Title = self._Title
        item.Html = self._Html
        item.Content = self._Content
        item.IncludedUrl = self._IncludedUrl
        item.ImgUrl = self._ImgUrl

    def Work(self, item: MyItem):

        # 若没有正常链接下载，不解析数据直接返回
        if self.Downloader() != 200: return
        self.Parser(item)
        self.Pack(item)
