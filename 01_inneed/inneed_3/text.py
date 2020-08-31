file = open('link.txt', 'a')
head = 'http://www.chinagrain.cn/liangyou_secondeproduct_next.htm?pageno='
end = '&xumuurl=yumi&newstype=&title=%E7%8E%89%E7%B1%B3%E4%BB%B7%E6%A0%BC%E8%A1%8C%E6%83%85%E5%88%86%E6%9E%90%E9%A2%84%E6%B5%8B&type=&key=&newsnum=&producttype=1061'
for i in range(1, 5000):
    file.write(head + str(i) + end + '\n')
file.close()