from bs4 import BeautifulSoup as Bs4
import os
import xlrd
import uuid
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import xlsxwriter

# 打开并全屏浏览器
country_list = [{'name': 'Oman', 'index': 159}, {'name': 'Russian Federation', 'index': 175},
                {'name': 'United States', 'index': 223},
                {'name': 'Canada', 'index': 36}, {'name': 'Spain', 'index': 199}, {'name': 'France', 'index': 71},
                {'name': 'United Kingdom', 'index': 222}, {'name': 'Netherlands', 'index': 148},
                {'name': 'Israel', 'index': 99},
                {'name': 'Brazil', 'index': 30}, {'name': 'Chile', 'index': 42}, {'name': 'Australia', 'index': 14},
                {'name': 'Ukraine', 'index': 220}, {'name': 'Belarus', 'index': 21}, {'name': 'Japan', 'index': 102},
                {'name': 'Thailand', 'index': 209}, {'name': 'Singapore', 'index': 190},
                {'name': 'Korea', 'index': 108},
                {'name': 'Indonesia', 'index': 96}, {'name': 'Malaysia', 'index': 125},
                {'name': 'Philippines', 'index': 168},
                {'name': 'Vietnam', 'index': 229}, {'name': 'Italy', 'index': 100}, {'name': 'Germany', 'index': 77},
                {'name': 'Saudi Arabia', 'index': 185}, {'name': 'United Arab Emirates', 'index': 221},
                {'name': 'Poland', 'index': 169},
                {'name': 'Turkey', 'index': 215}, {'name': 'Portugal', 'index': 170}]
country_list_single = ['Oman', 'Russian Federation', 'United States', 'Canada', 'Spain', 'France', 'United Kingdom',
                       'Netherlands', 'Israel', 'Brazil', 'Chile', 'Australia', 'Ukraine', 'Belarus', 'Japan', 'Thailand', 'Singapore', 'Korea',
                       'Indonesia', 'Malaysia', 'Philippines', 'Vietnam', 'Italy', 'Germany', 'Saudi Arabia', 'United Arab Emirates',
                       'Poland', 'Turkey', 'Portugal']


def save_image(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'cookie': 'cna=7fldF5D5s3oCAW5Xgh/JPTfz; isg=BBQUw-v1N8woAaMByc2xc5-p5VKGbThXBUqlfa796x3ymZXj1nzb5x1YnZEBYXCv',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38'
    }
    root = './images/'
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        image_name = str(uuid.uuid1()).replace('-', '') + '.' + 'jpg'
        path = root + image_name
        if not os.path.exists(path):
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print("图片保存成功")
        else:
            print("图片已存在")
        return image_name
    except Exception as e:
        print(e)
        print("图片获取失败")


