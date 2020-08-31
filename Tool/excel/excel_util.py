# 读，写，追加
import xlrd
import xlwt
import xlutils.copy


def set_style(font_name, height, bold=False):
    """设置单元格字体样式"""
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = font_name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def write_xlsx():
    """写xlsx"""
    work_book_2 = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = work_book_2.add_sheet('sheet1', cell_overwrite_ok=True)
    data = [
        ['姓名', '年龄', '性别'],
        ['张三', '12', '男'],
        ['李四', '13', '女']
    ]
    for i in range(0, len(data)):
        for j in range(0, len(data[i])):
            sheet.write(i, j, data[i][j], set_style('Times New Roman', 220, True))
    work_book_2.save(r'test2.xlsx')


def read_xlsx():
    """读取xlsx"""
    work_book = xlrd.open_workbook(r'test.xlsx')
    sheets = work_book.sheets()
    sheet_1 = sheets[0]
    # 打印出行数和列数以及一行和一列的数据
    print(sheet_1.nrows, sheet_1.ncols)
    print(sheet_1.row_values(1))
    print(sheet_1.col_values(1))
    # 打印单元格数据,第0行第1列的数据
    print(sheet_1.row(0)[1].value)
    print(sheet_1.cell_value(0, 1))


if __name__ == '__main__':
    # 追加
    tar_work_book = xlrd.open_workbook(r'test2.xlsx')
    work_book = xlutils.copy.copy(tar_work_book)
    sheet = work_book.get_sheet(0)
    sheet.write(4, 0, '王nm')
    sheet.write(4, 1, '12')
    sheet.write(4, 2, '男')
    work_book.save('test2.xlsx')
