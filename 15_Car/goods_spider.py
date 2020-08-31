import requests
import json
from bs4 import BeautifulSoup as Bs4

select1_list = ['jeep', 'land_rover', 'mitsubishi', 'nissan', 'suzuki', 'toyota', 'aro', 'asia_motors', 'audi', 'auverland',
             'bertone', 'bmw', 'cadillac', 'can_am', 'chevrolet_gm', 'citroen', 'dacia', 'daihatsu', 'dodge_chrysler', 'fiat',
             'ford_europe', 'ford_usa', 'galloper', 'gmc', 'honda', 'hummer_am_general', 'hyundai', 'infiniti', 'isuzu_gm', 'iveco',
             'jaguar', 'kia', 'lada', 'lexus', 'lincoln', 'mahindra', 'mazda', 'mercedes', 'mini', 'opel_vauxhall',
             'peugeot', 'polaris', 'porsche', 'portaro', 'puch_steyr', 'renault', 'saab', 'santana', 'skoda', 'ssangyong',
             'subaru', 'tata', 'uaz', 'umm', 'volkswagen', 'volvo']
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '23',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=92u39edv71go99cv5aiv30p893; languel=1; isol=0; tval=1; panierl=0; prixl=0; choixl=0; prol=0; pro_loginl=0; id_clientl=0; id_client_souvenirl=0; cmd_idl=0; cmd_corpsl=0; cmd_prix_totall=0; loi_cookiel=0; loi_hamonl=0; premiere_visitel=0; premiere_visite_ste_mariel=0; _ga=GA1.2.735137031.1598503378; _gid=GA1.2.1713094885.1598503378; _hjid=f6a5773e-744d-4392-8f3d-db7df8f94a29; _hjAbsoluteSessionInProgress=0; _hjAbsoluteSessionInProgress=0; hasConsent=2; champs_clientl=0; champs_vehiculel=0; champs_commandel=0; donneesl=0; cataloguel=0; _hjIncludedInPageviewSample=1; cle_modele2l=352; _uetsid=16a8f1ef67703eb02549d3b395e5ed90; _uetvid=d2366c2033305919922b445dac3cb842',
    'Host': 'www.euro4x4parts.com',
    'Origin': 'http://www.euro4x4parts.com',
    'Referer': 'http://www.euro4x4parts.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
    'X-Requested-With': 'XMLHttpRequest'
}
sub_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%227acfab24c70d9c199a3e65623bf8959e%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A14%3A%22203.218.249.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A115%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F84.0.4147.135+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1598534265%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7D2ea28fedb7abf72014ce0fbc55fbf0ec2b599d91; PHPSESSID=g6fo4n7f5noh3ssuvs1a1v7vg1; languel=1; isol=0; tval=1; panierl=0; prixl=0; choixl=0; prol=0; pro_loginl=0; id_clientl=0; id_client_souvenirl=0; cmd_idl=0; cmd_corpsl=0; cmd_prix_totall=0; loi_cookiel=0; loi_hamonl=0; premiere_visitel=0; premiere_visite_ste_mariel=0; _ga=GA1.2.240049314.1598534283; _gid=GA1.2.758458238.1598534283; _uetsid=e0da9ccd1ee4072100d0598dff9fa261; _uetvid=bb702a627f2a555e6343fd569f2de788; _hjid=6bbfb05e-a3e4-462b-b504-9b3c6d8aad82; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; hasConsent=2; champs_clientl=0; champs_vehiculel=0; champs_commandel=0; donneesl=0; cataloguel=0; cle_modele2l=1014',
    'Host': 'www.euro4x4parts.com',
    'Referer': 'http://www.euro4x4parts.com/jeep_parts/cherokee_1_xj_1997_2001/2_5i_petrol_1997_2000/1_service_items/F/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
}
url = 'http://www.euro4x4parts.com'


def has_contain_class(css_class):
    return str(css_class).find('content-ref') != -1


def get_select2_value(select1_value):
    """根据第一个关键字查询第二个关键字的值"""
    res = requests.post(url + '/?c=accueil&m=ajax_catalogue', headers=headers, data={'select0': select1_value, 'langue': '1'})
    return json.loads(res.content.decode())


