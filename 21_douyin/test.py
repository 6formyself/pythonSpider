from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import csv

# huashu_file = open('huashu.txt')
# huashu_lines = huashu_file.readlines()
# huashu = ''.join(huashu_lines)
# print('加载到话术：')
# print(huashu)
#
# with open("daren-" + time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time())) + ".csv", 'a', newline='', encoding='utf-8-sig') as csv_f:
#     csv_write = csv.writer(csv_f)
#     csv_write.writerow(['序号', '达人信息'])

# # 启动浏览器
# driver = webdriver.Chrome(executable_path='chromedriver.exe')
# driver.get('https://www.cnblogs.com/shengs/p/11203221.html')
# sleep(3)
# input('11111')
#
# # print(driver.window_handles)
# while True:
#     i = int(input('序号'))
#     a = driver.find_elements_by_class_name('catListTitle')[i]
#     driver.execute_script("arguments[0].scrollIntoView(false);", a)

# multiprocessing.py
import os
import multiprocessing

print('Process (%s) start...' % os.getpid())
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
