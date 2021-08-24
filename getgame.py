# -*- coding: utf-8 -*-

from __future__ import print_function, division

from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

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

class Spider(object):

    def __init__(self):
        ## setup
        # self.base_url = base_url
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def get_team_odd_oddslist(self, team_data):
        url = 'http://op1.win007.com/oddslist/' + team_data[0] + '.htm'
        #print('get_team_odd_oddslist:' + url)
        # 打开chrome浏览器（需提前安装好chromedriver）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        #print("正在打开网页...")
        browser.get(url)
        #print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tcenter")))

        #print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()

        oddstr_1129 = soup.find('tr', id='oddstr_1129')
        if oddstr_1129 is None:
            return 0
        oddstds_1129 = oddstr_1129.findAll("td", onclick=True)

        oddurl = "http://op1.win007.com"
        for oddstd in oddstds_1129:
            data = oddstd.get('onclick')
            data = data.split("'")
            oddurl += data[1]
            break

        #print(oddurl)

        return oddurl

    def get_team_odd_OddsHistory(self, team_data, oddurl):
        # 打开chrome浏览器（需提前安装好chromedriver）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        # browser = webdriver.PhantomJS()
        #print("正在打开网页...")
        browser.get(oddurl)

        #print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, "odds")))

        #print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()

        oddstrs = soup.findAll('tr')
        #print(oddstrs)

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
                odddata[-1] = str(datetime.now().year) + '-' + odddata[-1][-11:]
                del odddata[3: 10]
                odddatas.append(odddata)

        #print(odddatas)
        #print(team_data)
        team_data += odddatas[-1][0:3]
        team_data_s = datetime.strptime(team_data[2], '%Y-%m-%d %H:%M') + timedelta(hours=-1)
        for odd_data in odddatas:
            odd_data_s = datetime.strptime(odd_data[-1], '%Y-%m-%d %H:%M')
            if odd_data_s <= team_data_s:
                #print(odd_data_s)
                #print(team_data_s)
                team_data += odd_data[0:3]
                break
        if len(team_data) < 10:
            team_data += odddatas[-1][0:3]
        #print(team_data)
        return 1

    def get_team_odd_data(self, team_data):
        oddurl = self.get_team_odd_oddslist(team_data)
        if oddurl == 0:
            return 0
        self.get_team_odd_OddsHistory(team_data, oddurl)
        return 1

    #=========================================================================================================
    def get_team_asian_asianlist(self, team_data):
        url = 'http://vip.win007.com/AsianOdds_n.aspx?id=' + team_data[0]
        # 打开chrome浏览器（需提前安装好chromedriver）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        #print("正在打开网页...")
        browser.get(url)
        #print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, "odds")))

        #print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()

        oddurl = "http://vip.win007.com"

        asiantrs = soup.findAll('tr')
        for asiantr in asiantrs:
            asiantds = asiantr.findAll('td')
            if asiantds[0].text != '澳门':
                continue
            else:
                for asiantd in asiantds:
                    if asiantd.text.find('详') >= 0:
                        asianas = asiantd.findAll('a')
                        oddurl += asianas[0]['href']
                        break
                break
            #print(oddurl)
        return oddurl

    def get_team_odd_asianHistory(self, team_data, oddurl):
        # 打开chrome浏览器（需提前安装好chromedriver）
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        # browser = webdriver.PhantomJS()
        #print("正在打开网页...")
        browser.get(oddurl)

        #print("等待网页响应...")
        # 需要等一下，直到页面加载完成
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, "odds2")))

        #print("正在获取网页数据...")
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()

        oddstrs = soup.findAll('tr')
        #print(oddstrs)

        odddatas = []
        for oddstr in oddstrs:
            #print(oddstr.text)
            if oddstr.text.find('即') >= 0:
                odddatas.append(oddstr.text)

        team_data += odddatas[-1].split()[0:3]
        team_data_s = datetime.strptime(team_data[2], '%Y-%m-%d %H:%M') + timedelta(hours=-1)
        itercars = iter(odddatas)
        next(itercars)
        for odddata in itercars:
            odddatastr = odddata.split('\n')
            #print(odddatastr)
            odd_data_s = datetime.strptime(str(datetime.now().year) + '-' + odddatastr[4], '%Y-%m-%d %H:%M')
            if odd_data_s <= team_data_s:
                team_data += odddatastr[1:4]
                break
        if len(team_data) < 16:
            team_data += odddatas[-1].split()[0:3]
        #print(team_data)
        return 1

    def get_team_asian_data(self, team_data):
        oddurl = self.get_team_asian_asianlist(team_data)
        self.get_team_odd_asianHistory(team_data, oddurl)
        return 1
    # =========================================================================================================

    def get_team_data(self, team_data):
        reda = self.get_team_odd_data(team_data)
        if reda == 0:
            return 0
        self.get_team_asian_data(team_data)
        del team_data[0]
        for i, value in enumerate(team_data):
            if (4 <= i <= 10) or (12 <= i <= 13) or i == 15:
                value = float(value)
            else:
                value = str(value.encode('utf-8'))
        return team_data

    def get_team_ids(self, main_url):
        #print(main_url)
        self.driver.get(main_url)
        teams = self.driver.find_elements_by_xpath("//*[@id='table_live']/tbody/tr")
        data = []
        weekday = ''
        wd = datetime.now().weekday()
        week_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        week_map = dict(enumerate(week_list))
        wd_now = week_map[wd]
        flag = 0
        for team in teams:
            team_id = team.get_attribute("id")
            if len(team_id) == 0:
                if team.text.find(wd_now) > -1:
                    weekd = team.text.split()
                    weekday = weekd[0].lstrip()
                    weekday = datetime.strptime(weekd[0].lstrip(), '%Y年%m月%d日').date()
                    weekday = datetime.strftime(weekday,'%Y-%m-%d')
                    flag = 1
                else:
                    flag = 0
                    continue
            if flag == 0:
                continue
            index1 = team_id.find('tr1')
            if index1 <= -1:
                continue
            team_id = team_id.split('_')
            del team_id[0]
            team_name = team.text
            index1 = team_name.find('亚欧析')
            if index1 > -1:
                team_name = team_name[0:index1].split()
                if is_chinese(team_name[3]):
                    team_name = team_name[1:6]
                    del team_name[3]
                    #print(team_id, team_name)
                    date_s = datetime.now().date()
                    #datetime_object = (date_s + timedelta(days=-1)).strftime("%Y-%m-%d")
                    if team_name[1] < '11:00' or team_name[1] > '21:00':
                        team_name[1] = weekday + ' 20:00'
                    else:
                        team_name[1] = weekday + ' ' + team_name[1]
                    data.append([team_id + team_name])
        self.team_list = data
        # self.team_list = pd.DataFrame(data, columns=['team_name', 'team_id'])
        # self.team_list.to_excel('国家队ID.xlsx', index=False)

    def get_all_team_data(self):
        # 循环爬取每一支队的比赛数据(URL)
        datas = []
        data = []
        self.get_team_ids('http://jc.win007.com/index.aspx')
        for i, [team_data] in enumerate(self.team_list):
            print(i, team_data)
            reda = self.get_team_data(team_data)
            if reda == 0:
                continue
            data.append(team_data)
        print('=========================================================')
        print(data)
        df = pd.DataFrame(data,
                          columns=['赛事', '时间', '主队', '客队', '初胜赔', '初平赔', '初负赔', '终胜赔', '终平赔', '终负赔',
                                   '初上盘水', '初盘口', '初下盘水', '终上盘水', '终盘口', '终下盘水'])
        datas.append(df)

        self.driver.close()
        output = pd.concat(datas)
        output.reset_index(drop=True, inplace=True)
        # print(output)
        output.to_csv('预测_' + str(datetime.now().date()) + '.csv', index=False, encoding='utf-8')
        print('over')

if __name__ == "__main__":
    spider = Spider()
    # 第一步：抓2018世界杯球队的ID。第二部：循环抓取每一支队的比赛数据。
    spider.get_all_team_data()