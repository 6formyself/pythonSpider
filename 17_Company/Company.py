import requests
import json
from bs4 import BeautifulSoup as Bs4
import os
import csv
from time import sleep
# 爬取国家知识产权的企业信息，企业名称和图片
# 1.分页查询接口
country_search_url = 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearchDG.html'
country_code_url = 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html'
country_image_url = 'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/imageView.html'
# 获取商标期数
s = open('qishu.txt').read().split(' ')
qishu = int(s[0])
yeshu = int(s[1])

country_header = {
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '__jsluid_h=69506c7f023329110a1411d8dc362b41; tmas_cookie=51947.7706.15402.0000; JSESSIONID=0000NUWd7rRPNJHaicNY7BP13bz:1bm112lvs',
    'Host': 'wsgg.sbj.cnipa.gov.cn:9080',
    'Origin': 'http://wsgg.sbj.cnipa.gov.cn:9080',
    'Referer': f'http://wsgg.sbj.cnipa.gov.cn:9080/tmann/annInfoView/annSearch.html?annNum={qishu}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_company_name_img(page_num):
    """传入页码，获取20个公司的名称与商标图片链接"""
    saeach_data = f'page={page_num}&rows=20&annNum={qishu}&annType=&tmType=&coowner=&recUserName=&allowUserName=&byAllowUserName=&appId=&appIdZhiquan=&bfchangedAgengedName=&changeLastName=&transferUserName=&acceptUserName=&regName=&tmName=&intCls=&fileType=&totalYOrN=false&appDateBegin=&appDateEnd=&agentName='
    search_res = requests.post(country_search_url, headers=country_header, data=saeach_data)
    company_list = json.loads(search_res.content.decode())['rows']
    data_con = []
    for company in company_list:
        company_name = company['regname']
        # 获取id
        id_data = f'annNum={qishu}&annTypecode={company["ann_type_code"]}'
        id_res = requests.post(country_code_url, headers=country_header, data=id_data)
        id = id_res.content.decode()
        # 获取图片列表
        img_data = f'id={id}&pageNum={company["page_no"]}&flag=1'
        img_res = requests.post(country_image_url, headers=country_header, data=img_data)
        image = json.loads(img_res.content)['imaglist'][3]
        try:
            print(company_name, image)
        except:
            print('有特殊字符无法打印，但数据写入正常！')
            pass
        data_con.append([company_name, image])
    return data_con


# 2.启信宝查询企业信息
cookie_file = open('cookie.txt')
cookie = cookie_file.readlines()[0][0:-1]
head_url = 'https://www.qixin.com'
url = 'https://www.qixin.com/search?key={}&page=1'
qixinbao_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': cookie,
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
}
cookie_file.close()
print(cookie)


def get_qixinbao_info(company_name):
    res = requests.get(url.format(company_name), headers=qixinbao_header)
    soup = Bs4(res.text, 'lxml')
    if soup.text.find('点击按钮进行验证') != -1:
        print('网站出现验证码请前往：' + url.format(company_name) + '确认！确认完毕请输入1，并按回车')
        open('test.txt', 'w', encoding='utf-8').write(soup.text)
        print(soup.text.find('点击按钮进行验证'))
        input()
        res = requests.get(url.format(company_name), headers=qixinbao_header)
        soup = Bs4(res.text, 'lxml')
    try:
        container = soup('div', attrs={'class': 'col-xs-24 padding-v-25px margin-0-0x border-b-b4 company-item'})[0].find_all('div', class_='col-2-1')[0]
    except:
        return '-', '-', '-'
    string_list = list(container.stripped_strings)
    faren = phone = addr = '-'
    try:
        faren = string_list[string_list.index('法定代表人：') + 1]
    except:
        print('没有法人！')
    try:
        phone = string_list[string_list.index('电话：') + 1]
    except:
        print('没有电话！')
    try:
        addr = '地址：' + string_list[string_list.index('地址：') + 1]
    except:
        print('没有地址！')
    return faren, phone, addr


