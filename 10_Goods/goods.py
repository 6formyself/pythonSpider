import requests
import json
import time
import os
import xlwt


def save_image(path, url, i):
    d = path + '/' + str(i + 1) + '.' + url.split('/')[-1].split('.')[-1]
    print(d)
    try:
        if not os.path.exists(d):
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            with open(d, 'wb') as f:
                f.write(r.content)
                f.close()
                print("图片保存成功")
        else:
            print("图片已存在")
    except Exception as e:
        print(e)
        print("图片获取失败")


# 获取登陆凭证
a = 'https://wx-akc.hcarm.com/admin/v1/admin/login'
data = {
    'password': 'e10adc3949ba59abbe56e057f20f883e',
    'user_name': 'hz_akc'
}
res = requests.post(a, data=data)
print(json.loads(res.content)['data']['token'])

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Authorization': str(json.loads(res.content)['data']['token']),
    'Connection': 'keep-alive',
    'Host': 'wx-akc.hcarm.com',
    'Referer': 'https://wx-akc.hcarm.com/system/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}
head_url = 'https://wx-akc.hcarm.com/admin/v2/akc/'
# 获取分类api
category_api = 'getFrontCatList'
# 获取活动api，传入分类id
activity_api = 'getActivityList?front_cat_id={}&show_all=1'
# 获取商品api，传入页数和活动id
goods_api = 'getGoodsList?page={}&page_size=200&goods_name=&start_time=&end_time=&is_add_to_goods=&live_id={}'
# 获取商品详细信息api，传入goods_id
detail_api = 'getGoodsInfo?goods_id={}'
sheet_title = ['商品名称', '活动名称', '品牌', '开始时间', '结束时间', '标签价', '建议零售价', '成本价', '利润', '描述']

# 1-----遍历分类：
category_res = requests.get(head_url + category_api, headers=headers, timeout=10)
print(category_res.content)
category_list = json.loads(category_res.content.decode())['data']['list'][::-1]
for category in category_list:
    # 分类名称
    category_name = category['cat_name']
    print('分类：' + category_name)
    # 2-----遍历活动
    activity_res = requests.get(head_url + activity_api.format(category['cat_id']), headers=headers, timeout=10)
    dict_data = json.loads(activity_res.content.decode())['data']
    # 活动列表和商品数量
    activity_list = dict_data['list'][::-1]
    for activity in activity_list:
        # 活动名称，id
        activity_name = activity['name'].replace('.', '').replace('<', '').replace('>', '').replace('/', '').replace('\\', '').replace('|', '').replace(':', '').replace('*', '').replace('?', '')
        activity_id = activity['id']
        # 跳过过期的活动
        end_time = int(time.mktime(time.strptime(activity['end_time'], "%Y-%m-%d %H:%M:%S")))
        current_time = round(time.time())
        if end_time < current_time:
            print('活动：' + activity_name + '--------过期！')
            continue
        print('活动：' + activity_name)
        if not os.path.exists('爱库存'):
            os.mkdir('爱库存')
        path = '爱库存/' + category_name
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception:
                continue
        path += '/' + activity_name
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception:
                continue
        else:
            continue
        path += '/'
        work_book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = work_book.add_sheet('sheet0', cell_overwrite_ok=True)
        for i in range(0, len(sheet_title)):
            sheet.write(0, i, sheet_title[i])
        # 3-----查询商品
        j = 1
        i = 1
        while True:
            try:
                goods_res = requests.get(head_url + goods_api.format(i, activity_id), headers=headers, timeout=10)
            except Exception as e:
                print('请求商品列表超时！！！！ 正在处理。。。')
                try:
                    goods_res = requests.get(head_url + goods_api.format(i, activity_id), headers=headers, timeout=10)
                except Exception as e:
                    print('处理失败！！当前位置：' + category_name + '/' + activity_name)
                    continue
            goods_list = json.loads(goods_res.content.decode())['data']['list']
            goods_count = int(json.loads(goods_res.content.decode())['data']['total'])
            if (i - 1) * 200 >= goods_count:
                break
            # 4-----查询商品详细信息
            for goods in goods_list:
                try:
                    detail_res = requests.get(head_url + detail_api.format(goods['goods_id']), headers=headers, timeout=10)
                except Exception:
                    print('请求商品信息超时！！！！ 正在处理。。。')
                    try:
                        detail_res = requests.get(head_url + detail_api.format(goods['goods_id']), headers=headers, timeout=10)
                    except Exception as e:
                        print('处理失败！！当前位置：' + category_name + '/' + activity_name + '/' + goods['goods_id'])
                        continue
                dict_data = json.loads(detail_res.content.decode('utf-8').replace('\\/', '/')[17:-10])
                goods_name = dict_data['goods_name'].replace('.', '').replace('<', '').replace('>', '').replace('/', '').replace('\\', '').replace('|', '').replace(':', '').replace('*', '').replace('?', '')
                print('商品：' + goods_name)
                sheet.write(j, 0, dict_data['goods_name'])
                sheet.write(j, 1, activity_name)
                sheet.write(j, 2, dict_data['brand'])
                sheet.write(j, 3, dict_data['start_time'])
                sheet.write(j, 4, dict_data['end_time'])
                sheet.write(j, 5, dict_data['tag_price'])
                sheet.write(j, 6, dict_data['price'])
                sheet.write(j, 7, dict_data['settlement_price'])
                sheet.write(j, 8, dict_data['profit'])
                sheet.write(j, 9, dict_data['description'])
                if not os.path.exists(path + goods_name):
                    try:
                        os.mkdir(path + goods_name)
                    except Exception as e:
                        print('商品名称有误！！')
                        continue
                else:
                    continue
                j += 1
                for i in range(0, len(dict_data['picture'])):
                    save_image(path + goods_name, dict_data['picture'][i], i)
            i += 1
        print(path + activity_name + '.xlsx')
        work_book.save(path + activity_name + '.xlsx')
        time.sleep(3)
