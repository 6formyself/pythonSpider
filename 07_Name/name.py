import requests
from bs4 import BeautifulSoup as Bs4
import xlrd
import xlutils.copy
import xlwt
import os
from time import sleep
cookie_file = open('cookie.txt')
header = {
    # ':authority': 'www.ancestry.com',
    # ':method': 'GET',
    # ':path': '/search/collections/7488/?name=_Kim&count=50&fh=50&fsk=MDs0OTs1MA-61--61-,
    # ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': cookie_file.readlines()[0][0:-1],
    'if-none-match': 'W/"3d2c0-hFfkZBY3d6s/adMdu4vZZR60T9w"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59'
}
cookie_file.close()
head_url = 'https://www.ancestry.com/search/collections/7488/?name={}&count=50'


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def create_excel_file(name):
    f = xlwt.Workbook()
    m_sheet = f.add_sheet('sheet1', cell_overwrite_ok=True)
    row = ['Name', 'Arrival Date', 'Birth Year', 'Port of Departure', 'Ethnicity/ Nationality', 'Ship Name']
    for i in range(0, len(row)):
        m_sheet.write(0, i, row[i], set_style('Times New Roman', 220, True))
    f.save('./file/' + name + '.xlsx')


def get_struct_data(url):
    res = requests.get(url, headers=header)
    soup = Bs4(res.text, 'lxml')
    if len(soup('body')[0].select('iframe')) == 1:
        print('可能出现了验证码,验证完毕请输入1并回车：')
        input()
    trs = soup('tr', attrs={'class': 'record'})
    data_list = []
    for item in trs:
        tds = item.select('td')
        name = tds[1].text
        arrival_date = tds[2].text
        birth_year = tds[3].text
        port_of_departure = tds[4].text
        ethnicity_nationality = tds[5].text
        ship_name = tds[6].text
        line_data = [name, arrival_date, birth_year, port_of_departure, ethnicity_nationality, ship_name]
        print(line_data)
        data_list.append(line_data)
    return data_list


if __name__ == '__main__':
    # 读取姓名数据
    name_file = open('name.txt')
    names = name_file.readlines()

    for name in names:
        if not os.path.exists('./file/' + name[0:-1] + '.xlsx'):
            # 创建excel文件
            create_excel_file(name[0:-1])
        # 读取excel
        read_book = xlrd.open_workbook(r'file/' + name[0:-1] + '.xlsx')
        nrows = read_book.sheets()[0].nrows
        work_book = xlutils.copy.copy(read_book)
        sheet = work_book.get_sheet(0)

        url = head_url.format('_' + name[0:-1])
        # 获取数据量
        print(url)
        res = requests.get(url, headers=header)
        page_soup = Bs4(res.text, 'lxml')
        # 判断是否需要验证
        main_iframe = page_soup('iframe', id='main-iframe')
        if len(main_iframe) != 0 and main_iframe[0].text.find('Request unsuccessful. Incapsula incident') != -1:
            print(res.text)
            sleep(3)
            res = requests.get(url, headers=header)
            print(res.text)
            page_soup = Bs4(res.text, 'lxml')
            # 判断是否需要验证
            main_iframe = page_soup('iframe', id='main-iframe')
            if len(main_iframe) != 0 and main_iframe[0].text.find('Request unsuccessful. Incapsula incident') != -1:
                print('网站需要人工验证，请前往验证(cookie过期或者需要人工验证)，验证完请输入1并回车：')
                input()
                res = requests.get(url, headers=header)
                page_soup = Bs4(res.text, 'lxml')
        page = list(page_soup('h3', attrs={'class': 'topSpacing w30'})[0].stripped_strings)[0].split('of')[1].strip()
        page_str = ''
        for char in page:
            try:
                num = int(char)
            except Exception:
                continue
            page_str += str(num)
        page_num = int(page_str)
        page_num = page_num + 50 - (page_num % 50)
        if page_num > 4950:
            url_file = open('url.txt', 'a')
            for i in range(4950, page_num, 50):
                url_file.write(url + '&fh=' + str(i) + '&fsk=MDs5OTs1MA-61--61-\n')
            url_file.close()
            page_num = 4950
        print(page_num)
        for i in range(nrows - 1, page_num, 50):
            if i == 0:
                data = get_struct_data(url)
            else:
                print(url + '&fh=' + str(i) + '&fsk=MDs5OTs1MA-61--61-')
                data = get_struct_data(url + '&fh=' + str(i) + '&fsk=MDs5OTs1MA-61--61-')
            if len(data) <= 0:
                print('网页出现问题，请前往核实，核实完毕请输入1并回车：')
                input()
                continue
            for item in data:
                sheet.write(nrows, 0, item[0])
                sheet.write(nrows, 1, item[1])
                sheet.write(nrows, 2, item[2])
                sheet.write(nrows, 3, item[3])
                sheet.write(nrows, 4, item[4])
                sheet.write(nrows, 5, item[5])
                nrows += 1
            work_book.save(r'file/' + name[0:-1] + '.xlsx')



