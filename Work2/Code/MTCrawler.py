import queue
import threading
from MyStack import Stack
from MyCrawler import Crawler, MyItem


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
        self._id = -1
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
        return self._id

    def _GetValidUrls(self, item: MyItem):
        """
        将没有处理过的 urls 放入 urls 分配器
        """
        for url in item.IncludedUrl:
            if url not in self._visited:
                self._url_allocator.put(url)

    def ToSave(self, item: MyItem):
        json_str = item.toJson()
        with open(f"./web_{item.Id}.txt", 'w') as file:
            file.write(json_str)

    def handle_task(self, nums):
        """
        具体的拿到链接后的处理方式
        """
        while True:
            with self._lock:
                if self._id >= nums: return

            with self._cond:
                while self._url_allocator.empty(): self._cond.wait()

            url = self._url_allocator.get()
            self._visited.append(url)
            id = self._GetId()

            spider = Crawler(url)
            item = spider.Work()
            item.Id = id
            item.Url = url

            self._GetValidUrls(item)
            with self._cond:
                self._cond.notify_all()

            self.ToSave(item)

    def Work(self, start_urls, target_num):
        # 这是一个包装函数，用于作为线程的目标
        # def task_wrapper():
        #     self.handle_task(NumOfWebs)
        #
        # for _ in range(self._num_threads):
        #     thread = threading.Thread(target=task_wrapper)
        #     self._threads.append(thread)
        #     thread.start()
        #
        # for t in self._threads:
        #     t.join()
        self._url_allocator.put(start_urls)
        self.handle_task(1)













