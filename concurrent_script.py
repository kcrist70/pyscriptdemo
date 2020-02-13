from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait, Future


def func(arg):
    print('...')
    return arg


executor = ThreadPoolExecutor(max_workers=2)
urls = [1, 2, 3, 4]
all_task = [executor.submit(func, url) for url in urls]
for future in as_completed(all_task):
    print(future.result())
# wait(all_task)  阻塞主线程，等待相应子进程完成
# Future   task的返回容器
