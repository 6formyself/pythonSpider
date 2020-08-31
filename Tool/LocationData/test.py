# import requests
# import json
# url = 'https://apis.map.qq.com/ws/district/v1/getchildren'
# key = 'MKMBZ-5CXCJ-ZQ7FC-KFJ3J-2HYUT-3HBSN'
#
# res = requests.get(url + '?key=' + key)
# json_str = res.content.decode()
# dict_data = json.loads(json_str)
# location_data = dict_data['result'][0]
# print(location_data)
# ['湖北', '海南']
province_info = [
    {'id': '420000', 'name': '湖北', 'fullname': '湖北省', 'pinyin': ['hu', 'bei'], 'location': {'lat': 30.54539, 'lng': 114.34234}},
    {'id': '460000', 'name': '海南', 'fullname': '海南省', 'pinyin': ['hai', 'nan'], 'location': {'lat': 20.01997, 'lng': 110.34863}}]
