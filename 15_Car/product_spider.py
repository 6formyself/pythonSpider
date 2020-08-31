import requests
import json
import csv
import os
from bs4 import BeautifulSoup as Bs4
select1_list = ['jeep', 'land_rover', 'mitsubishi', 'nissan', 'suzuki', 'toyota', 'aro', 'asia_motors', 'audi', 'auverland',
             'bertone', 'bmw', 'cadillac', 'can_am', 'chevrolet_gm', 'citroen', 'dacia', 'daihatsu', 'dodge_chrysler', 'fiat',
             'ford_europe', 'ford_usa', 'galloper', 'gmc', 'honda', 'hummer_am_general', 'hyundai', 'infiniti', 'isuzu_gm', 'iveco',
             'jaguar', 'kia', 'lada', 'lexus', 'lincoln', 'mahindra', 'mazda', 'mercedes', 'mini', 'opel_vauxhall',
             'peugeot', 'polaris', 'porsche', 'portaro', 'puch_steyr', 'renault', 'saab', 'santana', 'skoda', 'ssangyong',
             'subaru', 'tata', 'uaz', 'umm', 'volkswagen', 'volvo']
url = 'http://www.euro4x4parts.com'
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
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=92u39edv71go99cv5aiv30p893; languel=1; isol=0; tval=1; panierl=0; prixl=0; choixl=0; prol=0; pro_loginl=0; id_clientl=0; id_client_souvenirl=0; cmd_idl=0; cmd_corpsl=0; cmd_prix_totall=0; loi_cookiel=0; loi_hamonl=0; premiere_visitel=0; premiere_visite_ste_mariel=0; _ga=GA1.2.735137031.1598503378; _gid=GA1.2.1713094885.1598503378; _hjid=f6a5773e-744d-4392-8f3d-db7df8f94a29; _hjAbsoluteSessionInProgress=0; hasConsent=2; champs_clientl=0; champs_vehiculel=0; champs_commandel=0; donneesl=0; cataloguel=0; _hjIncludedInPageviewSample=1; cle_modele2l=353; _uetsid=16a8f1ef67703eb02549d3b395e5ed90; _uetvid=d2366c2033305919922b445dac3cb842; _hjAbsoluteSessionInProgress=0; ci_session=a%3A5%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%223be2343c7af475a14d8aff111bb3ce7b%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A15%3A%22203.218.249.182%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A120%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F84.0.4147.135+Safari%2F537.36+Edg%2F%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1598598099%3Bs%3A9%3A%22user_data%22%3Bs%3A0%3A%22%22%3B%7Dd7bf6d5dedef7ce93fea2fdd68e255ea35738e4b',
    'Host': 'www.euro4x4parts.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63'
}


def get_select2_value(select1_value):
    """根据第一个关键字查询第二个关键字的值"""
    res = requests.post(url + '/?c=accueil&m=ajax_catalogue', headers=headers, data={'select0': select1_value, 'langue': '1'})
    return json.loads(res.content.decode())


