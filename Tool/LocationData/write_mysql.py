import pymysql
import xlrd

db = pymysql.connect('localhost', 'root', '123456', 'location_data')
cursor = db.cursor()

# table = 'location'
sql = """INSERT INTO `location` (`p_name`, `p_ad_code`, `p_lng`, `p_lat`, `s_name`, `s_ad_code`, `s_lng`, `s_lat`, `x_name`, `x_ad_code`, `x_lng`, `x_lat`, `z_name`, `z_ad_code`, `z_lng`, `z_lat`)
 VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");"""

# 读取数据
r_book = xlrd.open_workbook('区域数据.xlsx')
r_sheet = r_book.sheets()[0]
rows = r_sheet.nrows

# print(r_sheet.row_values(3043))
temp_data = []
flag = True
for i in range(28369, 29383):
    row_data = r_sheet.row_values(i)
    if row_data[0] == '' and flag:
        temp_data = r_sheet.row_values(i - 1)[0:12]
        flag = False
    if row_data[0] != '':
        flag = True
    else:
        row_data = temp_data + row_data[12:]
    print(row_data)
    try:
        cursor.execute(sql.format(row_data[0], row_data[1], row_data[2], row_data[3], row_data[4], row_data[5], row_data[6], row_data[7], row_data[8], row_data[9], row_data[10], row_data[11], row_data[12], row_data[13], row_data[14], row_data[15]))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    # print(row_data)
# 110000 120000 310000 500000 # 710000 810000 820000
# try:
#     cursor.execute(sql)
#     db.commit()
# except Exception as e:
#     print(e)
#     db.rollback()