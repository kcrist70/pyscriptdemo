#使用多线程，在协程中集成阻塞IO

from concurrent.futures import ThreadPoolExecutor
import asyncio
import socket
from urllib.parse import urlparse


def get_url(url):
    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,80))
    client.send("GET {} HTTP/1.1\r\nHost: {}\r\nConnection:close\r\n\r\n".format(path,host).encode('utf8'))
    data = bytes()
    while True:
        d = client.recv(1024)
        if d:
            data += d
        else:
            break
    data = data.decode('utf8')
    html_data = data.split('\r\n\r\n')[1]
    print(html_data)
    client.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor()
    tasks = list()
    import time
    start_time = time.time()
    for url in range(1,50):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(url)

        task = loop.run_in_executor(executor, get_url, url)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time() - start_time)