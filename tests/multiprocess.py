from multiprocessing import Process, JoinableQueue
import time


# 消费者方法
def consumer(q, name):
    while True:
        res = q.get()
        if res is None:
            print(1111)
            break
        print("%s 吃了 %s" % (name, res))
        q.task_done()  # 发送信号给q.join(),表示已经从队列中取走一个值并处理完毕了


# 生产者方法
def producer(q, name, food):
    for i in range(3):
        time.sleep(1)  # 模拟生产西瓜的时间延迟
        res = "%s %s" % (food, i)
        print("%s 生产了 %s" % (name, res))
        # 把生产的vegetable放入到队列中
        q.put(res)
    q.join()  # 等消费者把自己放入队列的所有元素取完之后才结束


if __name__ == "__main__":
    # q = Queue()
    q = JoinableQueue()
    # 创建生产者
    p1 = Process(target=producer, args=(q, "kelly", "西瓜"))
    p2 = Process(target=producer, args=(q, "kelly2", "蓝莓"))
    # 创建消费者
    c1 = Process(
        target=consumer,
        args=(
            q,
            "peter",
        ),
    )
    c2 = Process(
        target=consumer,
        args=(
            q,
            "peter2",
        ),
    )
    c3 = Process(
        target=consumer,
        args=(
            q,
            "peter3",
        ),
    )

    c1.daemon = True
    c2.daemon = True
    c3.daemon = True

    p_l = [p1, p2, c1, c2, c3]
    for p in p_l:
        p.start()

    p1.join()
    p2.join()
    # 1.主进程等待p1,p2进程结束才继续执行
    # 2.由于q.join()的存在,生产者只有等队列中的元素被消费完才会结束
    # 3.生产者结束了,就代表消费者已经消费完了,也可以结束了,所以可以把消费者设置为守护进程(随着主进程的退出而退出)

    print("主进程")
