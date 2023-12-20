# -*- coding: utf-8 -*-
import xlwt # 进行Excel操作

def main():
     # 创建一个Workbook对象
    workbook = xlwt.Workbook()
    # 添加一个sheet
    sheet = workbook.add_sheet('sheet1')

    # 写入表头
    # sheet.write(0, 0, 'X')
    # for i in range(1, 10):
    #     sheet.write(0, i, i)

    # 写入表格数据
    for i in range(0, 10):
        for j in range(0, i):
            sheet.write(i, j, f'{i} X {j+1} = {i * (j+1)}')

    # 保存文件
    workbook.save('multiplication_table.xls')

if __name__ == '__main__':
    main()