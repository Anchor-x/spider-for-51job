# coding=utf-8
# -*- coding:uft-8 -*-
# 数据爬取

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from lxml import etree
import random


def main():
    resLs = []
    for p in range(pz):
        p += 1
        print(f'爬取第{p}页>>>')
        sleep(10)
        for i in range(200):
            sleep(random.random() / 10)
            driver.execute_script('window.scrollBy(0, 50)')
        res = driver.page_source
        tree = etree.HTML(res)
        for li in tree.xpath('//div[@class="j_joblist"]/div'):
            name = li.xpath('.//span[@class="jname at"]/text()')[0]
            href = li.xpath('./a/@href')[0]
            time = li.xpath('.//span[@class="time"]/text()')[0]
            sala = (li.xpath('.//span[@class="sal"]/text()') + [''])[0]
            addr = (li.xpath('.//span[@class="d at"]/span/text()') + [''] * 5)[0]
            exp = (li.xpath('.//span[@class="d at"]/span/text()') + [''] * 5)[2]
            edu = (li.xpath('.//span[@class="d at"]/span/text()') + [''] * 5)[4]
            comp = li.xpath('.//a[@class="cname at"]/text()')[0]
            kind = li.xpath('.//p[@class="dc at"]/text()')[0].split('|')[0].strip()
            num = (li.xpath('.//p[@class="dc at"]/text()')[0].split('|') + [''])[1].strip()
            ind = (li.xpath('.//p[@class="int at"]/text()') + [''])[0]
            dic = {
                '标题': name,
                '薪资': sala,
                '地区': addr,
                '经验': exp,
                '学历': edu,
                '公司': comp,
                '类型': kind,
                '规模': num,
                '行业': ind
            }
            print(dic)
            resLs.append(dic)
        pd.DataFrame(resLs).to_excel(f'data/{key}.xlsx', index=False, encoding='utf-8')
        if p != pz:
            driver.find_element(By.ID, 'jump_page').clear()
            driver.find_element(By.ID, 'jump_page').send_keys(p + 1)
            sleep(random.random())
            driver.find_element(By.CLASS_NAME, 'jumpPage').click()


if __name__ == '__main__':
    pz = 50
    for key in ['python', 'pytorch', 'tensorflow', '爬虫']:
        # for key in ['Java']:
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options=options)
        js = open('stealth.min.js').read()
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
        driver.get(f'https://we.51job.com/pc/search?keyword={key}&searchType=2&sortType=0&metro=')
        sleep(10)
        main()
        driver.quit()
