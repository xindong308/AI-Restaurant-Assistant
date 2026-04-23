import time

if __name__ == '__main__':
    # 获取当前的时间格式为 yyyy-mm-dd hh:mm:ss
    str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(type(str), str)
