import requests
import json
import xlrd
import xlutils.copy
from time import sleep
from Tool.LocationData.test import province_info

url = 'https://apis.map.qq.com/ws/district/v1/getchildren'
key = 'MKMBZ-5CXCJ-ZQ7FC-KFJ3J-2HYUT-3HBSN'


def get_location_data(id):
    if len(str(id)) > 6:
        return -1
    sleep(0.2)
    res = requests.get(url + '?key=' + key + '&id=' + id)
    try:
        json_str = res.content.decode()
        dict_data = json.loads(json_str)
        location_data = dict_data['result'][0]
    except Exception as e:
        print(id)
        print(res.content.decode())
        print(e)
        input()
        return -1
    return_data =[]
    for item in location_data:
        location_name = item['fullname']
        location_code = item['id']
        location_lng = item['location']['lng']
        location_lat = item['location']['lat']
        return_data.append([location_name, location_code, location_lng, location_lat])
    return return_data


if  __name__ == '__main__':
    r_book = xlrd.open_workbook(r'区域数据.xlsx')
    rows = r_book.sheets()[0].nrows
    w_book = xlutils.copy.copy(r_book)
    w_sheet = w_book.get_sheet(0)
    # 1.获取省级信息--一级
    # res = requests.get(url + '?key=' + key)
    # json_str = res.content.decode()
    # dict_data = json.loads(json_str)
    # province_data = dict_data['result'][0]
    # {'id': '350000','fullname': '福建省',, 'location': {'lat': 39.90469, 'lng': 116.40717}}
    print(province_info)
    for province in province_info:
        province_name = province['fullname']
        province_code = province['id']
        province_lng = province['location']['lng']
        province_lat = province['location']['lat']
        # 2.查询市级信息--二级
        shi_data = get_location_data(province_code)
        print(shi_data)
        # {'id': '350100','fullname': '福州市',, 'location': {'lat': 39.90469, 'lng': 116.40717}}
        if len(shi_data) == 0:
            w_sheet.write(rows, 0, province_name)
            w_sheet.write(rows, 1, province_code)
            w_sheet.write(rows, 2, province_lng)
            w_sheet.write(rows, 3, province_lat)
            rows += 1
            w_book.save(r'区域数据.xlsx')
            continue
        for shi in shi_data:
            # 3.查询区县信息--三级
            qu_data = get_location_data(shi[1])
            print(qu_data)
            if len(qu_data) == 0:
                w_sheet.write(rows, 0, province_name)
                w_sheet.write(rows, 1, province_code)
                w_sheet.write(rows, 2, province_lng)
                w_sheet.write(rows, 3, province_lat)
                w_sheet.write(rows, 4, shi[0])
                w_sheet.write(rows, 5, shi[1])
                w_sheet.write(rows, 6, shi[2])
                w_sheet.write(rows, 7, shi[3])
                rows += 1
                w_book.save(r'区域数据.xlsx')

                continue
            # {'id': '350121','fullname': '闽侯县',, 'location': {'lat': 39.90469, 'lng': 116.40717}}
            for qu in qu_data:
                w_sheet.write(rows, 0, province_name)
                w_sheet.write(rows, 1, province_code)
                w_sheet.write(rows, 2, province_lng)
                w_sheet.write(rows, 3, province_lat)
                w_sheet.write(rows, 4, shi[0])
                w_sheet.write(rows, 5, shi[1])
                w_sheet.write(rows, 6, shi[2])
                w_sheet.write(rows, 7, shi[3])
                w_sheet.write(rows, 8, qu[0])
                w_sheet.write(rows, 9, qu[1])
                w_sheet.write(rows, 10, qu[2])
                w_sheet.write(rows, 11, qu[3])
                if province_name == '北京市' or province_name == '天津市' or province_name == '上海市' or province_name == '重庆市':
                    rows += 1
                    print([province_name, province_code, shi[0], shi[1], qu[0], qu[1]])
                else:
                    xian_data = get_location_data(qu[1])
                    if xian_data == -1 or len(xian_data) == 0:
                        print([province_name, province_code, shi[0], shi[1], qu[0], qu[1]])
                        rows += 1
                        continue
                    for xian in xian_data:
                        w_sheet.write(rows, 12, xian[0])
                        w_sheet.write(rows, 13, xian[1])
                        w_sheet.write(rows, 14, xian[2])
                        w_sheet.write(rows, 15, xian[3])
                        print([province_name, province_code, shi[0], shi[1], qu[0], qu[1], xian[0], xian[1]])
                        rows += 1
            w_book.save(r'区域数据.xlsx')




