import json
import jieba
import signal
import sys
from MyLogging import logger
from Scheduler import MultiThreadCrawler


def signal_handler(signal, frame):
    logger.debug("任务中断，正在结束正在执行的任务以及任务数据备份...")
    crawlers.stop()
    crawlers.back_up()
    logger.info("数据备份完成，bye...")

    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    crawlers = MultiThreadCrawler(8, True)
    crawlers.Work("https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%8E%86%E5%8F%B2/152769?fr=ge_ala",
                  11000,
                  5,
                  debug=True)

    logger.info("本次任务执行完成！")