def get_excel1_data(driver):
    # 移动鼠标
    ActionChains(driver).move_to_element(driver.find_element_by_class_name("store-name")).perform()
    sleep(2.5)
    page_source = driver.page_source
    soup = Bs4(page_source, 'lxml')
    bs = soup('div', attrs={"class": "store-dsr-data"})[0].select('b')
    item_as_described = bs[0].text
    communication = bs[1].text
    shipping_speed = bs[2].text

    # 店铺名称
    shop_name = soup('h3', attrs={"class": "store-name"})[0].text
    # 店铺评分
    shop_score = soup('div', attrs={"class": "store-container"})[0].find('i').text
    # 追
    followers = soup('p', attrs={"class": "num-followers"})[0].text.split('Followers')[0].strip()
    # 标题
    try:
        title = soup('h1', attrs={"class": "product-title-text"})[0].text
    except Exception as e:
        print(e)
        print('没有title')
        title = ''
    try:
        review = soup("span", attrs={"class": "product-reviewer-reviews black-link"})[0].text.split('Reviews')[0].strip()
    except Exception as e:
        print(e)
        print('没有review')
        review = ''
    try:
        orders = soup("span", attrs={"class": "product-reviewer-sold"})[0].text.split('orders')[0].strip()
    except Exception as e:
        print(e)
        print('没有orders')
        orders = ''
    try:
        score = soup("span", attrs={"class": "overview-rating-average"})[0].text
    except Exception as e:
        print(e)
        print('没有score')
        score = ''
    # 首图
    first_image = soup("img", attrs={"class": "magnifier-image"})[0].get('src')
    # 爱心
    like = soup("span", attrs={"class": "add-wishlist-num"})[0].text

    driver.execute_script("window.scrollTo(0, 450)")
    sleep(1.5)
    driver.execute_script("document.getElementsByClassName('tab-inner')[6].click()")
    sleep(1.5)
    soup = Bs4(driver.page_source, 'lxml')
    specifications = "".join(list(soup("div", attrs={"class": "product-specs"})[0].stripped_strings))
    # 优惠券
    ActionChains(driver).click(driver.find_element_by_class_name('product-coupon-more')).perform()
    sleep(2)
    soup = Bs4(driver.page_source, 'lxml')
    # 1
    coupon_new = []
    try:
        coupon_new = list(
            soup("div", attrs={"class": "product-coupon-wrap"})[0].stripped_strings)
    except Exception as e:
        print(e)
        print('优惠券获取异常')
    # 2
    coupon_voucher_wrap = []
    # try:
    #     box = soup("div", attrs={"class": "coupon-voucher-wrap"})[0]
    #     coupon_voucher_wrap_1 = box.find_all('div', attrs={"class": "coupon-voucher-tip"})[0].text
    #     coupon_voucher_wrap_2 = box.find_all("div", attrs={"class": "coupon-voucher-price"})[0].text
    #     coupon_voucher_wrap_3 = box.find_all("div", attrs={"class": "coupon-voucher-time two-line-clamp"})[0].text
    #     coupon_voucher_wrap = [coupon_voucher_wrap_1, coupon_voucher_wrap_2, coupon_voucher_wrap_3]
    # except Exception as e:
    #     print(e)
    return {
        "shop_name": shop_name,
        "shop_score": shop_score,
        "followers": followers,
        "title": title,
        "review": review,
        "orders": orders,
        "score": score,
        "first_image": first_image,
        "like": like,
        "specifications": specifications,
        "item_as_described": item_as_described,
        "communication": communication,
        "shipping_speed": shipping_speed,
        "coupon_new": coupon_new,
        "coupon_voucher_wrap": coupon_voucher_wrap
    }


def write_excel1_data(date, link, excel1_sheet, rows, excel_1_data):
    excel1_sheet.write_row(rows, 0, [date, link, excel_1_data['shop_name'], excel_1_data['shop_score'],
                                     excel_1_data['followers'], excel_1_data['item_as_described'],
                                     excel_1_data['communication'], excel_1_data['shipping_speed'],
                                     excel_1_data['title'], excel_1_data['review'], excel_1_data['orders'],
                                     excel_1_data['score'], '', excel_1_data['like'],
                                     excel_1_data['specifications'],
                                     " ".join(excel_1_data['coupon_new'])])
    image = save_image(excel_1_data['first_image'].split('.jpg')[0] + '.jpg')
    excel1_sheet.insert_image('M' + str(rows + 1), './images/' + image,
                              {'x_offset': 5, 'y_offset': 5, 'x_scale': 0.06, 'y_scale': 0.06})


def get_excel2_data(driver):
    soup = Bs4(driver.page_source, 'lxml')
    # 1.运费
    try:
        shipping = soup('div', attrs={"class": "product-shipping-price"})[0].text
        if len(shipping.split('$')) != 1:
            shipping = shipping.split('$')[1]
    except:
        shipping = 'Can not deliver'
    try:
        product_count = len(soup('ul', attrs={"class": "sku-property-list"})[0].select('li'))
    except:
        print('只有一张图')
        product_count = 1
    products = []
    for i in range(0, product_count):
        try:
            image_divs = driver.find_elements_by_class_name('sku-property-image')
            ActionChains(driver).click(image_divs[i]).perform()
            sleep(0.7)
            color = driver.find_element_by_class_name('sku-title-value').get_property('innerText')
            imageUrl = image_divs[i].find_element_by_tag_name('img').get_attribute('src')
        except:
            pass
            color = ''
            imageUrl = ''
        # 颜色，图片，原价，现价，折扣

        rePrice = driver.find_element_by_class_name('product-price-current').find_element_by_class_name(
            'product-price-value').get_property('innerText')
        try:
            nowPrice = driver.find_element_by_class_name('product-price-original').find_element_by_class_name(
                'product-price-del').get_property('innerText')
            sail = driver.find_element_by_class_name('product-price-original').find_element_by_class_name(
                'product-price-mark').get_property('innerText')
        except:
            nowPrice = ''
            sail = ''
        products.append({
            "color": color,
            "imageUrl": imageUrl,
            "rePrice": rePrice,
            "nowPrice": nowPrice,
            "sail": sail
        })
    return {
        "shipping": shipping,
        "products": products
    }


