import requests
from bs4 import BeautifulSoup as Bs4
from selenium import webdriver

head = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
head_url = 'https://www.lawtime.cn/dongchengqu/lawfirm/'


if __name__ == '__main__':
    driver = webdriver.Chrome()
    file = open('dongcheng.txt', 'a')
    # 79
    for i in range(1, 23):
        driver.get(head_url + 'p' + str(i) + '?order=1')
        soup = Bs4(driver.page_source, 'lxml')
        lay_info_div_con = soup('div', attrs={'class': 'law-info'})
        for lay_info_div in lay_info_div_con:
            lay_name = lay_info_div.select('a')[0].text
            lay_phone = lay_info_div.select('a')[1].text
            people = lay_info_div.select('span')[0].text
            if 10 <= int(people) <= 50:
                file.write(lay_name + ' ' + lay_phone + ' ' + people + '人\n')
            print(lay_name, lay_phone, people)
    file.close()
