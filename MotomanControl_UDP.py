import threading
import time

def print_numbers():
    for i in range(5):
        time.sleep(1)  # 模拟一些工作
        print(f"Thread 1: {i}")

def print_letters():
    for char in 'ABCDE':
        time.sleep(1)
        print(f"Thread 2: {char}")

# 创建两个线程
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# 启动线程
thread1.start()
thread2.start()

# 等待两个线程完成
thread1.join()
thread2.join()
