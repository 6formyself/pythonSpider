import requests
from bs4 import BeautifulSoup as Bs4
import xlrd
import xlutils.copy

head_url = 'https://www.qixin.com'
url = 'https://www.qixin.com/search?key={}&page=1'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cookie': 'acw_tc=76b20f4415974934489006279e9e242675c3a810664cf04959ca906a999c08; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1597493450; cookieShowLoginTip=3; sid=s%3AhTl2LRA8C98d1Of7AbZ3Qqt49Xq9GaO0.NkoGBCEzrD6b129fg3ZjM9wS628pL84CbYfSVkezNNU; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1597498749',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'
}

test_company = '洞头华夏阀门有限公司'


def get_company_title_link(company_name):
    """根据企业名称获取详情链接"""
    res = requests.get(url.format(company_name), headers=header)
    # 可能包含验证码从而抛出异常
    soup_simple = Bs4(res.text, 'lxml')
    detail_link = soup_simple('div', attrs={'class': 'company-title'})[0].select('a')[0].get('href')
    return head_url + detail_link


def get_company_detail_info(title_link):
    """获取企业详细信息"""
    res = requests.get(title_link, headers=header)
    detail_soup = Bs4(res.text, 'lxml')
    # 企业状态
    company_state_span = detail_soup('span', attrs={'class': 'head-tag'})[0]
    company_state = company_state_span.text
    data_content_soup = Bs4(company_state_span.get('data-content'), 'lxml')
    gong_shi = list(data_content_soup.stripped_strings)[1]
    shi_yi = '-'
    try:
        shi_yi = list(data_content_soup.stripped_strings)[3]
    except Exception as e:
        pass
    gu_dong_list = []
    # 发起人/股东	认缴出资	实缴出资	备注
    try:
        trs = detail_soup('div', id='partners')[0].select('table')[0].select('tbody')[0].select('tr')
    except Exception as e:
        print('该企业没有股东数据')
        gu_dong_list.append(['-', '-', '-', '-'])
        return [company_state, gong_shi, shi_yi, gu_dong_list]
    for tr in trs:
        tds = tr.select('td')
        gu_dong = tds[1].text
        ren_jiao = tds[2].text
        shi_jiao = tds[3].text
        bei_zhu = '无'
        try:
            r = requests.get(head_url + tds[1].select('a')[0].get('href'), headers=header)
            rsoup = Bs4(r.text, 'lxml')
            tag_box = rsoup('div', attrs={'class': 'tags-box'})[0]
            if len(tag_box.select('span')) != 0:
                bei_zhu = tag_box.select('span')[0].text
        except Exception as e:
            pass
        gu_dong_list.append([gu_dong, ren_jiao, shi_jiao, bei_zhu])
    return [company_state, gong_shi, shi_yi, gu_dong_list]


if __name__ == '__main__':
    # 读取excel
    read_book = xlrd.open_workbook(r'企业数据.xlsx')
    nrows = read_book.sheets()[0].nrows
    work_book = xlutils.copy.copy(read_book)
    sheet = work_book.get_sheet(0)

    # 读取企业名称
    company_file = open('company.txt')
    company_lines = company_file.readlines()
    company_lines = list(set(company_lines))
    file = open('re.txt', 'a')
    file.writelines(company_lines)
    file.close()

    for company in company_lines:
        try:
            title_link = get_company_title_link(company[0:-1])
        except Exception as e:
            print('第一种错误：' + str(e))
            print('网页出现问题！请前往（https://www.qixin.com/search?key=' + company[0:-1] + '）确认，如需要验证请验证完毕请输入1并回车，如查询不到请输入2并回车：')
            error_type = input()
            title_link = None
            if error_type == '1':
                title_link = get_company_title_link(company[0:-1])
            if error_type == '2':
                continue
        print(company[0:-1] + ':' + title_link)
        try:
            data = get_company_detail_info(title_link)
        except Exception as e:
            print('第二种错误：' + str(e))
            print('网站出现第二种验证，复制当前链接前往验证，验证完毕请输入2并回车：')
            input()
            data = get_company_detail_info(title_link)
        print(data)
        sheet.write(nrows, 1, company)
        sheet.write(nrows, 2, data[0])
        sheet.write(nrows, 3, data[1])
        sheet.write(nrows, 4, data[2])
        flag = False
        # 写入股东信息
        for item in data[3]:
            sheet.write(nrows, 5, item[0])
            sheet.write(nrows, 6, item[1])
            sheet.write(nrows, 7, item[2])
            sheet.write(nrows, 8, item[3])
            nrows += 1
            flag = True
        if not flag:
            nrows += 1
        work_book.save('企业数据.xlsx')
    company_file.close()
    work_book.save('企业数据.xlsx')