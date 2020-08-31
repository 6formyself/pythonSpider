import requests
from bs4 import BeautifulSoup as Bs4
from time import sleep

head_url = 'https://you.ctrip.com'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_RF1=121.204.51.170; _RSG=MKKoCKy.X5CLJV_advekG8; _RDG=28ae214e10f80c2f331452432efd1a3af2; _RGUID=c161fbc5-0cc9-4516-842e-a399e4fdf4d5; _ga=GA1.2.1738225420.1597758100; MKT_CKID=1597758099804.3lfvk.ma7d; MKT_Pagesource=PC; ASP.NET_SessionSvc=MTAuMjUuMTY2LjMyfDkwOTB8b3V5YW5nfGRlZmF1bHR8MTU4OTAwNDY0OTQyNQ; _gid=GA1.2.756526625.1597914536; MKT_CKID_LMT=1597914537935; _bfa=1.1597758097384.44dc2r.1.1597758097384.1597914533451.2.32; _bfs=1.28; _gat=1; _jzqco=%7C%7C%7C%7C1597914543192%7C1.1645988122.1597758099799.1597915587036.1597915777754.1597915587036.1597915777754.undefined.0.0.31.31; __zpspc=9.2.1597914537.1597915777.27%234%7C%7C%7C%7C%7C%23; appFloatCnt=30; _bfi=p1%3D290570%26p2%3D290602%26v1%3D32%26v2%3D31',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

linkf = open('links.txt')
links = linkf.readlines()
youji = open('you_ji.txt', 'a')
for link in links:
    print('\n' + link[0:-1])
    res = requests.get(link[0:-1], headers=headers)
    soup = Bs4(res.text, 'lxml')
    you_ji_links = soup('a', attrs={'class': 'journal-item cf'})
    for you_ji_link in you_ji_links:
        href = you_ji_link.get('href')
        print(href)
        youji.write(head_url + href + '\n')
    youji.flush()
    sleep(1)
linkf.close()
youji.close()
