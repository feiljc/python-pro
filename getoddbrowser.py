import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False

# 打开chrome浏览器（需提前安装好chromedriver）
browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()
print("正在打开网页...")
browser.get("http://op1.win007.com/OddsHistory.aspx?id=104587617&sid=2062092&cid=1129&l=0")

print("等待网页响应...")
# 需要等一下，直到页面加载完成
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.ID, "odds")))

print("正在获取网页数据...")
soup = BeautifulSoup(browser.page_source, "lxml")
browser.close()

oddstrs = soup.findAll('tr')
print(oddstrs)

odddatas = []
for oddstr in oddstrs:
    oddstds = oddstr.findAll("td")
    odddata = []
    for oddstd in oddstds:
        oddstd_text = oddstd.text

        if oddstd_text.find('(初盘)') >= 0:
            oddstd_text = oddstd_text.replace('(初盘)', '')
        if is_chinese(oddstd_text):
            break
        odddata.append(oddstd_text)
    if len(odddata) > 0:
        odddata[-1] = odddata[-1][-5:]
        del odddata[3: 10]
        odddatas.append(odddata)
        print(odddata)

print(odddatas)













