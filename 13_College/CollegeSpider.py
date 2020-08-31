# -*- coding:utf-8 -*-
import requests
import time
import json
import csv
import os
import pandas as pd
import numpy as np
import hashlib
import re

numcount = 0
recold_state = False


def Spider(page_num):
    url_Index = r"https://api.eol.cn/gkcx/api/"
    header = {
        'Host': 'api.eol.cn',
        'Connection': 'keep-alive',
        'Content-Length': '268',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://gkcx.eol.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://gkcx.eol.cn/school/search',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }
    for page in range(page_num, 148):
        data = {"access_token": "", "admissions": "", "central": "", "department": "", "dual_class": "", "f211": "",
                "f985": "", "is_dual_class": "", "keyword": "", "page": page, "province_id": "", "request_type": 1,
                "school_type": "", "size": 20, "sort": "view_total", "type": "", "uri": "apigkcx/api/school/hotlists"}
        response_Index = requests.post(url_Index, headers=header, json=data)
        # print(response_Index.status_code)
        # print(response_Index.text)
        # print(type(response_Index.text))
        with open("./recold.txt", "a") as f:
            f.write(str(page) + ",")

        data_json = json.loads(response_Index.text)
        school_list = data_json["data"]["item"]
        print(school_list)
        for item in school_list:
            print(item["name"])
            print(item["school_id"])
            getInfo(item["name"], item["school_id"])


def getInfo(schoolname, school_id):
    header = {
        'Host': 'static-data.eol.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://gkcx.eol.cn',
        'Connection': 'keep-alive',
    }
    url = r"https://static-data.eol.cn/www/2.0/school/" + str(school_id) + r"/dic/specialplan.json"
    response_Info = requests.get(url, headers=header)
    # print(response_Info.text)
    try:
        response_json = json.loads(response_Info.text)
        # print(response_json["data"]["data"])
        info_lsit = response_json["data"]["data"]
        for item in info_lsit:
            years = item["year"]
            # print(years)
            if years == 2019:
                # print(item["province"])
                Handel_info(item["province"], school_id, years, schoolname)
            elif years == 2018:
                # print(item["province"])
                Handel_info(item["province"], school_id, years, schoolname)
            elif years == 2017:
                # print(item["province"])
                Handel_info(item["province"], school_id, years, schoolname)
        time.sleep(2)
    except:
        pass


def Handel_info(items, shoolid, years, schoolname):
    province = {
        11: "北京",
        12: "天津",
        13: "河北",
        14: "山西",
        15: "内蒙古",
        21: "辽宁",
        22: "吉林",
        23: "黑龙江",
        31: "上海",
        32: "江苏",
        33: "浙江",
        34: "安徽",
        35: "福建",
        36: "江西",
        37: "山东",
        41: "河南",
        42: "湖北",
        43: "湖南",
        44: "广东",
        45: "广西",
        46: "海南",
        50: "重庆",
        51: "四川",
        52: "贵州",
        53: "云南",
        54: "西藏",
        61: "陕西",
        62: "甘肃",
        63: "青海",
        64: "宁夏",
        65: "新疆",
        71: "香港",
        81: "澳门",
        82: "台湾",
        99: "其他",
        100: "不分省",
    }
    project_type = {1: "理科", 2: "文科"}
    li_url = []
    page = 1
    url = r"https://static-data.eol.cn/www/2.0/schoolplanindex/"
    for item in items:
        pid = item["pid"]
        stdent_type = item["type"]
        batch = item["batch"]
        provinName = province[pid]

        for ty in stdent_type:
            for bat in batch:
                if ty == 1 or ty == 2:
                    projectName = project_type[ty]
                    pid_ty_bat = url + str(years) + r"/" + str(shoolid) + r"/" + str(pid) + r"/" + str(ty) + r"/" + str(
                        bat) + r"/" + str(page) + ".json" + "=" + provinName + "=" + projectName
                    li_url.append(pid_ty_bat)
    print(li_url)
    HandelRequest(li_url, years, schoolname)


def HandelRequest(li_url, years, schoolname):
    header = {
        'Host': 'static-data.eol.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://gkcx.eol.cn',
        'Connection': 'keep-alive',
    }
    for url in li_url:
        new_url = url.split("=")

        with open("./recoldurl.txt", "r") as f:
            line = f.readlines()
            if new_url[0] + '\n' in line:
                print("有重复url.....")
                continue
            else:
                global recold_state
                if recold_state == False:
                    recold_state = True
                    try:
                        recold_endUrl = line[-1].strip('\n')
                        data = requests.get(recold_endUrl, headers=header)
                        numFou = json.loads(data.text)["data"]["numFound"]
                        page_recold = numFou / 10
                        if page_recold > 1:
                            Handel_SonPage(header, page_recold, recold_endUrl, schoolname, new_url[1], new_url[2],
                                           years)
                    except:
                        pass

        deatil_response = requests.get(new_url[0], headers=header)
        with open("./recoldurl.txt", "a") as f:
            f.write(new_url[0] + '\n')

        # deatain_info = deatil_response.text.encode('utf-8').decode('unicode_escape')
        deatain_info = deatil_response.text
        deatain_info_json = json.loads(deatain_info)
        # print(deatain_info_json["data"])
        try:
            print(deatain_info, new_url[0])
            numFound = deatain_info_json["data"]["numFound"]
        except:
            continue
        print(numFound)

        pages = numFound / 10
        deatain_data = deatain_info_json["data"]["item"]
        HandelEndData(deatain_data, schoolname, new_url[1], new_url[2], years)
        # time.sleep(1)
        if pages > 1:
            Handel_SonPage(header, pages, new_url[0], schoolname, new_url[1], new_url[2], years)


def Handel_SonPage(header, pages, new_url0, schoolname, new_url1, new_url2, years):
    for pagenum in range(2, int(pages) + 2):
        page_url = new_url0
        end_url = re.sub(r'(\d+).json', str(pagenum), page_url) + ".json"

        with open("./recoldurl.txt", "r") as f:
            line = f.readlines()
            if end_url + '\n' in line:
                print("有重复url.....")
                continue

        resopnse = requests.get(end_url, headers=header)
        with open("./recoldurl.txt", "a") as f:
            f.write(end_url + '\n')

        # data_utf8 = resopnse.text.encode('utf-8').decode('unicode_escape')
        data_utf8 = resopnse.text
        print(data_utf8, end_url)
        try:
            data_json = json.loads(data_utf8)["data"]["item"]
        except:
            continue
        HandelEndData(data_json, schoolname, new_url1, new_url2, years)
        # time.sleep(1)


def HandelEndData(deatain_data, schoolname, new_url1, new_url2, years):
    for item in deatain_data:
        school_name = schoolname
        provinceName = new_url1
        projectName = new_url2
        year = years
        try:
            local_batch_name = item["local_batch_name"]
            spname = item["spname"]
            level2_name = item["level2_name"]
            level3_name = item["level3_name"]
            num = item["num"]
            zslx = "-"
        except Exception as e:
            continue
        # print([school_name, provinceName, projectName, year, local_batch_name, spname, level2_name, level3_name, num,zslx])
        li_data = [school_name, provinceName, projectName, year, local_batch_name, spname, level2_name, level3_name,
                   num, zslx]

        with open('./招生.csv', 'a', newline="", encoding="gb18030") as f:
            w = csv.writer(f)
            w.writerow(li_data)
        # df.to_csv("./test.csv", index=False, mode="a")
        global numcount
        numcount += 1
        print("当前数据量：" + str(numcount))


if __name__ == "__main__":
    columns = ['学校', '地区', '文理', '年份', '批次', '专业', '学科门类', '专业类', '招生数', '学制']
    if not os.path.exists('./test.csv'):
        with open('./test.csv', 'a', newline="", encoding="gb18030") as f:
            w = csv.writer(f)
            w.writerow(columns)
    if not os.path.exists('./recoldurl.txt'):
        f = open("./recoldurl.txt", "a")
        f.close()

    if os.path.exists('./recold.txt'):
        with open('./recold.txt') as f:
            list_num = f.readline().split(',')
            page_num = int(list_num[-2])
            Spider(page_num)
    else:
        Spider(1)

# os.system('python C:/Users/Administrator/PycharmProjects/untitled/FreeSpider/CollegeSpider.py')
