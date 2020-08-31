from selenium import webdriver
from bs4 import BeautifulSoup as Bs4

head_url = 'http://www.mafengwo.cn'
driver = webdriver.Chrome()
# 读取游记列表
link_file = open('links.txt')
links = link_file.readlines()
link_file.close()

# 写入游记链接
you_ji_file = open('youji.txt', 'a')

for link in links:
    print(link[0:-1])
    driver.get(link[0:-1])
    soup = Bs4(driver.page_source, 'lxml')
    you_ji_list = soup('div', attrs={'class': 'post-list'})[0].select('ul')[0].select('li')
    for you_ji in you_ji_list:
        a_tag = you_ji.select('h2')[0].select('a')
        href = ''
        if len(a_tag) == 3:
            href = a_tag[2].get('href')
        if len(a_tag) == 2:
            href = a_tag[1].get('href')
        if len(a_tag) == 1:
            href = a_tag[0].get('href')
        if not href.endswith('\n'):
            href += '\n'
        print(head_url + href)
        you_ji_file.write(href)
