import pdfkit
import requests
from bs4 import BeautifulSoup as Bs4

url = 'https://finance.sina.com.cn/stock/data/2020-08-18/doc-iivhvpwy1695237.shtml'
# res = requests.get(url)
# print(res.encoding)
# soup = Bs4(res.text.encode('ISO-8859-1').decode('ISO-8859-1'), 'lxml')
# d = soup('div', attrs={'class': 'main-content w1240'})[0]
# print(d)
i = 2
confg = pdfkit.configuration(wkhtmltopdf='./wkhtmltopdf.exe')
pdfkit.from_url(url, 'jmeter_下载文件' + str(i) + '.pdf', configuration=confg)
# pdfkit.from_string(d, 'jmeter_下载文件' + str(i) + '.pdf', configuration=confg)
# pdfkit.from_file('hemt.txt', 'jmeter_下载文件' + str(1) + '.df', configuration=confg)