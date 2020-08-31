from bs4 import BeautifulSoup as Bs4
test = open('test.txt')
ls = test.readlines()
a = ''
for l in ls:
    a += l
soup = Bs4(a, 'lxml')
sa = list(soup('h3', attrs={'class': 'topSpacing w30'})[0].stripped_strings)[0].split('of')[1].strip()
print(sa)
# text.split('of')[1]