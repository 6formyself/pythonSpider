from bs4 import BeautifulSoup as Bs4
import requests
import json

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'br-resp-key="g:2008211437134270000000be26272265f2"; mfw_uuid=5f3bd6cd-ec7d-acff-3bdb-a8998bcf4b1a; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-08-18+21%3A25%3A33%22%3B%7D; __omc_chl=; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1597757134%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1597757134%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5f3bd6cd-ec7d-acff-3bdb-a8998bcf4b1a; UM_distinctid=17401bf1828547-0fcfa3a4974b83-3323767-1fa400-17401bf182a82d; PHPSESSID=s37dani21i2iundf918hvakvk7; _r=csdn; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A47%3A%22blog.csdn.net%2Fstarsliu%2Farticle%2Fdetails%2F49019689%22%3Bs%3A1%3A%22t%22%3Bi%3A1597814646%3B%7D; __mfwothchid=referrer%7Cblog.csdn.net; __mfwc=referrer%7Cblog.csdn.net; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1597757135,1597761419,1597814648; __omc_r=; __mfwa=1597757134162.85322.8.1597913147652.1597991546579; __mfwlv=1597991546; __mfwvn=6; __mfwb=e04e80854e51.2.direct; __mfwlt=1597991617; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1597991617',
    'Host': 'pagelet.mafengwo.cn',
    'Referer': 'http://www.mafengwo.cn/poi/829.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery18106878960410176205_1597991617055&params=%7B%22poi_id%22%3A%22829%22%2C%22page%22%3A2%2C%22just_comment%22%3A1%7D&_ts=1597992619501&_sn=d37df26902&_=1597992619502'
aaa = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?callback=jQuery18106878960410176205_1597991617055&params=%7B%22poi_id%22%3A%22829%22%2C%22page%22%3A1%2C%22just_comment%22%3A1%7D&_ts=1597993466346&_sn=4a6fa23533&_=1597993466346'
res = requests.get(url, headers=headers)
print(res.content.decode().encode('UTF-8'))
open('c.html', 'a').writelines(str(res.content.decode().encode('UTF-8')))
#print(res.encoding)
#print(res.content.decode(res.encoding))
#print(json.loads(res.content))
#print(json.dump(res.content).decode('utf-8'))
# json_str = res.content.decode()
# dict_data = json.loads(json_str)
# print(dict_data)