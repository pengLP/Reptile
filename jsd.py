
import os,xlrd
from typing import Type

path = "C:\\Users\\Lp\\Desktop\\jsd.xlsx"

class Item:

    def __init__(self,dq) -> None:
        self.dq = dq
        self.data = []

    def getData(self, data):
        self.data = data

if __name__ == '__main__':
    # 打开excel文件,获取工作簿对象
    excel = xlrd.open_workbook(path)
    sheets = excel.sheet_names()
    table = excel.sheet_by_index(0)
    titles = table.row_values(0)
    col = -1
    # 找到大区在多少列
    for i in range(len(titles)):
        if(titles[i] == '大区'):
            col = i
    data = {}
    for i in range(1,table.nrows):
        data[table.cell(i, col).value] = Item(table.cell(i, col).value)

    for sheetName in sheets:
        sheet = excel.sheet_by_name(sheetName)
