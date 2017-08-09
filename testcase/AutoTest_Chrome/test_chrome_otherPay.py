__author__ = 'zhangchun'
# coding=utf-8

import time
import unittest
from framework import webPay
from selenium import webdriver
import os



class TestCase(unittest.TestCase):

    def setUp(self):  #初始化
        chrome_driver = os.path.abspath(webPay.config(self,'driver_path','chrome'))
        os.environ["webdriver.chrome.driver"] = chrome_driver
           # 读取配置文件config中chromedriver文件位置，，创建chromeDriverServer的一个接口用于连接chrome
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.maximize_window()
        #浏览器最大化
        self.driver.set_page_load_timeout(20)
        #等待页面加载

    def tearDown(self):
        self.driver.quit()

    def test_otherPay(self):

        """支付中心页面切换点击左侧支付渠道，显示对应的页面"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        time.sleep(1)
        nowHandle=self.driver.current_window_handle
        #获取当前窗口句柄
        list_payment1=['网上银行','支付宝','微信支付','PayPal','神州行移动卡','财付通',
                       '游戏卡','固定电话','港澳台充值','联通卡','电信卡']
        list_payment2=['支付宝','PayPal','神州行移动卡','财付通','联通卡','电信卡']
        for payment in list_payment1:
            #遍历点击页面左侧的支付方式，查看是否切换到对应的页面
            self.driver.find_element_by_link_text(payment).click()
            time.sleep(2)
            try:
                self.assertTrue(webPay.enum(self,'channel',payment) in self.driver.find_element_by_class_name("open-tip").text)
            except:
                self.assertTrue(webPay.enum(self,'channel',payment) in self.driver.find_element_by_id('tags_list').text)
            webPay.screenShot(self,"Chrome",payment)
            #截取当前页面图片
            if payment in list_payment2:
                #若支付方式为list_payment2中的元素，选择充值服点击充值，并验证是否进入对应的充值页面
                self.select_server()
                #选择充值服务器
                self.driver.find_element_by_id("payFormSubmitBtn").click()
                time.sleep(2)


                try:
                    webPay.switch_to_newPage(self,nowHandle)
                    time.sleep(15)
                    print(self.driver.title)
                    webPay.screenShot(self,"Chrome",payment)
                    self.assertEqual(self.driver.title,webPay.enum(self,'paypage',payment),'没有进入对应支付方式页面'+payment)
                except Exception as e:
                    print('Reason:', e)
                    #捕获所有异常，并打印
                self.driver.close()
                time.sleep(1)
                self.driver.switch_to.window(nowHandle)
                time.sleep(1)
                self.driver.find_element_by_id('kz_pay_id').click()


            if payment=='固定电话':
                links=['固定电话和手机支付(电信&联通)','电信固定电话充值']
                for link in links:
                    self.driver.find_element_by_link_text(link).click()
                    time.sleep(2)
                    self.select_server()
                    self.driver.find_element_by_id("payFormSubmitBtn").click()
                    time.sleep(2)

                    try:
                        webPay.switch_to_newPage(self,nowHandle)
                        time.sleep(15)
                        print(self.driver.title)
                        webPay.screenShot(self,"Chrome",link)
                        self.assertEqual(self.driver.title,webPay.enum(self,'paypage',link),'没有进入对应支付方式页面'+link)
                    except Exception as e:
                        print('Reason:', e)

                    self.driver.close()
                    time.sleep(1)
                    self.driver.switch_to.window(nowHandle)
                    time.sleep(1)
                    self.driver.find_element_by_id('kz_pay_id').click()
                    time.sleep(1)

            if payment=='港澳台充值':
                links=['PayPal','信用卡','WebATM','點卡&會員儲值','電信小額支付']
                for link in links:
                    self.driver.find_element_by_link_text(link).click()
                    time.sleep(2)
                    self.select_server()
                    self.driver.find_element_by_id("payFormSubmitBtn").click()
                    time.sleep(2)

                    try:
                        webPay.switch_to_newPage(self,nowHandle)
                        time.sleep(15)
                        print(self.driver.title)
                        webPay.screenShot(self,"Chrome",link)
                        self.assertEqual(self.driver.title,webPay.enum(self,'paypage',link),'没有进入对应支付方式页面'+link)
                    except Exception as e:
                        print('Reason:', e)

                    self.driver.close()
                    self.driver.switch_to.window(nowHandle)
                    time.sleep(1)
                    self.driver.find_element_by_id('kz_pay_id').click()
                    time.sleep(1)

    def select_server(self):

        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        time.sleep(2)
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(2)
        self.driver.find_element_by_id('server_list').find_element_by_id(webPay.config(self,'setting','server_id')).click()
        self.driver.find_element_by_id('server_1580501').click()
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()

