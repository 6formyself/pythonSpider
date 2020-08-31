import requests
from bs4 import BeautifulSoup as Bs4
from Tool.excel import excel_write

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}


def get_item(url):
    data_con = []
    html = requests.get(url, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    ul_list = soup.select('ul')
    for ul in ul_list:
        ul_id = ul.get('id')
        if ul_id and ul_id == 'list':
            a_list = ul.select('a')
            for a_item in a_list:
                href = a_item.get('href')
                title = list(a_item.select('h2')[0].stripped_strings)[0]
                data_con.append([title, href])
    return data_con


if __name__ == '__main__':
    my_file = open('link.txt')
    lines = my_file.readlines()
    sheet, file = excel_write.get_sheet('玉米需求3')
    row_count = 0
    for index in range(0, len(lines)):
        try:
            print('第' + str(index) + '个链接:')
            row_data = get_item(lines[index][0:-1])
            for row in row_data:
                row_count += 1
                excel_write.write_excel(sheet, row_count, row)
        except Exception:
            pass
            excel_write.save_file(file, '玉米需求3')
    print('---------------------')
    excel_write.save_file(file, '玉米需求3')