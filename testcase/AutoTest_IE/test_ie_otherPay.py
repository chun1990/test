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

    def test_otherPay(self):

        """支付中心页面切换点击左侧支付渠道，显示对应的页面"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        nowHandle=self.driver.current_window_handle
        list_payment1=['网上银行','支付宝','微信支付','PayPal','神州行移动卡','财付通',
                       '游戏卡','固定电话','港澳台充值','联通卡','电信卡']
        list_payment2=['支付宝','PayPal','神州行移动卡','财付通','联通卡','电信卡']
        for payment in list_payment1:
            self.driver.find_element_by_link_text(payment).click()
            time.sleep(2)
            try:
                self.assertTrue(webPay.enum(self,'channel',payment) in self.driver.find_element_by_class_name("open-tip").text)
            except:
                self.assertTrue(webPay.enum(self,'channel',payment) in self.driver.find_element_by_id('tags_list').text)
                #遍历点击页面左侧的支付方式，查看是否切换到对应的页面
            webPay.screenShot(self,"IE",payment)
            if payment in list_payment2:
                #若支付方式为list_payment2中的元素，选择充值服点击充值，并验证是否进入对应的充值页面
                self.select_server()
                self.driver.find_element_by_id("payFormSubmitBtn").click()
                time.sleep(2)

                try:
                    webPay.switch_to_newPage(self,nowHandle)
                    time.sleep(10)
                    print(self.driver.title)
                    webPay.screenShot(self,"IE",payment)
                    self.assertEqual(self.driver.title,webPay.enum(self,'paypage',payment),'没有进入对应支付方式页面'+payment)
                    #验证是否进入对应的支付页面
                except Exception as e:
                    print('Reason:', e)

                self.driver.close()
                self.driver.switch_to.window(nowHandle)
                time.sleep(1)
                self.driver.find_element_by_id('kz_pay_id').click()

            if payment=='固定电话':
                links=['固定电话和手机支付(电信&联通)','电信固定电话充值']
                for link in links:
                    self.driver.find_element_by_link_text(link).click()
                    self.select_server()
                    self.driver.find_element_by_id("payFormSubmitBtn").click()
                    time.sleep(2)
                    webPay.switch_to_newPage(self,nowHandle)
                    time.sleep(10)
                    try:
                        print(self.driver.title)
                        webPay.screenShot(self,"IE",link)
                        self.assertEqual(self.driver.title,webPay.enum(self,'paypage',link),'没有进入对应支付方式页面'+link)
                        #验证是否进入对应的支付页面
                    except Exception as e:
                        print('Reason:', e)

                    self.driver.close()
                    self.driver.switch_to.window(nowHandle)
                    time.sleep(1)
                    self.driver.find_element_by_id('kz_pay_id').click()

            if payment=='港澳台充值':
                links=['PayPal','信用卡','WebATM','點卡&會員儲值','電信小額支付']
                for link in links:
                    self.driver.find_element_by_link_text(link).click()
                    self.select_server()
                    self.driver.find_element_by_id("payFormSubmitBtn").click()
                    time.sleep(2)
                    webPay.switch_to_newPage(self,nowHandle)
                    time.sleep(15)
                    try:
                        print(self.driver.title)
                        webPay.screenShot(self,"IE",link)
                        self.assertEqual(self.driver.title,webPay.enum(self,'paypage',link),'没有进入对应支付方式页面'+link)
                        #验证是否进入对应的支付页面
                    except Exception as e:
                        print('Reason:', e)

                    self.driver.close()
                    self.driver.switch_to.window(nowHandle)
                    time.sleep(1)
                    self.driver.find_element_by_id('kz_pay_id').click()

    def select_server(self):
    #选择充值服
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
