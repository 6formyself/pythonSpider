import csv

with open("test.csv") as f:
    reader = csv.reader(f)
    # rows = [row for row in reader]
    # print(rows[0])
    print(len(list(reader)))

with open("test.csv", 'a', newline='') as f:
    row = ['曹操', '23', '学生', '黑龙江', '5000', '23', '学生', '黑龙江', '5000']
    write = csv.writer(f)
    write.writerow(row)
    print("写入完毕！")