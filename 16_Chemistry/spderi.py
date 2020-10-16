# from selenium import webdriver
# from time import sleep
# from bs4 import BeautifulSoup as Bs4
#
# driver = webdriver.Chrome(executable_path='chromedriver.exe')
# driver.get('https://tcmspw.com/browse.php?qc=diseases')
# sleep(5)
# js = 'window.open("https://tcmspw.com/molecule.php?qn=432");'
# driver.execute_script(js)
# sleep(1)
# driver.switch_to.window(driver.window_handles[1])
# sleep(1)
# driver.refresh()
#
# soup = Bs4(driver.page_source, 'lxml')
# table = soup('table', attrs={'class': 'tableRst2'})[0]
# tr_list = table.select('')
#
# target = soup('div', id='kendo_target')[0]
import requests
import os
import base64


def save_image(url):
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '__cfduid=dc35af0f2d123d84b85aa7d485240d5ce1599918841; __cf_bm=47ad1c20f32ef48df10d3f7ff2d4596accad5761-1599918841-1800-Aedl7bSIpYrmtCnfFqZ8fa9IEp3vib/J7MogLZoeFeXcj9RCkuSDKTATz1L0sMIGgf4tnkJ6eCBKg+8rCdIFWrg=',
        'if-modified-since': 'Fri, 31 Jul 2020 13:41:46 GMT',
        'if-none-match': 'cb52150e6edebd71a136cc69cbd49301',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    d = './images/'
    image_name = url.split('/')[-1].split('?')[0]
    path = d + image_name
    try:
        if not os.path.exists(d):
            os.mkdir(d)
        if not os.path.exists(path):
            r = requests.get(url, headers=header)
            r.raise_for_status()
            with open(path, 'wb') as f:
                print(r.content)
                # f.write(base64.decode(r.content))
                f.close()
                print("图片保存成功")
        else:
            print("图片已存在")
    except Exception as e:
        print(e)
        print("图片获取失败")
    return path


if __name__ == '__main__':
    # save_image('https://cdna.artstation.com/p/assets/images/images/029/017/144/large/witchzz-bearwitch-001.jpg')
    f = open(r'waimai.txt')  # 二进制方式打开图文件
    imagedata = base64.b64decode(f.read())  # 解码

    file = open('timg.jpg', "wb")
    file.write(imagedata)
    f.close()