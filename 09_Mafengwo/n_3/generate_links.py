file = open('links.txt', 'a')
a = 'https://you.ctrip.com/travels/Xiamen21/t3-p{}.html'

for i in range(2, 1807):
    file.write(a.format(i) + '\n')
file.close()