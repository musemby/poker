import time


def count_down(num):
    for num in reversed(range(num)):
        print(num, end='\r')
        time.sleep(0.5)