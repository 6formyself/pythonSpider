import requests
from bs4 import BeautifulSoup as Bs4
import os

head = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
head_url = 'https://uiiiuiii.com/inspirations/banner'


def download_image(url):
    try:
        urls = 'https:' + url
        ir = requests.get(urls, headers=head)
        if ir.status_code == 200:
            save_image(ir.content)
        return None
    except requests.RequestException:
        return None


def save_image(url):
    d = './images/'
    path = d + url.split('/')[-1]
    if not url.split('/')[-1].startswith('i'):
        return
    try:
        if not os.path.exists(d):
            os.mkdir(d)
        if not os.path.exists(path):
            r = requests.get(url)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("图片保存成功")
        else:
            print("图片已存在")
    except:
        print("图片获取失败")


def get_banner_page_link():
    file = open('banner_link.txt', 'a')
    for i in range(1, 82):
        html = requests.get(head_url + '/page/' + str(i), headers=head)
        html.encoding = 'utf-8'
        soup = Bs4(html.text, 'lxml')
        a_list = soup('a', attrs={'class': 'item-href'})
        for a in a_list:
            print(a.get('href'))
            file.write(a.get('href') + '\n')


if __name__ == '__main__':
    banner = open('banner.txt', 'a')
    banner_file = open('banner_link.txt')
    link_con = banner_file.readlines()
    for link in link_con:
        html = requests.get(link[0:-1], headers=head)
        html.encoding = 'utf-8'
        soup = Bs4(html.text, 'lxml')
        div = soup('div', attrs={'class': 'inspiration-images'})[0]
        image_links = div.select('img')
        for image_link in image_links:
            print(image_link.get('src'))
            save_image(image_link.get('src'))