def write_excel2_data(row, date, link, excel2_sheet, excel2_data):
    # [{ "shipping": shipping, "products": products },{ "shipping": shipping, "products": products }]

    temp_row = 0
    # 日期链接
    excel2_sheet.set_row(row, 60)
    excel2_sheet.write_row(row, 0, ['检索日期', '链接'])
    temp_row += 1
    row += 1
    excel2_sheet.set_row(row, 60)
    excel2_sheet.write_row(row, 0, [date, link])
    temp_row += 1
    row += 1
    column = 1
    # 国家
    excel2_sheet.set_row(row, 60)
    excel2_sheet.write_row(row, 0, ['国家'] + country_list_single)
    temp_row += 1
    row += 1
    # 运费
    for i in range(0, len(excel2_data)):
        # =========
        # 一列
        excel2_sheet.set_column(1, 30, 40)
        column_data = []
        for produce in excel2_data[i]['products']:
            column_data.append(excel2_data[i]['shipping'])
            column_data.append(str(produce['color']))
            column_data.append('')
            column_data.append(str(produce['rePrice']))
            column_data.append(str(produce['nowPrice']))
            column_data.append(str(produce['sail']))
            pass
        # print(row, column, column_data)
        excel2_sheet.write_column(row, column, column_data)
        # 图片
        try:
            if i == 0:
                image_row = row + 1
                for j in range(0, len(excel2_data[0]['products'])):
                    excel2_sheet.set_row(image_row + (6 * j), 60)
                    image = save_image(excel2_data[0]['products'][j]['imageUrl'].split('.jpg')[0] + '.jpg')
                    excel2_sheet.insert_image(image_row + (6 * j), column, './images/' + image,
                                              {'x_offset': 5, 'y_offset': 5, 'x_scale': 0.06, 'y_scale': 0.06})
        except:
            print('无图片写入')
        column += 1
    # 最后增加的行数
    temp_row += len(excel2_data[0]['products']) * 5 + 1

    return temp_row


def get_excel3_data(driver):
    comment_data = []
    try:
        driver.execute_script("window.scrollTo(0, 1050)")
        sleep(1)
        driver.execute_script("document.getElementsByClassName('tab-inner')[5].click()")
        sleep(3)
        # 跳转到iframe
        driver.switch_to.frame("product-evaluation")
        sleep(2)
        soup = Bs4(driver.page_source, 'lxml')
        # 评价星数百分比li
        rate_lis = soup('ul', attrs={"class": "rate-list"})[0].find_all("li")
        # star_lis = driver.find_element_by_id('filter_star_list').find_element_by_tag_name('ul').find_elements_by_tag_name('li')
        for i in range(0, 5):
            ActionChains(driver).move_to_element(driver.find_element_by_class_name('fb-star-selector')).perform()
            sleep(1.5)
            star_rate = rate_lis[i].find_all('span', attrs={"class": "r-num fb-star-list-href"})[0].text
            ActionChains(driver).click(
                driver.find_element_by_id('filter_star_list').find_element_by_tag_name('ul').find_elements_by_tag_name(
                    'li')[i + 1].find_element_by_tag_name('a')).perform()
            sleep(2)
            # 评论数据
            soup = Bs4(driver.page_source, 'lxml')
            comment_cons = soup('div', attrs={'class': 'feedback-item clearfix'})
            comment_list = []
            for comment_con in comment_cons:
                user_country = comment_con.find('div', attrs={"class": "fb-user-info"}).find('div', attrs={
                    "class": "user-country"}).find('b').text

                comment_box = comment_con.find('div', attrs={"class": "fb-main"})
                spans = comment_box.find('div', attrs={"class": "user-order-info"}).find_all('span')

                color = logistics = ''
                if list(spans[0].stripped_strings)[0] == "Color:":
                    color = list(spans[0].stripped_strings)[1]
                if list(spans[0].stripped_strings)[0] == "Logistics:":
                    logistics = list(spans[0].stripped_strings)[1]
                if len(spans) == 2:
                    if list(spans[1].stripped_strings)[0] == "Color:":
                        color = list(spans[1].stripped_strings)[1]
                    if list(spans[1].stripped_strings)[0] == "Logistics:":
                        logistics = list(spans[1].stripped_strings)[1]

                buyer_review = comment_box.find('div', attrs={"class": "f-content"}).find('dl',
                                                                                          attrs={
                                                                                              "class": "buyer-review"})

                comment_time_span = buyer_review.find('dt', attrs={"class": "buyer-feedback"}).find_all('span')
                comment_text = comment_time_span[0].text.strip()
                comment_time = comment_time_span[1].text.strip()

                images_url = []
                try:
                    images = buyer_review.find('dd', attrs={"class": "r-photo-list"}).select('img')
                    for image in images:
                        images_url.append(image.get('src'))
                except:
                    pass

                comment_list.append({
                    "user_country": user_country,
                    "color": color,
                    "logistics": logistics,
                    "comment_text": comment_text,
                    "comment_time": comment_time,
                    "images_url": images_url
                })
            comment_data.append({
                "star_rate": star_rate,
                "comment": comment_list
            })
    except Exception as e:
        print(e)
        print('没有评论数据')
        comment_data = []
    driver.switch_to.default_content()
    return comment_data


