import requests
from bs4 import BeautifulSoup as Bs4
from selenium import webdriver
from time import sleep

head_url = 'https://www.fzpaopao.com/admin.html#/pt/user/index.html?spm=m-62-63-81&limit=200&page=2'


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.fzpaopao.com/admin.html#/pt/user/index.html?spm=m-62-63-81&limit=200&page=1')
    input('输入1')
    for i in range(1, 2):
        driver.get('https://www.fzpaopao.com/admin.html#/pt/user/index.html?spm=m-62-63-81&limit=200&page='+str(i))
        # driver.switch_to.window(driver.window_handles[1])
        sleep(2)
        soup = Bs4(driver.page_source, 'lxml')
        trs = soup('table')[0].select('tbody')[0].select('tr')
        with open('user2.txt', 'a') as f:
            for tr in trs:
                try:
                    data = list(tr.stripped_strings)
                    if len(data) < 4:
                        continue
                    f.write(data[2])
                except Exception as e:
                    print(e)
    # fzpaopao
    # print(driver.title)
