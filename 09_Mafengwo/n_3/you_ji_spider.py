import requests
from bs4 import BeautifulSoup as Bs4
from time import sleep
import xlrd
import xlutils.copy
import os

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'MKT_CKID=1597915145961.lqtvw.nvk1; MKT_Pagesource=PC; _ga=GA1.2.1770546521.1597915147; _RSG=dFa6GfKjmhA.Bjhp.A_k69; _RDG=28c5b0009fa4df29c201d21c18aa491cd9; _RGUID=aaf0b54a-501a-43e7-91ae-fcafb3aed2fe; ASP.NET_SessionSvc=MTAuNjAuNDkuNzh8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTU4OTAwMzM0Njc4NQ; _gid=GA1.2.1412778062.1598501044; MKT_CKID_LMT=1598501043668; _RF1=121.204.59.188; appFloatCnt=10; _bfa=1.1597915145512.2ro1ej.1.1597930006703.1598501043080.4.12; _bfs=1.3; _gat=1; _jzqco=%7C%7C%7C%7C1598501043936%7C1.493391043.1597915145958.1598501159196.1598501320997.1598501159196.1598501320997.undefined.0.0.11.11; __zpspc=9.4.1598501043.1598501321.3%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D0%26p2%3D290570%26v1%3D12%26v2%3D11',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'referer': 'https://you.ctrip.com/travels/Xiamen21/t2-p30.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
head_url = 'https://you.ctrip.com'


def get_you_ji_links(url):
    """返回每页的游记链接集合"""
    print(url)
    res = requests.get(url, headers=headers)
    soup = Bs4(res.text, 'lxml')
    you_ji_links = soup('a', attrs={'class': 'journal-item cf'})
    youji_link_list = []
    for you_ji_link in you_ji_links:
        href = you_ji_link.get('href')
        youji_link_list.append(href)
    return youji_link_list


def get_struct_data(url):
    """获取游记正文信息"""
    res = requests.get(url, headers=headers)
    soup = Bs4(res.text, 'lxml')
    # 用户名称
    user_name = soup('a', id='authorDisplayName')[0].text.strip()
    # 游记标题
    youji_title = soup('h1')[0].text.strip()
    # 游记发布时间
    public_time = soup('div', attrs={'class': 'ctd_head_con cf'})[0].select('div')[0].text.strip()[3:]
    # 天数，时间，人均，和谁，玩法，路线
    days = times = ave = with_who = play = '-'
    line = ''
    con = soup('div', attrs={'class': 'bottom'})[0]
    spans = con.select('span')
    for span in spans:
        text = span.text.strip()
        print(span.text.strip())
        if text.find('天数') != -1:
            days = text[3:]
        elif text.find('时间') != -1:
            times = text[3:]
        elif text.find('人均') != -1:
            ave = text[3:]
        elif text.find('和谁') != -1:
            with_who = text[3:]
        elif text.find('玩法') != -1:
            play = text[3:]

    a_s = soup('a', attrs={'class': 'gs_a_poi locale hotspot_tag sight'})
    for a in a_s:
        line += a.text.strip() + '->'
    # 游记正文
    content_div = soup('div', attrs={'class': 'ctd_content'})[0]
    content = content_div.text
    print(user_name, youji_title, public_time, line)
    return [user_name, youji_title, public_time, days, times, ave, with_who, play, line, content]


def save_image(youji_title, url, index):
    d = './images/' + youji_title + '/'
    path = d + str(index) + '.jpg'
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
    except Exception as e:
        print(e)
        print("图片获取失败")


if __name__ == '__main__':
    r_book = xlrd.open_workbook(r'游记.xlsx')
    rows = r_book.sheets()[0].nrows
    w_book = xlutils.copy.copy(r_book)
    sheet = w_book.get_sheet(0)
    aa = 'https://you.ctrip.com/travels/Xiamen21/t2-p{}.html'
    for i in range(1, 501):
        print('第' + str(i) + '页：')
        you_ji_link_list = get_you_ji_links(aa.format(i))
        for you_ji_link in you_ji_link_list:
            print(you_ji_link)
            try:
                data = get_struct_data(head_url + you_ji_link)
            except Exception:
                continue
            for x in range(0, 10):
                if x == 9:
                    if len(data[x]) >= 32760:
                        sheet.write(rows, x, data[x][0:32760])
                    else:
                        sheet.write(rows, x, data[x])
                else:
                    sheet.write(rows, x, data[x])
            # for y in range(0, len(data[10])):
            #     save_image(data[1], data[10][y], y)
            rows += 1
            w_book.save(r'游记.xlsx')
            sleep(1)


