# import asyncio
#
# async def get_html(url):
#     print("start get url")
#     await asyncio.sleep(2)
#     print("end get url")
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     task = [get_html('http://www.baidu.com') for i in range(10)]
#     loop.run_until_complete(asyncio.wait(task))
#


#--------------------

# import asyncio
# from functools import partial  # 将一个函数包装成另一个函数
#
# async def get_html(url):
#     print("start get url")
#     await asyncio.sleep(2)
#     return 'finished'
#
# def callback(url, future):     # 自定义参数必须放在前面，最后接收callback的future
#     print("callback： ", url, future)
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     # get_future = asyncio.ensure_future(get_html('http://www.baidu.com'))   # loop.create_task() 效果相等
#     get_future = loop.create_task(get_html('http://www.baidu.com'))   # asyncio.ensure_future() 效果相等,task是future的子类
#     get_future.add_done_callback(partial(callback,"http://www.baidu.com"))      #callback 需要接收future类为参数
#     loop.run_until_complete(get_future)
#     print(get_future.result())
#

# --------------------------

import asyncio

async def get_html(url):
    print("start get url")
    await asyncio.sleep(2)
    print("end get url")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = [get_html('http://www.baidu.com') for i in range(10)]
    loop.run_until_complete(asyncio.gather(*task))



"""gather 和 wait 的区别
gather 更加 high-level
gather 可以将任务分组
    group1 = [get_html('http://www.baidu.com') for i in range(10)]
    group2 = [get_html('http://xxx.com') for i in range(10)]
    loop.run_until_complete(asyncio.gather(*group1, *group2))
或者这种形式：
    group1 = [get_html('http://www.baidu.com') for i in range(10)]
    group2 = [get_html('http://xxx.com') for i in range(10)]
    group1 = asyncio.gather(*group1)
    group2 = asyncio.gather(*group2)
    loop.run_until_complete(asyncio.gather(group1, group2))
还可以分组取消任务：
    group1 = [get_html('http://www.baidu.com') for i in range(10)]
    group2 = [get_html('http://xxx.com') for i in range(10)]
    group1 = asyncio.gather(*group1)
    group2 = asyncio.gather(*group2)
    group2.cancel()
    loop.run_until_complete(asyncio.gather(group1, group2))

"""
