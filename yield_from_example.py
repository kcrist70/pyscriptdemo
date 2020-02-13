final_result = {}


def sales_sum(pro_name):
    total = 0
    nums = []
    while True:
        x = yield
        print(pro_name + '销量: ', x)
        if not x:
            break
        total += x
        nums.append(x)
    return total, nums


def middle(key):
    while True:
        final_result[key] = yield from sales_sum(key)
        print(key + "销量统计完成！！.")


def main():
    data_sets = {
        "面膜": [1200, 1500, 3000],
        "手机": [28, 55, 98, 108],
        "大衣": [280, 560, 778, 70]

    }
    for key, data_set in data_sets.items():
        print("start key: ", key)
        m = middle(key)
        m.send(None)
        for value in data_set:
            m.send(value)
        m.send(None)
    print('final_result: ', final_result)


if __name__ == '__main__':
    main()

"""
总结：
1. 子生成器生产的值，都是直接传给调用方的；调用方通过.send()发送的值都是直接传递给子生成器的；
    如果发送的是None,会调用子生成器的__next__()方法，如果不是None，会调用子生成器的.send()方法；
2. 子生成器退出的时候，最后的return EXPR, 会触发一个StopIteration(EXPR)异常；
3. yield from 表达式的值，是子生成器终止时，传递给StopIteration异常的第一个参数；
4. 如果调用的时候出现StopIteration异常，委托生成器会恢复运行，同时其他的异常会向上‘冒泡’；
5. 传入委托生成器的异常里，除了GeneratorExit 之外，其他的所有异常全部传递给子生成器的.throw()方法；
    如果调用.throw()的时候出现了StopIteration异常，那么就恢复委托生成器的运行，其他的异常全部向上“冒泡”；
6. 如果在委托生成器上调用.close()或传入GeneratorExit异常，会调用子生成器的.close()方法，没有的话不调用。
    如果在调用.close()的时候抛出了异常，那么就向上‘冒泡’，否则的话委托生成器会抛出GeneratorExit异常。
"""

"""
def fun():
    while True:
        my_list = yield from fun1()
        print(my_list)

def fun1():
    n = list()
    while True:
        x = yield

        if not x:
            break
        print('销量: ', x)
        n.append(x)
    return n

def main():
    func = fun()
    func.send(None)
    for i in range(1,20):
        func.send(i)
    func.send(None)
main()
"""