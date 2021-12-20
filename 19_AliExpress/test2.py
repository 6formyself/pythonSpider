import xlsxwriter

excel2 = xlsxwriter.Workbook('excel2.xlsx')
excel2_sheet = excel2.add_worksheet()
excel2_sheet.set_column(1, 30, 60)
excel2_sheet.set_row(1, 30)
excel2_sheet.write_column(0, 0, ['Beige', '', 'US $12.45', 'US $13.99', '-11%', 'Black', '', 'US $35.59', 'US $39.99', '-11%', 'Blue', '', 'US $37.37', 'US $41.99', '-11%', 'Green', '', 'US $26.69', 'US $29.99', '-11%', 'Ivory', '', 'US $10.67', 'US $11.99', '-11%'])
excel2.close()