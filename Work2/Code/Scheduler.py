import queue
import json
import threading
from time import sleep
from MyStack import Stack
from MyLogging import logger
from MyCrawler import Crawler, MyItem

SrcPath = "../Src/WebPage"
BackupPath = "../Src/BackUp"


class MultiThreadCrawler:
    def __init__(self, num_threads=8, breadth_first=True):
        """
        用户需要初始化线程数，以及需要的爬取方式
        id：每一个爬取的网页分配的编号
        lock，cond：线程安全
        InitCon：初始化url处理的容器，深度：栈；广度：队列
        """
        self._isworking = True
        self._num_threads = num_threads
        self._breadth_first = breadth_first
        self._id = 0
        self._target_num = -1
        self._lock = threading.Lock()
        self._cond = threading.Condition()
        self._initialize_container()


    def stop(self):
        with self._lock:
            self._isworking = False

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
            self._url_allocator = Stack()

    def back_up(self):
        unprocessed_urls = []
        if not self._url_allocator.empty():
            unprocessed_urls.append(self._url_allocator.get())

        with open(f"{BackupPath}/unprocessed.txt", 'w', encoding='utf-8') as file:
            json.dump(unprocessed_urls, file)
        logger.debug("未处理的链接已保存")

        with open(f"{BackupPath}/processed.txt", 'w', encoding='utf-8') as file:
            json.dump(self._visited, file)
        logger.debug("已处理的链接已保存")

        config_dict = {
            "ID": self._id,
            "Target_Num": self._target_num,
            "Threads_Num": self._target_num,
            "Breadth_First": self._breadth_first
        }

        with open(f"{BackupPath}/config.txt", 'w', encoding='utf-8') as file:
            json.dump(config_dict, file)
        logger.debug("本次任务的配置已保存")

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

    def handle_task(self):
        """
        具体的拿到链接后的处理方式
        """
        if not self._isworking:
            logger.debug("任务暂停，停止任务！")
            return

        id = self._GetId()

        while True:
            with self._lock:
                if self._id >= self._target_num : return

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
            sleep(1)

    def Work(self, start_urls, target_num, debug=False):
        self._target_num = target_num
        self._url_allocator.put(start_urls)
        logger.info(f"本次任务开始将在 3s 后开始, 将展示任务信息...")
        crawl_method = "广度优先" if self._breadth_first else "深度优先"
        logger.info(f"爬取的方式为 {crawl_method}, 使用了 {self._num_threads} 个线程, 目标爬取网页数目为 {self._target_num }")
        sleep(3)

        # 调试模式
        if debug:
            self.handle_task()
        else:
            # 这是一个包装函数，用于作为线程的目标
            def task_wrapper():
                self.handle_task()

            for _ in range(self._num_threads):
                thread = threading.Thread(target=task_wrapper)
                self._threads.append(thread)
                thread.start()
            logger.debug("所有线程已经开始执行任务")

            for t in self._threads:
                t.join()
            logger.debug("所有线程已经退出")
