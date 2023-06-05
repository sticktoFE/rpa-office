import threading
import queue
import time


class BaseProducer(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def produce(self):
        # 用户需要覆盖这个方法以满足特定的需求
        raise NotImplementedError

    def run(self):
        while True:
            if self.q.qsize() < 10:  # 限制队列大小
                self.produce()
            else:
                time.sleep(1)  # 队列满了就暂停1秒


class BaseConsumer(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q

    def consume(self, data):
        # 用户需要覆盖这个方法以满足特定的需求
        raise NotImplementedError

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.consume(data)
            else:
                time.sleep(1)  # 数据不足就暂停1秒


class MyProducer(BaseProducer):
    def produce(self):
        for i in range(5):  # 每次产生5个数据
            msg = "数据" + str(i)
            self.q.put(msg)
            print("生产者产生数据: %s" % msg)
        time.sleep(1)  # 每秒产生数据


class MyConsumer(BaseConsumer):
    def consume(self, data):
        print("消费者处理数据: %s" % data)
        time.sleep(1)  # 模拟处理数据所需的时间
