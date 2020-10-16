import requests
import json
import csv
from time import sleep
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'mapbaidu.cn',
    'Referer': 'http://mapbaidu.cn/xianwjw/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# with open("hospital.csv", 'a', newline='') as f:
#     row = ['名称', '地址', '发证机构', '床位数', '电话', '等级', '邮政编码', '医院类型', '盈利性', '是否公立', '项目', '科目']
#     write = csv.writer(f)
#     write.writerow(row)
#     print("写入完毕！")


def write_data(data):
    global items
    for item in data:
        # if item['hospital_name'] != '中航工业西安医院':
        #     continue
        code = item['0']
        print(code)
        print(item['hospital_name'])
        res = requests.get(f'http://mapbaidu.cn/xianwjw/php/getDcpType.php?hospital_id={code}', headers=headers)
        try:
            items = json.loads(res.content)
        except:
            print(res.content)
        y = ''
        try:
            for x in items:
                y += str(x['2'] + '|')
        except:
            pass
        with open("hospital.csv", 'a', newline='') as f:
            row = [item['hospital_name'], item['address'], item['authority'], str(item['bednum']) + '床', '029-' + str(item['tel']), str(item['18']) + str(item['19']), item['postcode'], item['4'], item['21'], item['20'], y, item['subject']]
            write = csv.writer(f)
            write.writerow(row)
            print("写入完毕！")


def get_data(i):
    res = requests.get(f'http://mapbaidu.cn/xianwjw/php/getjson.php?category=hospital&pageNum={i}', headers=headers)
    data = json.loads(res.content)
    return data


if __name__ == '__main__':
    for i in range(13, 14):
        print(i)
        data = get_data(i)
        write_data(data)
        # sleep(20)
    # print([{},{},{},{}][2:-1])
