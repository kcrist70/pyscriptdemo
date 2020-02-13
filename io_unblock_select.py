from urllib.parse import urlparse
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
urls=[]
stop = False

class Fetcher:
    """
    非阻塞模式
    I/O复用
    函数回调
    高并发
    """
    def connected(self ,key):
        selector.unregister(key.fd)
        self.client.send \
            ("GET {} HTTP/1.1\r\nHost: {}\r\nConnection:close\r\n\r\n".format(self.path ,self.host).encode('utf8'))
        selector.register(self.client.fileno(), EVENT_READ, self.readable)

    def readable(self ,key):
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            selector.unregister(key.fd)
            data = self.data.decode("utf8")
            html_data = data.split('\r\n\r\n')[1]
            print(html_data)
            self.client.close()
            urls.remove(self.spider_url)
            if not urls:
                global stop
                stop = True

    def get_url(self, url):
        self.spider_url = url
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        self.data = bytes()
        if self.path == '':
            self.path = '/'

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)
        try:
            self.client.connect((self.host, 80))
        except BlockingIOError as e:
            pass

        selector.register(self.client.fileno(), EVENT_WRITE ,self.connected)


def loop():
    while not stop:
        ready = selector.select()
        for key ,mask in ready:
            call_back = key.data
            call_back(key)


if __name__ == '__main__':
    import time
    start_time = time.time()
    for url in range(1, 21):
        url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
        urls.append(url)
        fetcher = Fetcher()
        fetcher.get_url(url)
    loop()
    print(time.time() - start_time)