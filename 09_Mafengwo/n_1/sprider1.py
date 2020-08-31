# coding=utf-8
from html.parser import HTMLParser
from lxml import etree
import urllib.request
import urllib.parse
import re
import io
import gzip
import codecs


min = 50
max = 500

headerS={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'br-resp-key="g:2008182256901d7000000011f774d92ef8"; mfw_uuid=5f3bd6cd-ec7d-acff-3bdb-a8998bcf4b1a; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-08-18+21%3A25%3A33%22%3B%7D; __omc_chl=; __omc_r=; __mfwc=direct; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1597757134%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1597757134%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5f3bd6cd-ec7d-acff-3bdb-a8998bcf4b1a; UM_distinctid=17401bf1828547-0fcfa3a4974b83-3323767-1fa400-17401bf182a82d; __jsluid_h=341ca5f5f941c8f8b2c4861ceaca25b8; PHPSESSID=s37dani21i2iundf918hvakvk7; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1597757135,1597761419; __mfwlv=1597809752; __mfwvn=2; bottom_ad_status=0; __jsl_clearance=1597809961.563|0|1K%2BqOKvSNXCZZ2Zj0%2Bx9cISFS6g%3D; __mfwb=3cb315de725d.1.direct; __mfwa=1597757134162.85322.4.1597809752170.1597813199818; __mfwlt=1597813199; CNZZDATA30065558=cnzz_eid%3D188134141-1597754452-%26ntime%3D1597811485; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1597813200',
    'Host': 'www.mafengwo.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
}

link_list = open("youji.txt", 'r')
file = codecs.open("rsult.csv", 'a', 'utf-8')
for line in link_list:
    try:
        content = ""
        print(line)
        url = "http://www.mafengwo.cn" + line
        request = urllib.request.Request(url, data=None, headers=headerS)
        response = urllib.request.urlopen(request)
        page = response.read()
        iopage = io.BytesIO(page)
        depage = gzip.GzipFile(fileobj=iopage, mode="rb")
        html = depage.read().decode('utf-8')
        Htree = etree.HTML(html)
        # print(etree.tostring(Htree))
        body=Htree[1]
        # print(etree.tostring(body))
        main=body[1]
        # print(etree.tostring(main))
        view = main[3]
        # 此处使用etree以获取游记正文部分
        content = content + etree.tostring(view).decode('utf-8')
        content = HTMLParser().unescape(content)
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', content)
        dr = re.compile('\n', re.S)
        dd = dr.sub('', dd)
        dr = re.compile(' ', re.S)
        res = dr.sub('', dd)
        # 去除富文本标签、换行符、空格等
        print(res)
        file.write(str(res)+'\n')
    except Exception:
        pass
file.close()
