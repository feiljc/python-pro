import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# 打开chrome浏览器（需提前安装好chromedriver）
browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()
print("正在打开网页...")
browser.get("http://op1.win007.com/oddslist/2062092.htm")

print("等待网页响应...")
# 需要等一下，直到页面加载完成
wait = WebDriverWait(browser, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcenter")))

print("正在获取网页数据...")
soup = BeautifulSoup(browser.page_source, "lxml")
browser.close()

# 表头和表数据
oddstr_1129 = soup.find('tr', id = 'oddstr_1129')

# 得到表头数据
oddstd_1129 = oddstr_1129.findAll("td")

print(oddstd_1129)