def get_select3_value(select1_value, select2_value):
    """根据第二个关键字查询第三个关键字的值"""
    res = requests.post(url + '/?c=accueil&m=ajax_catalogue', headers=headers, data={'select0': select1_value, 'select1': select2_value, 'langue': '1'})
    return json.loads(res.content.decode())


def get_category_list(select3_url):
    """获取八个分类链接"""
    res = requests.get(select3_url)
    soup = Bs4(res.text, 'lxml')
    link_list = []
    entete_div_list = soup('section', attrs={'class': 'grille_superfam row'})[0].find_all(name='div', attrs={'class': 'entete'})
    for entete_div in entete_div_list:
        link_list.append(entete_div.select('a')[0].get('href'))
    return link_list


def get_all_items_url(category_url):
    res = requests.get(category_url)
    soup = Bs4(res.text, 'lxml')
    items_contain_list = soup('section', id='famille')[0].find_all(name='div', attrs={'class': 'liste_2cols ombre contenu row'})
    item_con = []
    for items_contain in items_contain_list:
        item_con.append(items_contain.find_all(name='li', attrs={'class': 'liG light'})[0].select('a')[0].get('href'))
    return item_con


def get_product_url_list(items_url):
    refer = items_url.split('/parts')[0] + '/'
    sub_headers['Referer'] = refer
    try:
        res = requests.get(items_url, headers=sub_headers, timeout=30)
    except Exception as e:
        res = requests.get(items_url, headers=sub_headers, timeout=30)
    soup = Bs4(res.text, 'lxml')
    goods_div_list = soup('div', attrs={'class': 'content-list-refs row-fluid'})[0].find_all(name='div', class_=has_contain_class)
    goods_link_list = []
    for goods_div in goods_div_list:
        goods_link_list.append(goods_div.select('a')[0].get('href'))
    return goods_link_list


def spider_main():
    # 读取重复
    r_repeat_f = open('repeat.txt')
    repeat_items = r_repeat_f.readlines()
    r_repeat_f.close()
    # 写入重复
    w_repeat_f = open('repeat.txt', 'a')
    for select1 in select1_list:
        if (select1 + '\n') in repeat_items:
            print(select1 + '重复')
            continue

        select2_list = get_select2_value(select1)
        for select2 in select2_list:
            if (select2['optionValue'] + '\n') in repeat_items:
                print(select2['optionValue'] + '重复')
                continue
            # 创建链接文件jeep_cherokee_1_xj_1984_1996.txt
            goods_link_file = open(select1 + '_' + select2['optionValue'] + '.txt', 'a', encoding='utf-8')

            select3_list = get_select3_value(select1, select2['optionValue'])
            for select3 in select3_list:
                full_name = select1 + ' > ' + select2['optionValue'] + ' > ' + select3['optionValue']
                print('类目位置：' + full_name)
                # 1.判断是否已经爬取过该车类
                if (select3['optionValue'] + '\n') in repeat_items:
                    print('重复')
                    continue
                # 2.读取每个车类零件的链接（例：8个）
                goods_link_file.write(full_name + '\n')

                try:
                    category_link_list = get_category_list(url + select3['optionValue'])
                except:
                    continue
                # 遍历零件
                for category_link in category_link_list:
                    print(category_link)
                    # 3.判断零件链接是否爬过
                    if (category_link + '\n') in repeat_items:
                        print('重复')
                        continue
                    # 4.通过每个零件的链接，获取零件下不同规格的分类链接

                    try:
                        item_url_list = get_all_items_url(url + category_link)
                    except:
                        continue
                    # 遍历四个 browser all this parts
                    for item_url in item_url_list:
                        # 获取98个产品链接
                        try:
                            goods_link_list = get_product_url_list(url + item_url)
                        except:
                            continue
                        print('产品数量：' + str(len(goods_link_list)))
                        for goods_link in goods_link_list:
                            goods_link_file.write(url + goods_link + '\n')
                        goods_link_file.flush()

                    w_repeat_f.write(category_link + '\n')
                    w_repeat_f.flush()
                w_repeat_f.write(select3['optionValue'] + '\n')
                w_repeat_f.flush()
            w_repeat_f.write(select2['optionValue'] + '\n')
            w_repeat_f.flush()
            goods_link_file.close()
        w_repeat_f.write(select1 + '\n')
        w_repeat_f.flush()
    w_repeat_f.close()


if __name__ == '__main__':
    spider_main()