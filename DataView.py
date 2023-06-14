# coding=utf-8
# -*- coding:uft-8 -*-
# 数据分析
import jieba
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, WordCloud, Pie, Line
from pyecharts.globals import ThemeType, SymbolType
import pymssql


def createWordCould(txt, name):
    print(name + '词云图绘制')
    words = jieba.cut(txt)
    word_dic = {}
    stops = []
    for word in words:
        if len(word) > 1 and word not in stops:
            word_dic[word] = word_dic.get(word, 0) + 1
    ls = list(word_dic.items())
    word_ls = ls[:500]
    chart = (
        WordCloud(
            init_opts=opts.InitOpts(theme=ThemeType.ESSOS, width='100%', height='780px')
        )
        .add('', word_ls, word_size_range=[20, 100], shape=SymbolType.ROUND_RECT)
        .set_global_opts(title_opts=opts.TitleOpts(title=f'{name}词云图'))
    )
    chart.render(f'./chart/{key}/{name.replace(key, "")}词云图.html')
    print(name + '词云图绘制完成')


def posit_draw(posit_ls, name):
    print(f'{name}排行柱状图绘制')
    dic = {}
    for posi in posit_ls:
        dic[posi] = dic.get(posi, 0) + 1
    items = list(dic.items())
    items.sort(key=lambda x: x[1], reverse=True)
    posit_ls = [item[0] for item in items][:9]
    num_ls = [item[1] for item in items][:9]
    chart = (
        Bar(
            init_opts=opts.InitOpts(theme=ThemeType.PURPLE_PASSION, width='100%', height='780px')
        )
        .add_xaxis(posit_ls)
        .add_yaxis('数量', num_ls)
        .set_colors(['#e098c6'])
        .set_global_opts(title_opts=opts.TitleOpts(title=f'{name}排行柱状图'))
    )
    chart.render(f'./chart/{key}/{name.replace(key, "")}排行柱状图.html')
    print(f'{name}排行柱状图绘制完成')


def pieDraw(label_ls, count_ls, name):
    print(f'{name}分布饼状图绘制')
    chart = (
        Pie(
            init_opts=opts.InitOpts(theme=ThemeType.DARK, width='100%', height='780px')
        )
        .add('', [list(z) for z in zip(label_ls, count_ls)])
        .set_global_opts(title_opts=opts.TitleOpts(title=f'{name}分布饼状图'))
        .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}: {c}'))
    )
    chart.render(f'./chart/{key}/{name.replace(key, "")}分布饼状图.html')
    print(f'{name}分布饼状图绘制完成')


def lineDraw(city_ls, salary_ls, name):
    print(name + '主要城市平均薪资折线图')
    chart = (
        Line(
            init_opts=opts.InitOpts(theme=ThemeType.SHINE, width='100%', height='780px')
        )
        .add_xaxis(city_ls)
        .add_yaxis('平均薪资', salary_ls)
        .set_global_opts(title_opts=opts.TitleOpts(title=f'{name}主要城市平均薪资折线图'))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    )
    chart.render(f'./chart/{key}/{name.replace(key, "")}主要城市平均薪资折线图.html')
    print(name + '主要城市平均薪资折线图绘制完成')


def positPlusDraw(posit_ls, num_ls, name):
    print(f'{name}对比柱状图绘制')
    chart = (
        Bar(
            init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, width='100%', height='780px')
        )
        .add_xaxis(posit_ls)
        .add_yaxis('最低薪资', num_ls[0])
        .add_yaxis('平均薪资', num_ls[1])
        .add_yaxis('最高薪资', num_ls[2])
        .set_global_opts(title_opts=opts.TitleOpts(title=f'{name}排行柱状图'))
    )
    chart.render(f'./chart/{key}/{name.replace(key, "")}对比柱状图.html')
    print(f'{name}对比柱状图绘制完成')


def GetConnect():
    # 连接到SQL Server
    conn = pymssql.connect(server='server',
                           port='1433',
                           user='sa',
                           password='password',
                           database='JobSpider')
    if not conn:
        raise (NameError, "连接数据库失败")
    else:
        return conn


