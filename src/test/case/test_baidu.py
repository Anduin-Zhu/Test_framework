# -*- coding:utf-8 -*-
__author__ = '朱永刚'

import os
import time
import unittest
from utils.config import Config,DRIVER_PATH,DATA_PATH,REPORT_PATH
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.mail import Email
from test.page.baidu_result_page import BaiDuMainPage,BaiDuResultPage


class TestBaiDu(unittest.TestCase):
    #URL = 'https://www.baidu.com/'
    URL = Config().get('URL')
    #base_path = os.path.abspath(os.path.join(os.getcwd(), '..\..'))#获取路径
    #driver_path = os.path.abspath(base_path+'\drivers\geckodriver.exe')

    excel = os.path.join(DATA_PATH,'baidu.xlsx')
    locator_kw = (By.ID,'kw')
    locator_su = (By.ID,'su')
    locator_result = (By.XPATH, '//div[contains(@class, "result")]/h3/a')

    def sub_setUp(self):
        #初始页面是main page，传入浏览器类型打开浏览器
        self.page = BaiDuMainPage(browser_type='firefox').get(self.URL,maxmize_windows=False)

        #self.driver = webdriver.Firefox(executable_path=os.path.join(DRIVER_PATH,'geckodriver.exe'))#用框架里的浏览器驱动
        #self.driver.get(self.URL)

    def sub_tearDown(self):
        #self.driver.quit()
        self.page.quit()

    def test_search(self):
        #可以对用例简单说明
        u"""百度搜索"""
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                self.page.search(d['search'])
                #self.driver.find_element(*self.locator_kw).send_keys(d['search'])
                #self.driver.find_element(*self.locator_su).click()
                #self.driver.implicitly_wait(5)
                time.sleep(2)
                self.page.save_screen_shot('test_baidu')#调用截图方法
                self.page = BaiDuResultPage(self.page)#页面跳转到result page
                links = self.page.result_links
                #links = self.driver.find_elements(*self.locator_result)  # ????????
                for link in links:
                    # print(link.text)
                    logger.info(link.text)
                self.sub_tearDown()

'''
    def test_search_0(self):

        self.driver.find_element(*self.locator_kw).send_keys('selenium 灰蓝')
        self.driver.find_element(*self.locator_su).click()
        self.driver.implicitly_wait(5)
        links = self.driver.find_elements(*self.locator_result)#????????
        for link in links:
            #print(link.text)
            logger.info(link.text)

    def test_search_1(self):

        self.driver.find_element(*self.locator_kw).send_keys('Python selenium')
        self.driver.find_element(*self.locator_su).click()
        self.driver.implicitly_wait(5)
        links = self.driver.find_elements(*self.locator_result)
        for link in links:
            #print(link.text)
            logger.info(link.text)
'''
if __name__ == '__main__':
    #unittest.main(verbosity=2)
    # 报告格式
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    report = REPORT_PATH + r'\\' + now + 'report.html'
    f = open(report, 'wb')
    runner = HTMLTestRunner(f, verbosity=2, title=u'百度测试报告', description=u'用例执行情况')
    runner.run(TestBaiDu('test_search'))
    Email().sentreport()