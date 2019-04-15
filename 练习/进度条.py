"""
进度条
"""
import sys,time

def view_bar(num):
    rate = num / 100
    rate_num = int(rate * 100)
    if rate_num < 100:
        r = '\r%s%d%%' %("="*int(num/2),rate_num)
        sys.stdout.write(r)
        sys.stdout.flush()
    else:
        r = '\r%s' % ("=" * int(num / 2))
        sys.stdout.write(r)

if __name__ == '__main__':
    for i in range(101):
        time.sleep(0.1)
        view_bar(i)