def write_excel3_data(row, date, link, title, shop_name, review, order, score, excel3_sheet, excel3_data):
    if not excel3_data:
        return 0
    add_row = 0
    # 店铺信息
    excel3_sheet.set_row(row, 60)
    excel3_sheet.write_row(row, 0, ['检索日期', '链接', '标题', '店铺名', 'Review', 'order', '评分'])
    row += 1
    add_row += 1
    excel3_sheet.set_row(row, 60)
    excel3_sheet.write_row(row, 0, [date, link, title, shop_name, review, order, score])
    row += 1
    add_row += 1
    # 评论信息
    for i in range(1, 6):
        excel3_sheet.set_row(row, 60)
        excel3_sheet.write_row(row, 0, [str(6 - i) + ' Stars', excel3_data[i - 1]['star_rate']])
        row += 1
        add_row += 1
        excel3_sheet.set_row(row, 60)
        excel3_sheet.write_row(row, 0, ['国家', '评价', 'Logistics', 'Color', '评价时间', '图片'])
        row += 1
        add_row += 1
        # 写评论
        for comment in excel3_data[i - 1]['comment']:
            excel3_sheet.set_row(row, 60)
            excel3_sheet.write_row(row, 0, [comment['user_country'], comment['comment_text'], comment['logistics'],
                                            comment['color'], comment['comment_time'], ''])
            # 下载图片
            if len(comment['images_url']) > 0:
                image_name = save_image(comment['images_url'][0])
                excel3_sheet.set_row(row, 60)
                excel3_sheet.insert_image('F' + str(row + 1), './images/' + image_name,
                                          {'x_offset': 5, 'y_offset': 5, 'x_scale': 0.06, 'y_scale': 0.06})
            row += 1
            add_row += 1
    return add_row


def exchange_country(name, index, driver):
    print(name)
    driver.execute_script("window.scrollTo(0, 0)")
    sleep(1.5)
    try:
        ActionChains(driver).click(driver.find_element_by_id('switcher-info')).perform()
    except Exception as e:
        print(e)
        sleep(5)
        ActionChains(driver).click(driver.find_element_by_id('switcher-info')).perform()
    sleep(3)
    # address-select-trigger
    ActionChains(driver).click(driver.find_element_by_class_name('address-select-trigger')).perform()
    sleep(1)
    # 点击输入框
    ActionChains(driver).click(driver.find_element_by_class_name('filter-input')).perform()
    sleep(1)
    # 输入国家
    driver.find_element_by_class_name("filter-input").send_keys(name)
    sleep(1)
    ActionChains(driver).click(driver.find_elements_by_class_name('address-select-item')[index]).perform()
    sleep(3.5)
    # 点击语言
    print('点击语言')
    ActionChains(driver).click(driver.find_element_by_class_name('select-item')).perform()
    sleep(1.5)
    ActionChains(driver).click(driver.find_element_by_class_name('switcher-item')).perform()
    sleep(1)
    # 点击货币
    print('点击货币')
    ActionChains(driver).click(driver.find_elements_by_class_name('select-item')[1]).perform()
    sleep(1.5)
    ActionChains(driver).click(
        driver.find_elements_by_class_name('notranslate')[3].find_element_by_tag_name('li').find_element_by_tag_name(
            'a')).perform()

    print('点击save')
    sleep(1)
    ActionChains(driver).click(driver.find_element_by_class_name('go-contiune-btn')).perform()
    sleep(12)


