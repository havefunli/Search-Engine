from MTCrawler import MultiThreadCrawler
import signal
import sys

def signal_handler(signal, frame):
    print('You received a SIGTERM. Exiting gracefully.')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    crawlers = MultiThreadCrawler(8, True)
    crawlers.Work("https://baike.baidu.com/item/%E4%B8%AD%E5%9B%BD%E5%8E%86%E5%8F%B2/152769?fr=ge_ala", 1)





