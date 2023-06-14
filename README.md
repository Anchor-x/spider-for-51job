# spider-for-51job
Python期末大作业，基于selenium的51job网站爬虫与数据可视化分析

## 配置环境
```bash
conda env create -f environment.yaml
```

```bash
pip install -r requirements.txt
```

## 运行爬虫
```bash
python ./GetData.py
```

## 创建数据库和表
> 使用`SQL Server`数据库

创建表：`CreateTable.sql`文件

## 数据入库
```bash
python ./DataStorage.py
```

## 数据可视化
```bash
python ./DataView
```
