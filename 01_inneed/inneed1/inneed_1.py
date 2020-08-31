import requests
from bs4 import BeautifulSoup as Bs4
from Tool.excel import excel_write

head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

head_url = 'https://grain.sci99.com'
url = [
    '/channel/corn'
]


def get_more_urls(m_head_url, back_url):
    """获取所有更多的链接"""
    html = requests.get(m_head_url + back_url, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    a_list = soup.select('a')
    all_url_list = []
    for a_tag in a_list:
        if str(a_tag).find("更多") != -1:
            url_href = a_tag.get('href')
            if url_href and url_href.startswith('/news'):
                print(m_head_url + url_href)
                all_url_list.append(m_head_url + url_href)
    return all_url_list


def get_title_link(item_url):
    """将数据页面的url记录"""
    links_file = open('links.txt', 'a')
    # data_list = []
    html = requests.get(item_url, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    # 拿到尾页数据
    aa_list = soup.select('a')
    useable_a = []
    for aa in aa_list:
        if aa.get('href') and aa.get('href').startswith('/news/?page='):
            useable_a.append(aa.get('href'))
    if len(useable_a) == 0:
        return
    i_need = useable_a[len(useable_a) - 1]
    pages = int(i_need[12:i_need.find('&')])
    params = i_need[i_need.find('&'):]
    # 第一页的数据
    links_file.write(item_url + '\n')
    # get_item(data_list, item_url)
    # 其他页数据
    for i in range(2, pages + 1):
        uri = 'https://grain.sci99.com/news/?page=' + str(i) + params
        print(uri)
        links_file.write(uri + '\n')
        # get_item(data_list, uri)
    links_file.close()
    # return data_list


def get_item(uri):
    """通过url读取数据页面的数据"""
    data_con = []
    html = requests.get(uri, headers=head)
    html.encoding = 'utf-8'
    soup = Bs4(html.text, 'lxml')
    ul_list = soup.select('ul')
    for ul in ul_list:
        class_name = ul.get('class')
        if class_name and class_name[0].startswith('ul_w488'):
            a_list = ul.select('a')
            for a_item in a_list:
                href = head_url + '/news/' + a_item.get('href')
                title = a_item.string.strip()
                data_con.append([title, href])
    return data_con


if __name__ == '__main__':
    # 写入链接
    # for my_url in url:
    #     print(my_url)
    #     url_list = get_more_urls(head_url, my_url)
    #     # 遍历 [更多]
    #     for url_item in url_list:
    #         print(url_item)
    #         get_title_link(url_item)
    # 读取数据
    my_file = open('links.txt')
    lines = my_file.readlines()
    sheet, file = excel_write.get_sheet('玉米需求1')
    row_count = 0
    for index in range(0, len(lines)):
        try:
            print(index)
            row_data = get_item(lines[index][0:-1])
            for row in row_data:
                row_count += 1
                excel_write.write_excel(sheet, row_count, row)
        except Exception:
            excel_write.save_file(file, '玉米需求1')
    print('---------------------')
    excel_write.save_file(file, '玉米需求1')

