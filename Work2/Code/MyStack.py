import threading

"""
实现一个线程安全的队列
"""
class Stack:
    def __init__(self):
        self.__stack = []
        self.__size = 0
        self.__lock = threading.Lock()

    def put(self, val):
        with self.__lock:
            self.__stack.append(val)
            self.__size += 1

    def get(self):
        with self.__lock:
            if not self.__stack:
                raise IndexError("pop from empty stack")
            return self.__stack.pop()

    def empty(self):
        with self.__lock:
            return self.__size == 0