# 企查查
def qcc(company_name):
    h = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': 'QCCSESSID=fsj5ivm4ji91hq9hjqonqohh26; UM_distinctid=1748163199595c-05a7e5d1ee96bc-7d647865-1fa400-17481631996991; zg_did=%7B%22did%22%3A%20%22174816319a261d-04c185ae4459dd-7d647865-1fa400-174816319a39af%22%7D; hasShow=1; _uab_collina=159989858986493199639217; Hm_lvt_78f134d5a9ac3f92524914d0247e70cb=1599898590; acw_tc=7518019715999136917252716e4a155a521b0dfb4d349598b67523b90d; CNZZDATA1254842228=816694089-1599893811-https%253A%252F%252Fwww.baidu.com%252F%7C1599910011; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201599913693042%2C%22updated%22%3A%201599914052522%2C%22info%22%3A%201599898589612%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22cuid%22%3A%20%22ebe496ca7c6c9e6ad97b81132af1fc9f%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%7D; Hm_lpvt_78f134d5a9ac3f92524914d0247e70cb=1599914053',
        'referer': 'https://www.qcc.com/search?key=%E6%B2%B3%E6%BA%90%E5%B8%82%E4%BA%BF%E9%87%91%E9%87%91%E5%B1%9E%E7%A7%91%E6%8A%80%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51'
    }
    res = requests.get(f'https://www.qcc.com/search?key={company_name}', headers=h)
    soup = Bs4(res.text, 'lxml')
    if soup.text.find('您的操作过于频繁，验证后再操作') != -1 or res.text.find("window.location.href='https://www.qcc.com/index_verify?type=companysearch") != -1:
        print('网站出现验证，请前往：' + f'https://www.qcc.com/search?key={company_name} ' + '确认，确认完毕请输入1并回车：')
        input()
    res = requests.get(f'https://www.qcc.com/search?key={company_name}', headers=h)
    soup = Bs4(res.text, 'lxml')
    t = soup('table', attrs={'class': 'm_srchList'})[0].find('tbody', id='search-result').select('tr')[0].find_all('td')[2]
    s = t.text.replace(' ', '').split('\n')
    faren = s[s.index('法定代表人：') + 1].split('注册资本')[0]
    phone = s[s.index('电话：') + 1]
    addr = ''
    for item in s:
        if item.find('地址') != -1:
            addr = item
    return faren, phone, addr


# 3.保存图片
def save_image(url, image_num):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__jsluid_h=6a91b2b9e46906bae5002a22dfb68e2c',
        'Host': 'sbggwj.sbj.cnipa.gov.cn:8000',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    d = './images/'
    image_name = str(image_num) + '.' + url.split('/')[-1].split('.')[-1]
    image_num += 1
    path = d + image_name
    try:
        if not os.path.exists(d):
            os.mkdir(d)
        if not os.path.exists(path):
            r = requests.get(url, headers=header)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("图片保存成功")
            with open('image.txt', 'a') as f:
                f.write(str(image_num) + '\n')
                f.close()
        else:
            print("图片已存在")
    except Exception as e:
        print(e)
        print("图片获取失败")
    return path


def spider_main():
    # repeat_r = open('repeat.txt')
    # repeat_lines = repeat_r.readlines()
    # begin_num = int(repeat_lines[-1][0:-1])
    # repeat_r.close()
    # print('加载到进度：第' + str(begin_num) + '页')
    image_r = open('image.txt')
    image_lines = image_r.readlines()
    image_num = int(image_lines[-1][0:-1])
    image_r.close()
    print('请输入开始页数：')
    begin_num = int(input())
    print('请输入结束页数：')
    end_num = int(input())
    repeat_w = open('repeat.txt', 'a')
    for i in range(begin_num,  end_num):
        # for i in range(begin_num,  yeshu):
        print(f'开始写入第{i}页！')
        # 20个企业信息
        company_info_list = get_company_name_img(i)
        for company_info in company_info_list:
            # 企业名称
            company_name = company_info[0]
            # 法人，电话，地址
            try:
                # faren, phone, addr, = qcc(company_name)
                faren, phone, addr, = get_qixinbao_info(company_name)
            except:
                continue
            # 图片
            image_name = save_image(company_info[1], image_num)
            image_num += 1
            try:
                print([company_name, image_name, faren, phone, addr])
            except:
                print('有特殊字符无法打印，但数据写入正常！')
                pass
            with open("company.csv", 'a', newline='', encoding='utf-8') as f:
                row = [company_name, image_name, faren, phone, addr]
                write = csv.writer(f)
                write.writerow(row)
                print("写入完毕！")
        print(f'第{i}页已经写入完毕！')
        repeat_w.write(str(i + 1) + '\n')
        repeat_w.flush()
    repeat_w.close()


if __name__ == '__main__':
    # print(qcc('恩施尊硒茶业开发有限公司'))
    spider_main()
    # print(qixinbao_header['Cookie'])
    # print(get_qixinbao_info('南京沙拉拉供应链管理有限公司'))