def get_struct_data(product_link):
    # A
    print('数据源：' + product_link)
    data_con = []
    try:
        res = requests.get(product_link, headers=sub_headers, timeout=10)
    except Exception:
        res = requests.get(product_link, headers=sub_headers, timeout=10)
    soup = Bs4(res.text, 'lxml')
    # B
    try:
        name_header = ' - '.join(list(soup('div', id='detail_refs')[0].stripped_strings)[2:])
        name_back = ' '.join(list(soup.select('h1')[0].stripped_strings))
        if len(name_header) == 0:
            data_con.append(name_back)
        else:
            data_con.append(name_header + ' - ' + name_back)
        print('Name：' + name_header + ' - ' + name_back)
    except Exception:
        print('Name：暂无数据！')
        data_con.append('')
    # C
    try:
        detail_note = ' '.join(list(soup('p', id='detail_notes')[0].stripped_strings))
        # detail_note.encode('utf-8').decode('gbk')
        data_con.append(detail_note)
        print('Short description：正常')
    except Exception as e:
        print(e)
        print('Short description：暂无数据！')
        data_con.append('')
    # D
    nav_str = list(soup('div', attrs={'class': 'basic_liens'})[0].stripped_strings)
    try:
        value = ' '.join(nav_str).split('›')[-1].strip()
        table_list = soup('div', attrs={'class': 'conteneur ombre'})[0].select('table')
        description_str = ''
        if len(table_list) == 1:
            print('该产品没有Description字段')
        else:
            for i in range(1, len(table_list)):
                if len(table_list[i].select('img')) != 0:
                    continue
                if table_list[i].text.find('parts') != -1:
                    description_str += 'This ' + value + ' also fits these models :\n\n'
                    for j in range(0, len(list(table_list[i].stripped_strings))):
                        description_str += list(table_list[i].stripped_strings)[j]
                        if list(table_list[i].stripped_strings)[j].find('parts') != -1:
                            description_str += ' '
                        if (j+1) % 3 == 0:
                            description_str += '\n'
                    description_str += '\n\n'
                elif table_list[i].select('width') is not None and table_list[i].text.find('parts') == -1:
                    description_str += 'This ' + value + ' also fits some models from the following makes of vehicle (click on manufacturer for more details):\n\n'
                    description_str += '\n'.join(list(table_list[i].stripped_strings))
        if description_str.endswith(':'):
            description_str = ''
        print('Description：' + description_str)
        data_con.append(description_str)
    except Exception:
        print('该产品没有Description字段')
        data_con.append('')
    # E & F
    weight = price = ''
    try:
        weight = list(soup('p', id='poids_prix')[0].stripped_strings)[0].split('kg')[0].split(':')[1].strip()
        price = soup('span', attrs={'itemprop': 'price'})[0].text
    except Exception:
        print('Weight or Price has problem!')
    data_con.append(weight)
    data_con.append(price)
    print('Weight (kg)：' + weight + '\n' + 'Regular price：' + price)
    # G
    category_splice = ' '.join(nav_str).split('›')[1:]
    category_str = ''
    if len(category_splice) == 2:
        item0 = category_splice[0].strip().replace('>', '')
        item1 = category_splice[1].strip().replace('>', '')
        category_str += item0 + ', ' + item0 + ' > ' + item1
    elif len(category_splice) == 3:
        item0 = category_splice[0].strip().replace('>', '')
        item1 = category_splice[1].strip().replace('>', '')
        item2 = category_splice[2].strip().replace('>', '')
        category_str += item0 + ', ' + item0 + ' > ' + item1 + ', ' + item0 + ' > ' + item1 + ' > ' + item2
    elif len(category_splice) == 4:
        item0 = category_splice[0].strip().replace('>', '')
        item1 = category_splice[1].strip().replace('>', '')
        item2 = category_splice[2].strip().replace('>', '')
        item3 = category_splice[3].strip().replace('>', '')
        category_str += item0 + ', ' + item0 + ' > ' + item1 + ', ' + item0 + ' > ' + item1 + ' > ' + item2 + ', ' + item3
    elif len(category_splice) == 5:
        item0 = category_splice[0].strip().replace('>', '')
        item1 = category_splice[1].strip().replace('>', '')
        item2 = category_splice[2].strip().replace('>', '')
        item3 = category_splice[3].strip().replace('>', '')
        item4 = category_splice[4].strip().replace('>', '')
        category_str += item0 + ', ' + item0 + ' > ' + item1 + ', ' + item0 + ' > ' + item1 + ' > ' + item2 + ', ' + item3 + ',' + item3 + ' > ' + item4
    else:
        category_str = '个数在2345之外'
    print('Categories：' + category_str)
    data_con.append(category_str)
    # H
    data_con.append('Classify')
    print('Attribute 1 name：Classify')
    # I
    try:
        attribute_value = list(soup('div', attrs={'class': 'basic_liens'})[0].stripped_strings)
        print('Attribute 1 value(s)：正常')
        data_con.append('>'.join(' '.join(attribute_value).split('›')[-2:]).strip())
    except Exception:
        data_con.append('')
    return data_con


def spider_main():
    # 读取重复
    r_repeat_f = open('p_repeat.txt')
    repeat_items = r_repeat_f.readlines()
    r_repeat_f.close()
    # 写入重复
    w_repeat_f = open('p_repeat.txt', 'a')
    flag = False
    for select1 in select1_list:
        if (select1 + '\n') in repeat_items:
            print(select1 + '重复')
            continue

        select2_list = get_select2_value(select1)
        for select2 in select2_list:
            if (select2['optionValue'] + '\n') in repeat_items:
                print(select2['optionValue'] + '重复')
                continue
            try:
                goods_link_list = open(select1 + '_' + select2['optionValue'] + '.txt', encoding='utf-8').readlines()
            except Exception as e:
                flag = True
                break
            if not os.path.exists(select1 + '_' + select2['optionValue'] + ".csv"):
                with open(select1 + '_' + select2['optionValue'] + ".csv", 'a', newline='', encoding='utf-8-sig') as csv_f:
                    csv_write = csv.writer(csv_f)
                    csv_write.writerow(['Name', 'Short description', 'Description', 'Weight (kg)', 'Regular price', 'Categories', 'Attribute 1 name', 'Attribute 1 value(s)'])
            print('当前位置：' + select1 + '_' + select2['optionValue'] + '.txt')
            try:
                record_line = int(repeat_items[-1][0:-1])
                print('加载到进度：' + str(record_line))
            except Exception:
                record_line = 0
            print(len(goods_link_list))
            # 爬取产品详情数据
            for i in range(record_line, len(goods_link_list)):
                if not goods_link_list[i].startswith('http://www.euro4x4parts.com'):
                    continue
                try:
                    data = get_struct_data(goods_link_list[i][0:-1])
                except Exception:
                    w_repeat_f.write(str(i) + '\n')
                    w_repeat_f.flush()
                    print('出现错误，已记录进度！')
                    continue
                with open(select1 + '_' + select2['optionValue'] + ".csv", 'a', newline='', encoding='utf-8-sig') as csv_f:
                    csv_write = csv.writer(csv_f)
                    csv_write.writerow(data)
                    print("写入完毕！")

            w_repeat_f.write(select2['optionValue'] + '\n')
            w_repeat_f.flush()

            print('爬取完成：' + select1 + '_' + select2['optionValue'] + '.txt')
        if flag:
            break
        w_repeat_f.write(select1 + '\n')
        w_repeat_f.flush()
    w_repeat_f.close()


if __name__ == '__main__':
    # a = get_struct_data('http://www.euro4x4parts.com/parts/jpe1083-5392_pads_high_performance_ebc_greenstuff_7L0698151J.html')
    # with open('test.csv', 'a', newline='', encoding='utf-8-sig') as f:
    #     write = csv.writer(f)
    #     write.writerow(a)
    #     print("写入完毕！")
    spider_main()