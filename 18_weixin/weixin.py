import requests
import json
from bs4 import BeautifulSoup as Bs4
import os
from selenium import webdriver
import re
import uuid


# 文章列表
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'IPLOC=CN3501; SUID=AA33CC794A42910A000000005F3B61D4; SUID=AA33CC795218910A000000005F3B61D4; weixinIndexVisited=1; SUV=0010B6E279CC33AA5F3B6856F5619293; pgv_pvi=7330187264; SMYUV=1599116135492843; UM_distinctid=17452bfcc482bf-03836ad679ffdc-58321f48-1fa400-17452bfcc494cb; ABTEST=0|1602489764|v1; SNUID=72FC8CB4DADF6BAF62F4054EDBA72181; JSESSIONID=aaaOysJl_evdigOiTnrux; ppinf=5|1602489894|1603699494|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlOEQlODElRTQlQkElOEN8Y3J0OjEwOjE2MDI0ODk4OTR8cmVmbmljazoxODolRTUlOEQlODElRTQlQkElOEN8dXNlcmlkOjQ0Om85dDJsdU96dmFOMlZtY3lrb0ExRi1ZTkpkSE1Ad2VpeGluLnNvaHUuY29tfA; pprdig=Z3KhJ2QJdlbdlwWgNRz20NNuezPh0S6JJUwhHZD-3hD5zqXUVswH8p3olWQAFXUgx_Ks31VQUZlSRBaWMhA6-c4L7VEWyHn3Y0MKoHyW1wwUCJ-nMJ9tJ4znLQgw2jyozpb4s1tVA2cua-q8g2bA-VpMRS2UDEa6YrbbQOxyDpM; ppinfo=7b4b339226; passport=5|1602489894|1603699494|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTUlOEQlODElRTQlQkElOEN8Y3J0OjEwOjE2MDI0ODk4OTR8cmVmbmljazoxODolRTUlOEQlODElRTQlQkElOEN8dXNlcmlkOjQ0Om85dDJsdU96dmFOMlZtY3lrb0ExRi1ZTkpkSE1Ad2VpeGluLnNvaHUuY29tfA|ea3db2ec39|Z3KhJ2QJdlbdlwWgNRz20NNuezPh0S6JJUwhHZD-3hD5zqXUVswH8p3olWQAFXUgx_Ks31VQUZlSRBaWMhA6-c4L7VEWyHn3Y0MKoHyW1wwUCJ-nMJ9tJ4znLQgw2jyozpb4s1tVA2cua-q8g2bA-VpMRS2UDEa6YrbbQOxyDpM; sgid=09-50157403-AVibEDiaZ4V4Dww60ggevTIVo; ppmdig=16024898940000004ee70284fbefc92252b9abd1e03bec81',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E8%A1%97%E6%8B%8D&ie=utf8&_sug_=n&_sug_type_=',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'
}
url = 'https://weixin.sogou.com/weixin'
options = '?type=2&s_from=input&query={}&ie=utf8&_sug_=n&_sug_type_=&page={}'


def get_article_list(key_word, page_num):
    # 获取文章列表链接
    res = requests.get(url + options.format(key_word, page_num), headers=headers)  # , allow_redirects=False
    soup = Bs4(res.text, 'lxml')
    if soup.text.find('没有找到相关的微信公众号文章。') != -1:
        raise Exception()
    links = []
    # 获取标题
    h3s = soup('h3')
    for h3 in h3s:
        a = h3.select('a')[0].get('href')
        links.append(a)
    return links


def get_article_link(original_link):
    # 拼接文章链接
    res2 = requests.get('https://weixin.sogou.com' + original_link, headers=headers)
    script_text = res2.text
    pattern = re.compile(r"url \+=.*?;")  # 查找数字
    result1 = pattern.findall(script_text)
    final = ''
    for item in result1:
        final += item[item.find("'")+1: item.find(";") - 1]
    print(final.replace("@", ""))
    return final.replace("@", "")


# 获取文章图片链接
headers2 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'cookie': 'pgv_pvid=5698158979; pgv_pvi=6700907520; eas_sid=P1r549s1n176U1t0N089f3t0o2; RK=MaIx2Y2mx0; ptcz=7460a9c43f61ba7655fe8503a676c2e36da5dcf7b0091c853216f61796044117; ua_id=74wXIGdhlWeVvAvnAAAAAKavht9knS5IY3c7vTWV4G0=; xid=29439867342341d97139bd6eec6844d6; openid2ticket_oE8SQ4rMTcwANIwXI58lukX8Dfqc=GhZGX6pmpnmxgbV1m17JCR++dM+1ZvYG0A4nPtMV38I=; mm_lang=zh_CN; wxuin=94173704501400; pac_uid=0_5f23bdc0da8d5; tvfe_boss_uuid=53b4b08895354960; rewardsn=; wxtokenkey=777',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'
}


def get_article_pic_links(final_link):
    res3 = requests.get(final_link, headers=headers2)
    soup3 = Bs4(res3.text, 'lxml')
    page_content = soup3('div', id='page-content')[0]
    images = page_content.select('img')
    images_links = []
    for image in images:
        link = image.get('data-src')
        if link is None:
            continue
        images_links.append(link)
        print(link)
    h2 = soup3('h2', id='activity-name')[0]
    print(h2.text)
    return {"title": h2.text.strip(), "pictures": images_links}


def save_image(title, url_list):
    root = './images/'
    title_dir = root + title
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(title_dir):
            os.mkdir(title_dir)

        for url in url_list:
            image_name = str(uuid.uuid1()).replace('-', '') + '.' + url.split('wx_fmt=')[-1]
            path = title_dir + '/' + image_name
            if not os.path.exists(path):
                r = requests.get(url)
                r.raise_for_status()
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print("图片保存成功")
            else:
                print("图片已存在")
    except Exception as e:
        print(e)
        print("图片获取失败")


if __name__ == '__main__':
    print("请输入关键字")
    key_word = input()
    for i in range(1, 10000):
        # 获取关键字下的第i页链接
        try:
            list_links = get_article_list(key_word, i)
            # 遍历链接
            for link in list_links:
                # 拿到最终链接
                final = get_article_link(link)
                # 获取文章图片链接
                res = get_article_pic_links(final)
                print(res)
                save_image(res['title'], res['pictures'])
        except:
            print('该关键字爬取完成')
            break
