__author__ = 'zhangchun'
# coding=utf-8

import time
import unittest
from framework import webPay
import os
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions



class TestCase(unittest.TestCase):

    def setUp(self):  #初始化
        self.driver=webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(20)

    def tearDown(self):
        self.driver.quit()

    def test_bankPay(self):

        """遍历网上银行支付方式的各个银行渠道，验证是否跳转到对应银行支付页面"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_link_text(u'网上银行').click()
        nowHandle=self.driver.current_window_handle
        self.driver.find_element_by_id('openMoneyBankBtn').click()
        self.select_server()
        time.sleep(2)
        #选择游戏服
        inputs=self.driver.find_element_by_class_name('sBank-bd-ul').find_elements_by_tag_name('input')
        for input in inputs:
        #获取所有银行渠道单选框，遍历点击银行单选框
            if input.get_attribute("type")=='radio':
                bankName=input.get_attribute("value")
                input.click()
                self.driver.find_element_by_id("payFormSubmitBtn").click()
                time.sleep(1)

                try:
                    webPay.switch_to_newPage(self,nowHandle)
                    #定位到当前页面窗口
                    print(webPay.banktitle(self))
                    time.sleep(10)
                    webPay.close_allAlert(self)
                    webPay.screenShot(self,"Firefox",bankName)
                    self.assertTrue(webPay.enum(self,'bank',bankName)
                                    in webPay.banktitle(self),u'没有进入对应支付方式页面'+bankName)
                    #验证是否进入对应的支付页面
                except Exception as e:
                    print('Reason:', e)
                self.driver.close()
                self.driver.switch_to.window(nowHandle)
                time.sleep(1)
                self.driver.find_element_by_id('kz_pay_id').click()

    def select_server(self):
        #选择游戏服务器
        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        time.sleep(1)
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(1)
        self.driver.find_element_by_id('server_list').find_element_by_id(webPay.config(self,'setting','server_id')).click()
        self.driver.find_element_by_id('server_1580501').click()
        time.sleep(1)




if __name__ == "__main__":
    unittest.main()