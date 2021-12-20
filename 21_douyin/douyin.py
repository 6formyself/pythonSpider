from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import csv
# 启动浏览器
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://fxg.jinritemai.com/login')

print('请安如下步骤进行初始化操作：')
print('1.登录抖店后台')
print('2.进入达人广场页面')
print('3.选择类目')
input('操作完毕请输入：1，并按回车\n')

# 读取话术
huashu_file = open('huashu.txt')
huashu_lines = huashu_file.readlines()
huashu = ''.join(huashu_lines)
print('加载到话术：')
print(huashu)

driver.maximize_window()
driver.switch_to.window(driver.window_handles[1])
sleep(3)
# 达人列表容器累名
daren_card_class = 'daren-card'
# 每个类目25页达人
pages_per_category = 25
# 在线沟通按钮
online_concat_class = 'contact-btn--im'
# 15659023280


def spider_main():
    count = 1
    with open("daren-" + time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time())) + ".csv", 'a', newline='', encoding='utf-8-sig') as csv_f:
        csv_write = csv.writer(csv_f)
        csv_write.writerow(['序号', '达人信息'])

        for pages in range(1, 25):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            # 1.获取达人列表
            daren_cards = driver.find_elements_by_class_name(daren_card_class)
            # 2.遍历达人
            for daren in daren_cards:
                # 写入信息
                csv_write.writerow([str(count), daren.get_attribute("textContent")])
                count += 1

                driver.execute_script("arguments[0].scrollIntoView(false);", daren)
                print('1.点击达人卡片')
                daren.click()
                sleep(6)
                driver.switch_to.window(driver.window_handles[-1])
                print('2.点击在线沟通')
                driver.find_element_by_class_name(online_concat_class).click()
                sleep(1)
                if len(driver.window_handles) == 4:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[1])
                else:
                    sleep(6)
                    if len(driver.find_elements_by_class_name('chatd-message')) == 0:
                        driver.switch_to.window(driver.window_handles[-1])
                        print('3.输入话术')
                        driver.find_elements_by_tag_name('textarea')[0].send_keys(huashu, Keys.ENTER)
                        sleep(2)
                        print('4.关闭窗口')
                        driver.close()
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.close()
                        driver.switch_to.window(driver.window_handles[1])
            print('5.下一页')
            next_page = driver.find_element_by_class_name('ant-pagination-next')
            driver.execute_script("arguments[0].scrollIntoView(false);", next_page)
            next_page.click()
            sleep(4)


if __name__ == "__main__":
    spider_main()