def main():
    global key
    # 词云
    conn = GetConnect()
    sql_1 = "select title from JobSpider.dbo.job51 where keyword = %(keyword)s"
    df = pd.read_sql(sql_1, conn, params={'keyword': key})
    title_ls = df['title'].tolist()
    titles = '/'.join(title_ls)
    createWordCould(titles, f'前程无忧{key}标题')
    
    # 排行柱状图
    sql_2 = "select area from JobSpider.dbo.job51 where keyword = %(keyword)s"
    df = pd.read_sql(sql_2, conn, params={'keyword': key})
    df['area'] = df['area'].apply(lambda x: x.split('·')[0])
    posit_ls = df['area'].tolist()
    posit_draw(posit_ls, f'前程无忧{key}城市职位数量')
    
    # 分布饼状图
    sql_3 = "select experience from JobSpider.dbo.job51 where keyword = %(keyword)s"
    df = pd.read_sql(sql_3, conn, params={'keyword': key})
    exp_ls = df['experience'].tolist()
    exp_dic = {}
    for exp in exp_ls:
        exp_dic[exp] = exp_dic.get(exp, 0) + 1
    exp_item = list(exp_dic.items())
    exp_item.sort(key=lambda x: x[1], reverse=True)
    pieDraw([i[0] for i in exp_item], [i[1] for i in exp_item], f'前程无忧{key}职位经验要求')
    
    # 分布饼状图
    sql_4 = "select degree from JobSpider.dbo.job51 where keyword = %(keyword)s"
    df = pd.read_sql(sql_4, conn, params={'keyword': key})
    eduLs = df['degree'].tolist()
    edu_dic = {}
    for edu in eduLs:
        edu_dic[edu] = edu_dic.get(edu, 0) + 1
    edu_item = list(edu_dic.items())
    edu_item.sort(key=lambda x: x[1], reverse=True)
    pieDraw([i[0] for i in edu_item], [i[1] for i in edu_item], f'前程无忧{key}职位学历要求')
    
    # 薪资折线图
    sql_5 = "select salary,keyword,area from JobSpider.dbo.job51 where keyword = %(keyword)s and area = %(area)s"
    dic = {}
    for posit in posit_ls:
        dic[posit] = dic.get(posit, 0) + 1
    
    items = list(dic.items())
    items.sort(key=lambda x: x[1], reverse=True)
    # 在一个列表 items 中提取前 20 个元素的第一个值，并将这些值组成一个新的列表 city_ls
    city_ls = [item[0] for item in items][:20]
    
    salary_ls = []
    for city in city_ls:
        df = pd.read_sql(sql_5, conn, params={'keyword': key, 'area': city})
        df_select = df[(df['keyword'] == key) & (df['area'] == city)]
        df['salary'] = pd.to_numeric(df['salary'], downcast="integer")
        # salary_ls.append(int(df['salary'].mean()))
        salary_ls.append(df_select['salary'])
    
    dic = {}
    for i in range(len(city_ls)):
        dic[city_ls[i]] = salary_ls[i]
    
    for i in range(len(city_ls)):
        items = sorted(dic[city_ls[i]].items(), key=lambda x: x[1], reverse=True)
    
    city_ls = [item[0] for item in items][:8]
    salary_ls = [item[1] for item in items][:8]
    
    lineDraw(city_ls, salary_ls, f'前程无忧{key}职位')
    
    # 对比饼状图
    dic = {}
    num_ls = [[], [], []]
    sql_6 = "select salary,keyword,area from JobSpider.dbo.job51 where keyword = %(keyword)s and area = %(area)s"
    
    for posit in posit_ls:
        dic[posit] = dic.get(posit, 0) + 1
    
    items = list(dic.items())
    
    items.sort(key=lambda x: x[1], reverse=True)
    
    posit_ls = [item[0] for item in items][:9]
    for city in posit_ls:
        df = pd.read_sql(sql_5, conn, params={'keyword': key, 'area': city})
        df_select = df[(df['keyword'] == key) & (df['area'] == city)]
        num_ls[0].append(int(float(df_select['salary'].min())))
        
        df['salary'] = pd.to_numeric(df['salary'], downcast="integer")
        num_ls[1].append(df['salary'])
        
        num_ls[2].append(int(float(df_select['salary'].max())))
        positPlusDraw(posit_ls, num_ls, f'前程无忧{key}职位城市薪资')


if __name__ == '__main__':
    for key in ['python', 'pytorch', 'tensorflow', '爬虫']:
        main()
