#coding=UTF-8-
import csv
def read_csv(filename):
    """根据文件名读取csv文件"""
    with open(filename,'r') as fp:
        reader = csv.reader(fp)
        table = list(reader)
        for x in table:
            print(x)
        return table

def create_csv(filename,headers,datas):
    """根据文件名，标题，数据创建csv文件"""
    """
    filename = "2.csv"
    hearder=['id','class','name']
    values = [('zhiliao',18,'111'),('wena',20,'222'),('bbc',21,'111')]
    """
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        # 写入列标题
        writer.writerow(headers)
        writer.writerows(datas)

def create_dict_csv(filename, headers, datas):
    """根据字典创建csv文件"""
    """
    headers = ['name','age','classroom']
    values = [
        {"name":'wenn',"age":20,"classroom":'222'},
        {"name":'abc',"age":30,"classroom":'333'}]
    """
    with open(filename,'w',newline='') as fp:
        writer = csv.DictWriter(fp,headers)
        writer.writerows(datas)