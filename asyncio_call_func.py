import asyncio


def callback(times):
    print("sleep {}".format(times))

def stoploop(loop):
    loop.stop()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_soon(callback,2)               # 在下一个轮询时执行此操作

    loop.call_later(2, callback, 2)          # 在指定时间之后执行此操作
    loop.call_later(1, callback, 1)          # 在指定时间之后执行此操作
    loop.call_later(3, callback, 3)          # 在指定时间之后执行此操作
    loop.call_soon(callback,4)               # call_soon 比call_later优先级高
    # loop.call_soon(stoploop,loop)
    now = loop.time()
    loop.call_at(now + 2, callback, 2)             #call_at 添加指定时间，必须是loop提供的内部时钟时间
    loop.call_at(now + 1, callback, 1)
    loop.call_at(now + 3, callback, 3)
    loop.run_forever()