import openpyxl
import os


def collectRepairCases(allcasenameFile, excelFile):
    #收集用例名称
    workbook = openpyxl.Workbook()
    data_sheet = workbook.create_sheet('result')
    i = 1
    with open(allcasenameFile) as file_object:   
        for line in file_object:
            i = i + 1
            data_sheet.cell(row=i, column=1, value=line)
    
    workbook.save(excelFile)


def collectResult(testrepairPath, excelFile):
    i = 1
    wb = openpyxl.load_workbook(excelFile)
    sheet = wb.get_sheet_by_name('result')
    for root, dirs, files in os.walk(testrepairPath):
        # print(root, end = ' ') #当前目录路径
        # print(dirs, end = ' ') #当前路径下的所有子目录
        # print(files)           #当前目录下的所有非目录子文件
        for file in files:
            if file == 'repair-test-case-log.txt':
                i = i + 1
                with open(os.path.join(root, file)) as file_object:
                    contents = file_object.read()
                    sheet.cell(row=i, column=3, value=contents)
                continue
    wb.save(excelFile)


if __name__ == '__main__':
    # collectRepairCases('C:\\Users\\Y_sun\\Desktop\\2019-1\\experiment-data\\repair-subjects\\all-repair-cases.txt', 'C:\\Users\\Y_sun\\Desktop\\2019-1\\experiment-data\\data.xlsx')
    collectResult('C:\\Users\\Y_sun\\Desktop\\2019-1\\experiment-data\\test-repair-author', 'C:\\Users\\Y_sun\\Desktop\\2019-1\\experiment-data\\data.xlsx')