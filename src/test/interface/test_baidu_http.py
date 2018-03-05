# -*- coding:utf-8 -*-
__author__ = '朱永刚'

import unittest
import time
from utils.config import Config,REPORT_PATH
from utils.client import HTTPClient
from utils.log import logger
from utils.HTMLTestRunner_PY3 import HTMLTestRunner

class TestBaiDuHttp(unittest.TestCase):
    URL = Config().get('URL')

    def setUp(self):
        self.client = HTTPClient(url=self.URL,method='GET')

    def test_baidu_http(self):
        res = self.client.send()
        logger.debug(res.text)
        self.assertIn('百度一下，你就知道',res.text)

if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    report = REPORT_PATH + r'\\' + now + 'report.html'
    f = open(report, 'wb')
    runner = HTMLTestRunner(f, verbosity=2, title=u'百度测试报告', description=u'用例执行情况')
    runner.run(TestBaiDuHttp('test_baidu_http'))