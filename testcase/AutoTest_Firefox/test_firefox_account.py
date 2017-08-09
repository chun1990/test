__author__ = 'zhangchun'
# coding=utf-8

import time
import unittest
from framework import webPay
import os
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
#取当前文件所在目录的上一级目录


class TestCase(unittest.TestCase):

    def setUp(self):  #初始化
        self.driver=webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(20)


    def tearDown(self):
        self.driver.quit()


    def test_accountName(self):

        """登录g首页后，进入支付中心，支付页面显示充值账号为当前登录账号"""

        base_url="http://g.pps.tv/"
        self.driver.get (base_url)
            #打开G首页
        if webPay.is_element_present(self,'id','login_btn'):
                #若G首页在未登录状态，执行登录操作
            self.driver.find_element_by_id('user_name_login').clear()
            self.driver.find_element_by_id('user_name_login').send_keys('zhifuceshi'+Keys.ENTER)
            time.sleep(2)
                    #输入用户名
            self.driver.find_element_by_id('user_pswd_login').clear()
            self.driver.find_element_by_id('user_pswd_login').send_keys('ppsadmin')
            time.sleep(2)
                    #输入密码
            self.driver.find_element_by_id('login_btn').click()
                    #点击登录按钮
            try:
                WebDriverWait(self.driver, 30).until(lambda driver :driver.find_element_by_link_text(u'zhifuceshi'))
                    #等待zhifuceshi文字出现后执行以下操作
                self.driver.get ("http://pay.game.pps.tv/")
                time.sleep(2)
                self.driver.find_element_by_id('jsby').find_element_by_link_text(u'花千骨').click()
                print(u"用户登录成功！")
            except :
                print(u"登录失败")
        else:
                #如G首页已在登录状态，直接跳转到支付中心
            self.driver.find_element_by_link_text(u'退出').is_display()
            self.driver.get ("http://pay.game.pps.tv/")
            time.sleep(2)
            self.driver.find_element_by_id('jsby').find_element_by_link_text(u'花千骨').click()
            print(u"用户已经登录！")
            account_name=self.driver.find_element_by_id("account_id").get_attribute("value")
            try:
                self.assertEqual(u'充值中心',self.driver.title ,u'跳转失败或页面显示有误')
                self.assertEqual('zhifuceshi',account_name,u'付款账号显示有误')
                #验证充值账号是否为zhifuceshi
            except NameError :
                print('switch timeout')


if __name__ == "__main__":
    unittest.main()


