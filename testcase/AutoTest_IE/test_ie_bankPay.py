__author__ = 'zhangchun'
# coding=utf-8

import time
import unittest
from framework import webPay
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
#取当前文件所在目录的上一级目录


class TestCase(unittest.TestCase):

    def setUp(self):  #初始化
        ie_driver = os.path.abspath(webPay.config(self,'driver_path','ie'))
        # 读取配置文件config中iedriver文件位置，创建IEDriverServer的一个接口用于连接ie
        os.environ["webdriver.ie.driver"] = ie_driver
        self.driver = webdriver.Ie(ie_driver)
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(20)

    def tearDown(self):
        self.driver.close()

    def test_bankPay(self):

        """遍历网上银行支付方式的各个银行渠道，验证是否跳转到对应银行支付页面"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_link_text(u'网上银行').click()
        nowHandle=self.driver.current_window_handle
        self.driver.find_element_by_id('openMoneyBankBtn').click()
        time.sleep(2)
        self.select_server()
        self.driver.find_element_by_id("payFormSubmitBtn").click()
        time.sleep(2)
        #选择游戏服
        inputs=self.driver.find_element_by_class_name('sBank-bd-ul').find_elements_by_tag_name('input')
        for input in inputs:
            if input.get_attribute("type")=='radio':
                bankName=input.get_attribute("value")
                input.click()
                self.driver.find_element_by_id("payFormSubmitBtn").click()
                time.sleep(1)
                try:
                    webPay.switch_to_newPage(self,nowHandle)
                    time.sleep(10)
                    webPay.screenShot(self,"IE",bankName)
                    self.assertTrue(webPay.enum(self,'bank',bankName)
                                    in webPay.banktitle(self),u'没有进入对应支付方式页面'+bankName)
                except Exception as e:
                    print('Reason:', e)

                self.driver.close()
                self.driver.switch_to.window(nowHandle)
                time.sleep(1)
                self.driver.find_element_by_id('kz_pay_id').click()



    def select_server(self):
        self.driver.find_element_by_id('changeAccountBtn').click()
        self.driver.find_element_by_id('account_id').send_keys(Keys.CONTROL,'a')
        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        time.sleep(2)
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(2)
        self.driver.find_element_by_id('server_list').find_element_by_id(webPay.config(self,'setting','server_id')).click()
        self.driver.find_element_by_id('server_1580501').click()
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
