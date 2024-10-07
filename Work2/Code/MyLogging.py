import logging


class MyLogger:
    def __init__(self, format="[%(asctime)s][%(levelname)s][%(funcName)s][%(message)s]"):
        self._mylogger = logging.Logger("Crawler_Logger")
        self._format = format

    def GetLogger(self):
        my_handler = logging.StreamHandler()
        my_handler.setLevel(logging.DEBUG)
        my_handler.setFormatter(logging.Formatter(self._format))
        self._mylogger.addHandler(my_handler)

        return self._mylogger


logger = MyLogger().GetLogger()
