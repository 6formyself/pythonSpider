import requests
from bs4 import BeautifulSoup as Bs4
from time import sleep
import xlrd
import xlutils.copy
import os

url = 'https://www.pkulaw.com/case/pfnl'
head_url = 'https://www.pkulaw.com'
header = {
    "User-Agent": "PostmanRuntime/7.26.3",
    "Cookie": 'pkulaw_v6_sessionid=dgcr33ohf04qrzzvctqoxugb; authormes=1297637caf7621801819041472edf8fde1342fa0363c6ed9773e70fbfba2f6289f26f851f798bce0bdfb; Hm_lvt_8266968662c086f34b2a3e2ae9014bf8=1597664779; xCloseNew=18; redSpot=false; xClose=17; Hm_lpvt_8266968662c086f34b2a3e2ae9014bf8=1597716700; Porschev=MainSessionId=lsist5ufrzts2spe2beis1b1',
    "Host": "www.pkulaw.com",
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

body = {
    'Menu': 'case',
    'Keywords': '（2019）鲁05执128号',
    'PreKeywords': '（2019）鲁05执128号',
    'SearchKeywordType': 'DefaultSearch',
    'MatchType': 'Exact',
    'Library': 'pfnl',
    'ClassFlag': 'pfnl',
    'QuerySearchCondition': 'DefaultSearch+Exact+undefined+0',
    'QueryOnClick': False,
    'AfterSearch': True,
    'RequestFrom': 'btnSearch',
    'PreviousLib': 'pfnl',
    'IsSynonymSearch': 'true',
    'RecordShowType': 'List',
    'ClassCodeKey': ',,,,,,,,,',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_wen_shu_link(key_word):
    body['Keywords'] = key_word
    res = requests.post(url, headers=header, data=body)
    soup = Bs4(res.text, 'lxml')
    try:
        li_list = soup('div', attrs={'class': 'list-wrap'})[0].select('ul')[1].select('li')
    except Exception as e:
        return -1
    link_list = []
    for li in li_list:
        h4 = li.select('h4')[0]
        wen_shu_link = head_url + h4.select('a')[0].get('href')
        link_list.append(wen_shu_link)
        print(wen_shu_link)
    return link_list


def get_struct_data(link):
    res = requests.get(link, headers=header)
    soup = Bs4(res.text, 'lxml')
    all_text = "\n".join(list(soup('div', attrs={'class': 'content'})[0].stripped_strings))
    data_con = { "slfy": "-", "slfg": "-", "wslx": "-", "ajlx": "-", "sjrq": "-", "slcx": "-" }
    li_s = soup('div', attrs={'class': 'fields'})[0].select('ul')[0].select('li')
    for li in li_s:
        str_data = list(li.stripped_strings)
        if str_data[0] == '审理法院：':
            data_con['slfy'] = ",".join(str_data[1:])
        if str_data[0] == '审理法官：':
            data_con['slfg'] = ",".join(str_data[1:])
        if str_data[0] == '文书类型：':
            data_con['wslx'] = ",".join(str_data[1:])
        if str_data[0] == '案件类型：':
            data_con['ajlx'] = ",".join(str_data[1:])
        if str_data[0] == '审结日期：':
            data_con['sjrq'] = ",".join(str_data[1:])
        if str_data[0] == '审理程序：':
            data_con['slcx'] = ",".join(str_data[1:])
    h2_text = list(soup('div', attrs={'class': 'content'})[0].select('h2')[0].stripped_strings)[0]
    if len(h2_text.split('与')) > 1:
        return h2_text.split('与'), data_con, all_text
    if len(h2_text.split('、')) > 1:
        return h2_text.split('、'), data_con, all_text
    if len(h2_text.split('诉')) > 1:
        return h2_text.split('诉'), data_con, all_text
    return [h2_text, '-'], data_con


if __name__ == "__main__":
    # 读取excel
    r_book = xlrd.open_workbook('文书数据.xlsx')
    rows = r_book.sheets()[0].nrows
    w_book = xlutils.copy.copy(r_book)
    sheet = w_book.get_sheet(0)
    # 读取案号
    an_hao_file = open('anhao.txt')
    an_hao_list = an_hao_file.readlines()
    for an_hao in list(set(an_hao_list)):
        print(an_hao[0:-1] + ':')
        link_list = get_wen_shu_link(an_hao[0:-1])
        if link_list == -1:
            print('改案号未查询到案件！')
            continue
        for link in link_list:
            try:
                h2_text, data, all_text = get_struct_data(link)
            except Exception:
                sleep(1)
                try:
                    h2_text, data, all_text = get_struct_data(link)
                except Exception:
                    continue
            file_name = ''
            if os.path.exists('./全文/' + an_hao[0:-1] + '.txt'):
                file_name = './全文/' + an_hao[0:-1] + str(rows) + '.txt'
            else:
                file_name = './全文/' + an_hao[0:-1] + '.txt'
            f = open('./全文/' + an_hao[0:-1] + str(rows) + '.txt', 'a', encoding='utf-8')
            f.writelines(all_text)
            f.close()
            print(h2_text)
            print(data)
            sheet.write(rows, 0, an_hao[0:-1])
            sheet.write(rows, 1, h2_text[0])
            sheet.write(rows, 2, h2_text[1])
            sheet.write(rows, 3, data['slfy'])
            sheet.write(rows, 4, data['slfg'])
            sheet.write(rows, 5, data['wslx'])
            sheet.write(rows, 6, data['ajlx'])
            sheet.write(rows, 7, data['sjrq'])
            sheet.write(rows, 8, data['slcx'])
            rows += 1
            w_book.save('文书数据.xlsx')
    w_book.save('文书数据.xlsx')