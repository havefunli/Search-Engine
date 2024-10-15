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
        self._debug = False;
        self._id = 0
        self._sleep_time = 0
        self._isworking = True
        self._num_threads = num_threads
        self._breadth_first = breadth_first
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
        """
        数据备份模块
        TODO
        """
        unprocessed_urls = []
        while not self._url_allocator.empty():
            unprocessed_urls.append(self._url_allocator.get())

        with open(f"{BackupPath}/unprocessed.txt", 'w', encoding='utf-8') as file:
            json.dump(unprocessed_urls, file)
        logger.debug("未处理的链接已保存")

        with open(f"{BackupPath}/processed.txt", 'w', encoding='utf-8') as file:
            json.dump(self._visited, file)
        logger.debug("已处理的链接已保存")

        config_dict = {
            "ID": self._id,
            "Debug": self._debug,
            "Sleep_Time": self._sleep_time,
            "Target_Num": self._target_num,
            "Threads_Num": self._num_threads,
            "Breadth_First": self._breadth_first
        }

        with open(f"{BackupPath}/config.txt", 'w', encoding='utf-8') as file:
            json.dump(config_dict, file)
        logger.debug("本次任务的配置已保存")

    def _GetId(self):
        """
        为每一个爬取任务分配 id
        对共享变量的操作上锁
        """
        with self._lock:
            self._id += 1
        logger.debug(f"此次任务分配的 id 是 {self._id}")
        return self._id

    def _GetValidUrls(self, item: MyItem):
        """
        将没有处理过的 urls 放入 urls 分配器
        """
        for url in item.IncludedUrl:
            if url not in self._visited:
                self._url_allocator.put(url)
        logger.debug(f"URL分配器最新的链接数目为 {self._url_allocator.qsize()}")

    def _ToSave(self, item: MyItem):
        """
        对获取的完整的数据进行保存
        """
        json_str = item.toJson()
        with open(f"{SrcPath}/web_{item.Id}.txt", 'w', encoding='utf-8') as file:
            file.write(json_str)
        logger.info(f"{self._id} 号任务数据保存完毕，任务成功结束")

    def _GetItem(self, id, url):
        """
        创建一个 ITEM 对象来存储需要的数据
        """
        item = MyItem()
        item.Id = id
        item.Url = url

        return item

    def handle_task(self):
        """
        具体的链接的处理方式
        """
        if not self._isworking:
            logger.debug("任务暂停！")
            return

        while True:
            id = self._GetId()

            with self._lock:
                if self._id >= self._target_num: return

            with self._cond:
                while self._url_allocator.empty():
                    self._cond.wait()
                    logger.info(f"{id} 号任务暂停，URL分配器中的 url 为空")

            url = self._url_allocator.get()
            self._visited.append(url)

            item = self._GetItem(id, url)
            spider = Crawler(url)
            spider.Work(item)

            # 若数据是无效的，直接跳过处理
            if not item.isvalid: continue

            self._GetValidUrls(item)
            with self._cond:
                self._cond.notify_all()

            self._ToSave(item)
            sleep(self._sleep_time)

    def _Init_Config(self, target_num, sleep_time, debug):
        self._debug = debug
        self._sleep_time = sleep_time
        self._target_num = target_num

    def Work(self, start_urls, target_num, sleep_time=0, debug=False):
        self._Init_Config(target_num, sleep_time, debug)

        self._url_allocator.put(start_urls)

        logger.info(f"本次任务开始将在 2s 后开始, 将展示任务信息...")
        crawl_method = "广度优先" if self._breadth_first else "深度优先"
        logger.info(
            f"爬取的方式为 {crawl_method}, "
            f"使用了 {self._num_threads} 个线程, "
            f"目标爬取网页数目为 {self._target_num}")
        sleep(2)

        # 调试模式
        if self._debug:
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

    def ReWork(self):
        logger.info("开始还原数据...")
        with open(f"{BackupPath}/config.txt", 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            logger.info("成功读取配置文件")

        with open(f"{BackupPath}/unprocessed.txt", 'r', encoding='utf-8') as file:
            unprocessed_urls = json.load(file)
        for url in unprocessed_urls[1:]:
            self._url_allocator.put(url)
        logger.info("成功读取未处理的链接")

        with open(f"{BackupPath}/processed.txt", 'r', encoding='utf-8') as file:
            processed_urls = json.load(file)
        for url in processed_urls:
            self._visited.append(url)
        logger.info("成功读取处理的链接")

        self._id = config_data["ID"]
        self._num_threads = config_data["Threads_Num"]
        self._breadth_first = config_data["Breadth_First"]

        logger.info("数据还原成功，开始工作")

        self.Work(unprocessed_urls[0],
                  config_data["Target_Num"],
                  config_data["Sleep_Time"],
                  config_data["Debug"])