def spider_main():
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    # 1.读取所有链接数据
    work_book = xlrd.open_workbook(r'link.xls')
    sheet = work_book.sheets()[0]
    shop_links = sheet.col_values(1)[1:]
    search_date = sheet.col_values(0)[1:]
    # excel1表格
    excel1 = xlsxwriter.Workbook('excel1.xlsx')
    excel1_sheet = excel1.add_worksheet()
    excel1_sheet.set_row(0, 30)
    excel1_sheet.write_row(0, 0, ['检索日期', '链接', '店铺名', '店铺综合评分', 'Followers', 'Item as Described',
                                  'Communication', 'Shipping Speed', '标题 ', 'Review', 'order', '评分', '首图',
                                  '喜欢', 'SPECIFICATIONS', 'Get coupons'])
    # excel3
    excel3 = xlsxwriter.Workbook('excel3.xlsx')
    excel3_sheet = excel3.add_worksheet()
    # excel
    excel2 = xlsxwriter.Workbook('excel2.xlsx')
    excel2_sheet = excel2.add_worksheet()

    # 遍历链接
    excel3_row = 0
    excel2_row = 0
    for i in range(0, len(shop_links)):
        print('链接：' + shop_links[i])
        driver.get(shop_links[i])
        # driver.maximize_window()
        sleep(2)
        try:
            # 2.获取每个链接的excel1数据
            try:
                excel_1_data = get_excel1_data(driver)
            except Exception as e:
                print(e)
                print('excel1 数据获取异常')
                excel_1_data = {}
            excel1_sheet.set_row(i + 1, 60)
            print(excel_1_data)
            write_excel1_data(search_date[i], shop_links[i], excel1_sheet, i + 1, excel_1_data)
            # 3.获取每个链接的excel3数据
            try:
                excel_3_data = get_excel3_data(driver)
            except Exception as e:
                print(e)
                print('excel3 数据获取异常')
                excel_3_data = {}
            print(excel_3_data)
            excel3_add_row = write_excel3_data(excel3_row, search_date[i], shop_links[i], excel_1_data['title'],
                                               excel_1_data['shop_name'],
                                               excel_1_data['review'], excel_1_data['orders'], excel_1_data['score'],
                                               excel3_sheet, excel_3_data)
            excel3_row += excel3_add_row
        except Exception as e:
            print(e)
            print('excel1 and excel3 写入异常')
            # excel1.close()
            # excel3.close()
            # raise e

        # 4.遍历29个国家，获取29个国家商品数据
        excel2_data = []
        for item in country_list:
            # 切换国家
            try:
                exchange_country(item['name'], item['index'], driver)
                single_country_data = get_excel2_data(driver)
                print(single_country_data)
                excel2_data.append(single_country_data)
            except Exception as e:
                print(e)
                print('组装产品数据excel2_data异常')
                with open('excel2.json', 'a', encoding='utf-8') as f:
                    f.write(str(excel2_data))
        # 写入excel2_data { "shipping": shipping, "products": products }
        try:
            temp_row = write_excel2_data(excel2_row, search_date[i], shop_links[i], excel2_sheet, excel2_data)
            excel2_row += temp_row
        except Exception as e:
            print(e)
            print('excel2 写入异常')
            excel2.close()
    excel1.close()
    excel3.close()
    excel2.close()


if __name__ == "__main__":
    spider_main()
    # url = 'https://www.aliexpress.com/item/32995907155.html?spm=a2g0o.store_home.productList_8569852.pic_5'
    # driver = webdriver.Chrome(executable_path='chromedriver.exe')
    # driver.get(url)
    # sleep(2)
    # print(get_excel2_data(driver))
