import requests
from bs4 import BeautifulSoup as Bs4
from Tool.excel import excel_write

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
head_url = 'https://www.cofeed.com'
row = 0


def get_li_a_link():
    html = requests.get(head_url, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    ul_con = soup.select('ul')
    a_list = []
    for ul in ul_con:
        if not ul.get('class'):
            continue
        if ul.get('class')[0] == 'menu_ul_left' or ul.get('class')[0] == 'menu_ul_right':
            a_s = ul.select('a')
            for a in a_s:
                a_list.append(a.get('href'))
    return a_list


def get_other_page(sheet, page_url):
    my_file = open('data.txt', 'a');
    html = requests.get(page_url, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    # 拿到所有div
    my_div_list = soup.select('div')
    for div in my_div_list:
        if div.get('class') and div.get('class')[0] == 'side_con_left':
            title = div.select('a')[0].get('title')
            href = head_url + div.select('a')[0].get('href')
            data = [title, href]
            global row
            row = row + 1
            excel_write.write_excel(sheet, row, data)
            my_file.write(str(data) + '\n')
    my_file.close()


if __name__ == '__main__':
    # links_file = open('links2.txt', 'a')
    # item_list = get_li_a_link()
    # sheet, file = excel_write.get_sheet('需求2')
    # for item in item_list:
    #     tar_url = head_url + item
    #     html = requests.get(tar_url, headers=head)
    #     html.encoding = 'utf-8'
    #     soup = Bs4(html.text, 'lxml')
    #     # 拿到所有div
    #     my_div_list = soup.select('div')
    #     pages = 0
    #     # 拿到页数
    #     for div in my_div_list:
    #         if div.get('id') and div.get('id') == 'page':
    #             page_a = div.select('a')
    #             temp_href = page_a[len(page_a) - 1].get('href')
    #             print('pages:' + temp_href[6:temp_href.find('.')])
    #             try:
    #                 pages = int(temp_href[6:temp_href.find('.')])
    #             except Exception:
    #                 pass
    #     # 写入数据
    #     try:
    #         # get_other_page(sheet, head_url + item)  # 主页
    #         links_file.write(head_url + item + '\n')
    #         for index in range(2, pages):
    #             # get_other_page(sheet, head_url + item + 'index_' + str(index) + '.html')
    #             links_file.write(head_url + item + 'index_' + str(index) + '.html\n')
    #     except Exception:
    #         pass
    #         # excel_write.save_file(file, '需求2')
    #     # excel_write.save_file(file, '需求2')
    my_file = open('needLink.txt')
    lines = my_file.readlines()
    sheet, file = excel_write.get_sheet('需求2')
    for index in range(0, len(lines)):
        try:
            print(index)
            # if index != 0 and index % 40 == 0:
            get_other_page(sheet, lines[index][0:-1])
        except Exception:
            excel_write.save_file(file, '需求2')
    print('---------------------')
    excel_write.save_file(file, '需求2')

