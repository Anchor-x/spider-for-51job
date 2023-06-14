# coding=utf-8
# -*- coding:uft-8 -*-
# 数据入库

import pymssql
import pandas as pd


def clearSalary(string) -> int or Exception:
    try:
        string = str(string)
        if not string:
            return None
        elif '千' in string and '万' in string:
            if '·' in string:
                new_salary_list = string.split('·')[0].split("-")
            else:
                new_salary_list = string.split('-')
            temp = (float(new_salary_list[0].strip("千")) + float(new_salary_list[1].strip("万")) * 10) / 2
            new_salary = f'{temp}'
        elif "千·" in string:
            new_salary_list = string.strip('薪').split('·')[0].split('-')
            new_salary = 0
            for i in new_salary_list:
                new_salary += float(i.strip('千'))
            new_salary = float(new_salary) / len(new_salary_list)
        
        elif '千' in string:
            new_salary_list = string.strip('千').split('-')
            new_salary = float(new_salary_list[0]) + float(new_salary_list[1]) / 2
        
        elif '万/年' in string:
            new_salary_list = string.strip('万/年').split('-')
            new_salary = 0
            for i in new_salary_list:
                new_salary += float(i) * 12
            new_salary = float(new_salary) / len(new_salary_list)
        
        elif '万·' in string:
            new_salary_list = string.strip('薪').split('·')[0].split('-')
            new_salary = 0
            for i in new_salary_list:
                new_salary += float(i.strip('万')) * 10
            new_salary = float(new_salary) / len(new_salary_list)
        
        elif '万' in string:
            new_salary_list = string.strip('万').split('-')
            new_salary = 0
            for i in new_salary_list:
                new_salary += float(i) * 10
            new_salary = float(new_salary) / len(new_salary_list)
        
        elif '元' in string:
            if "元/天" in string:
                new_salary_list = string.strip('元/天')
                new_salary = 0
                for i in new_salary_list:
                    new_salary += float(i) * 30 / 1000
                new_salary = float(new_salary) / len(new_salary_list)
            else:
                new_salary = float(string.split("元")[0]) * 8 * 22 / 1000
        
        elif "千以下" in string:
            new_salary = string.strip('千以下')
        elif '千' in string:
            new_salary = string.strip('千')
        else:
            new_salary = None
        return new_salary
    except Exception as e:
        print(e)
        print(string)


def clear(df):
    df['薪资'] = df['薪资'].apply(clearSalary)
    df.duplicated(keep='first')
    df.dropna(how='any', inplace=True)
    return df


def insert():
    df = pd.read_excel(f'data/{key}.xlsx', engine='openpyxl')
    df = clear(df)
    resLs = df.to_dict(orient='records')
    
    # 连接到SQL Server
    conn = pymssql.connect(server='server',
                           port='1433',
                           user='sa',
                           password='password',
                           database='JobSpider')
    
    cursor = conn.cursor()
    
    for res in resLs:
        res['keyword'] = key
        
        sql = "insert into JobSpider.dbo.job51" \
              "(keyword, title, salary, area, experience, degree, company, class, scale, industry)" \
              "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        tup = (res['keyword'],
               res['标题'], res['薪资'], res['地区'],
               res['经验'], res['学历'], res['公司'],
               res['类型'], res['规模'], res['行业'])
        cursor.executemany(sql, [tup])
        conn.commit()
    conn.close()


if __name__ == '__main__':
    for key in ['python', 'pytorch', 'tensorflow', '爬虫']:
        insert()
