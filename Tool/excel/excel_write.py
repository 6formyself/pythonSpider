import xlwt


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def get_sheet(title):
    f = xlwt.Workbook()
    m_sheet = f.add_sheet(title, cell_overwrite_ok=True)
    row = ["标题", "链接"]
    for i in range(0, len(row)):
        m_sheet.write(0, i, row[i], set_style('Times New Roman', 220, True))
    return m_sheet, f


def write_excel(m_sheet, row_count, row_data):
    print(row_count, row_data)
    for i in range(0, len(row_data)):
        m_sheet.write(row_count, i, row_data[i], set_style('Times New Roman', 220))


def save_file(m_file, title):
    m_file.save(title + '.xlsx')


if __name__ == '__main__':
    sheet, file = get_sheet('需求1')
    write_excel(sheet, 1, ["玉米", "http//：www。baidu。com"])
    save_file(file, '需求1')
