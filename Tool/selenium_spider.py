from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.baidu.com')
print(driver.title)
print(driver.page_source)
driver.quit()
