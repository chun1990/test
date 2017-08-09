__author__ = 'zhangchun'
# coding=utf-8

import time
import unittest
from framework import webPay
import os
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys

class TestCase(unittest.TestCase):

    def setUp(self):  #初始化
        self.driver=webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(20)

    def tearDown(self):
        self.driver.quit()

    def test_swicthpay(self):

        """返回到支付中心页面，弹出框中点击“其他支付方式付款”下拉框选择进入对应的支付页面"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_link_text(u'网上银行').click()
        nowHandle=self.driver.current_window_handle
        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        time.sleep(1)
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(1)
        self.driver.find_element_by_id('server_list').find_element_by_id(webPay.config(self,'setting','server_id')).click()
        self.driver.find_element_by_id('server_1580501').click()
        time.sleep(1)
        self.driver.find_element_by_id("payFormSubmitBtn").click()
        time.sleep(1)
        webPay.switch_to_newPage(self,nowHandle)
        self.driver.close()
        self.driver.switch_to.window(nowHandle)
        time.sleep(1)
        payselects=['支付宝','PayPal','神州行移动卡','财付通','游戏卡','固定电话','港澳台充值','联通卡','电信卡','网上银行']
        #遍历选择“其他支付方式付款”下拉框中的所有选项，进入对应的充值页面
        for payselect in payselects:
            options=self.driver.find_element_by_id('otherPaySelect').find_elements_by_tag_name('option')
            for option in options:
                if option.get_attribute('text')==payselect:
                    option.click()
                    break
            time.sleep(2)
            try:
                self.assertTrue(webPay.enum(self,'channel',payselect)
                                                in self.driver.find_element_by_class_name("open-tip").text)
            except:
                self.assertTrue(webPay.enum(self,'channel',payselect)
                                                in self.driver.find_element_by_id('tags_list').text)

            self.driver.find_element_by_id('account_id').send_keys('zhifuceshi'+Keys.ENTER)
            time.sleep(4)
            self.driver.find_element_by_id("payFormSubmitBtn").click()
            time.sleep(2)
            webPay.switch_to_newPage(self,nowHandle)
            self.driver.close()
            self.driver.switch_to.window(nowHandle)
            time.sleep(1)

if __name__ == "__main__":
    unittest.main()