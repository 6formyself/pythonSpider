from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://hotels.ctrip.com/hotels/list?city=25&checkin=2020/12/22&checkout=2020/12/23&optionId=25&optionType=City&directSearch=0&display=%E5%8E%A6%E9%97%A8&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&')
driver.maximize_window()

# 退出登录
ActionChains(driver).click(driver.find_element_by_id('lg_loginbox').find_element_by_tag_name('a')).perform()

# driver.execute_script('window.scrollTo(0,20000);')

detail_xpath = '//*[@id="ibu_hotel_container"]/div/section/div[2]/ul/li[{}]/div/div/div/div[2]/div[2]/div[2]'
more_xpath = '//*[@id="ibu_hotel_container"]/div/section/div[2]/ul/div[2]/p/span'
# ActionChains(driver).click(driver.find_element_by_xpath(xpath.format(4))).perform()
# ActionChains(driver).move_to_element(driver.find_element_by_xpath(detail_xpath.format(4))).click().perform()
# ActionChains(driver).move_to_element(driver.find_element_by_xpath(detail_xpath.format(4))).click().perform()
while 1:
    driver.execute_script('window.scrollTo(0,20000000);')
    sleep(2)
    try:
        ActionChains(driver).click(driver.find_element_by_xpath(more_xpath)).perform()
        sleep(2)
    except Exception as e:
        print(e)
