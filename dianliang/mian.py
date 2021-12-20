import xlrd
from datetime import datetime
import os
import xlwt

"""
读取一组excel表格，把表格内时间按照指定时段分组，然后按照指定公式逐行运算每组后求和运算结果，最后输出汇总表格。
如A表格内现有0:00-23:59时段内所有温度，然后需要按照
0:00-0:29 | 0:30-6:59 | 7:00-7:59 | 8:00-12:29 | 12:30-15:59 | 16:00-19:59 | 20:00-23:59分七组时段。

拆分后每组时段逐行运行SUM(B5:G5)公式。然后对逐行结果求和。
最后输出汇总excel表格。
"""


def read_xlsx(name):
    """读取xlsx"""
    work_book = xlrd.open_workbook(name)
    sheets = work_book.sheets()
    return sheets[0]

    
if __name__ == "__main__":
    file_list = os.listdir('excel')

    final_excel = xlwt.Workbook()
    final_sheet = final_excel.add_sheet('汇总', cell_overwrite_ok=True)
    row = 0

    for file_name in file_list:
        city_name = file_name.split('.')[0]

        sheet = read_xlsx(r"excel/" + file_name)
        print(sheet.nrows, sheet.ncols)

        data = []
        final_data = [] # 汇总数据
        for row_index in range(1, sheet.nrows):
            temp = sheet.row_values(row_index)
            date = datetime.strptime(temp[0], "%Y-%m-%d %H:%M:%S")
            temp.pop(0)
            temp.insert(0, date.minute)
            temp.insert(0, date.hour)
            data.append(temp)

        # 分时间段进行统计
        date_slice = [
            [0, 0, 0, 29],
            [0, 30, 6, 59],
            [7, 0, 7, 59],
            [8, 0, 12, 29],
            [12, 30, 15, 59],
            [16, 0, 19, 59],
            [20, 0, 23, 59],
        ]
        # 1, 0:00-0:29
        excel_data = [city_name]
        for item in date_slice:
            sub_list = [el for el in data if item[0] <= el[0] <= item[2] and item[1] <= el[1] <= item[3]]
            value = 0
            for data_item in sub_list:
                value = value + sum(data_item[2:])*225/1000/60
            print(value)
            excel_data.append(value)
        # 写数据
        print(excel_data)
        for i in range(0, len(excel_data)):
            final_sheet.write(row, i, excel_data[i])
        row += 1
    final_excel.save('汇总.xlsx')
