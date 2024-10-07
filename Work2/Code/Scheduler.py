import queue
import threading
from time import sleep
from MyStack import Stack
from MyLogging import logger
from MyCrawler import Crawler, MyItem

SrcPath = "../Src/WebPage"


class MultiThreadCrawler:
    def __init__(self, num_threads=8, breadth_first=True):
        """
        用户需要初始化线程数，以及需要的爬取方式
        id：每一个爬取的网页分配的编号
        lock，cond：线程安全
        InitCon：初始化url处理的容器，深度：栈；广度：队列
        """
        self._num_threads = num_threads
        self._breadth_first = breadth_first
        self._id = 0
        self._lock = threading.Lock()
        self._cond = threading.Condition()
        self._initialize_container()

    def _initialize_container(self):
        """
        容器初始化模块
        _url_allocator: 用来接受需要处理的 urls, 这里容器一定要预先存在数据，放置全部线程阻塞等待
        visited：用来接受已经处理了的 urls
        threads: 用来管理线程
        """
        self._threads = []
        self._visited = []
        if self._breadth_first:
            self._url_allocator = queue.Queue()
        else:
            self.__url_allocator = Stack()

    def _GetId(self):
        """
        为每一个爬取任务分配 id
        """
        with self._lock:
            self._id += 1
        logger.debug(f"此次分配的 id 是 {self._id}")
        return self._id

    def _GetValidUrls(self, item: MyItem):
        """
        将没有处理过的 urls 放入 urls 分配器
        """
        for url in item.IncludedUrl:
            if url not in self._visited:
                self._url_allocator.put(url)
        logger.debug(f"URL分配器最新的链接数目为 {self._url_allocator.qsize()}")

    def ToSave(self, item: MyItem):
        json_str = item.toJson()
        with open(f"{SrcPath}/web_{item.Id}.txt", 'w', encoding='utf-8') as file:
            file.write(json_str)
        logger.info(f"{self._id} 号任务数据保存完毕，任务成功结束")

    def handle_task(self, nums):
        """
        具体的拿到链接后的处理方式
        """
        id = self._GetId()

        while True:
            with self._lock:
                if self._id >= nums: return

            with self._cond:
                while self._url_allocator.empty():
                    self._cond.wait()
                    logger.info(f"{id} 号任务暂停，URL分配器中的 url 为空")

            url = self._url_allocator.get()
            self._visited.append(url)

            spider = Crawler(url)
            item = spider.Work()
            item.Id = id
            item.Url = url

            self._GetValidUrls(item)
            with self._cond:
                self._cond.notify_all()

            self.ToSave(item)

    def Work(self, start_urls, target_num, debug=False):
        self._url_allocator.put(start_urls)
        logger.info(f"本次任务开始将在 3s 后开始, 将展示任务信息...")
        crawl_method = "广度优先" if self._breadth_first else "深度优先"
        logger.info(f"爬取的方式为 {crawl_method}, 使用了 {self._num_threads} 个线程, 目标爬取网页数目为 {target_num}")
        sleep(3)

        # 调试模式
        if debug:
            self.handle_task(target_num)
        else:
            # 这是一个包装函数，用于作为线程的目标
            def task_wrapper():
                self.handle_task(target_num)

            for _ in range(self._num_threads):
                thread = threading.Thread(target=task_wrapper)
                self._threads.append(thread)
                thread.start()
            logger.debug("所有线程已经开始执行任务")

            for t in self._threads:
                t.join()
            logger.debug("所有线程已经退出")
