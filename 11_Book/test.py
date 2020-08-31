import xlrd
import xlutils.copy

lines = open('booka.txt', 'r', encoding='utf-8').readlines()

r_book = xlrd.open_workbook('Book.xlsx')
nrows = r_book.sheets()[0].nrows + 1
w_book = xlutils.copy.copy(r_book)
sheet = w_book.get_sheet(0)
for i in range(0, len(lines), 4):
    print(i)
    sheet.write(nrows, 0, lines[i])
    try:
        sheet.write(nrows, 1, lines[i + 1].split('(지은이)')[0])
        sheet.write(nrows, 2, lines[i + 1].split('(지은이)')[1])
    except Exception:
        sheet.write(nrows, 1, lines[i + 1])
    sheet.write(nrows, 3, lines[i+2].split('|')[0])
    sheet.write(nrows, 4, lines[i+2].split('|')[1])
    nrows += 1
w_book.save('Book.xlsx')

# for i in range(0, 1460, 4):
#     print(i)
# s = '김태성(지은이)'
# print(s.split('(지은이)')[1])
