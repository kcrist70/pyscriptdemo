#asyncio 没有提供http协议的接口， aiohttp 基于asyncio包装的第三方模块，异步requests

import asyncio
import socket
from urllib.parse import urlparse


async def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'

    # client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # client.connect((host,80))

    reader, writer = await asyncio.open_connection(host, 80)

    writer.write("GET {} HTTP/1.1\r\nHost: {}\r\nConnection:close\r\n\r\n".format(path,host).encode('utf8'))
    all_lines = []
    async for row_line in reader:
        data = row_line.decode('utf8')
        all_lines.append(data)
    html = '\n'.join(all_lines)
    return html


async def main(loop):
    tasks = []
    for url in range(1,50):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
        tasks.append(asyncio.ensure_future(get_url(url)))
    for task in asyncio.as_completed(tasks):
        result = await task    # 返回结果是一个协程，需要await
        #执行完成一个就打印一个
        print(result)

if __name__ == '__main__':
    import time
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    print(time.time() - start_time)

# if __name__ == '__main__':
#     import time
#     start_time = time.time()
#     loop = asyncio.get_event_loop()
#     tasks = []
#     for url in range(1,50):
#         url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
#         tasks.append(get_url(url))
#     loop.run_until_complete(asyncio.wait(tasks))
#     print(time.time() - start_time)

# if __name__ == '__main__':
#     import time
#     start_time = time.time()
#     loop = asyncio.get_event_loop()
#     tasks = []
#     for url in range(1,50):
#         url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
#         tasks.append(asyncio.ensure_future(get_url(url)))
#     loop.run_until_complete(asyncio.wait(tasks))
#   执行完成后全部打印
#     for task in tasks:
#         print(task.result())
#     print(time.time() - start_time)