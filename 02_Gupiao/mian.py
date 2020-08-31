import requests
from bs4 import BeautifulSoup as Bs4

api = 'http://data.10jqka.com.cn/ajax/yjgg/op/code/code/{}/ajax/1/free/1/'
head = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'data.10jqka.com.cn',
    'Referer': 'http://data.10jqka.com.cn/financial/yjgg/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}
export_url = 'http://basic.10jqka.com.cn/api/stock/export.php?export=main&'
data_type = ['report', 'year', 'simple']


def main_get():
    print('请输入公司股票代码：')
    company_code = str(input())
    for item in data_type:
        a = export_url + 'type=' + item + '&code=' + company_code
        print(a)
        res = requests.get(a, headers=header)
        res.raise_for_status()
        path = './数据表格/{}_main_{}.xls'.format(company_code, item)
        print('正在下载文件：', path)
        with open(path, 'wb') as f:
            f.write(res.content)
            f.close()
            print("数据保存成功")


if __name__ == '__main__':
    while True:
        main_get()
