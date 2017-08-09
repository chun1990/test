# coding=utf-8
import time
import unittest
from framework import webPay
import os
from selenium import webdriver


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
#取当前文件所在目录的上一级目录

class TestCase(unittest.TestCase):

    def setUp(self):  #初始化
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(20)

    def tearDown(self):
        self.driver.quit()


    def test_noaccount (self):

        """充值用户为空，点击充值按钮，弹出提示框：账号不能为空"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(1)
        self.driver.find_element_by_id('server_list').find_element_by_id(webPay.config(self,'setting','server_id')).click()
        self.driver.find_element_by_id('server_1580501').click()
        time.sleep(1)
        self.driver.find_element_by_id("payFormSubmitBtn").click()
        alert=self.driver._switch_to.alert
        self.assertEqual(u"账号不能为空", alert.text,u'未出现弹出框或弹出框提示不正确')
        time.sleep(1)
        alert.accept()



    def test_noSelectServer(self):

        """未选择充值服务器，点击充值按钮，弹出提示框：没有选择服务器"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        server=self.driver.find_element_by_id('server-tit').text
        if server==u"选择充值服务器":
            try:
                self.driver.find_element_by_id("payFormSubmitBtn").click()
                time.sleep(3)
                alert=self.driver._switch_to.alert
                self.assertEqual(u"没有选择服务器", alert.text,u'未出现弹出框或弹出框提示不正确')
                time.sleep(1)
                alert.accept()
                #无法充值，弹出提示框
            except Exception as e:
                print('Reason:', e)
                #捕获所有异常并打印
        else:
            print(u'已选择充值服务器')
            pass

    def test_noRole(self):

        """用户在充值服务器下未创建角色，点击充值按钮，提示未创建角色，无法充值"""

        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(1)
        self.driver.find_element_by_id('server_list').find_element_by_id('server_tab_2').click()
        server_select=self.driver.find_element_by_id("server_15806302").text
        self.driver.find_element_by_id('server_15806302').click()
        server_box=self.driver.find_element_by_id('server-tit').text
        self.assertEqual(server_box,server_select,u'选择充值服务器失败')
        wrong=self.driver.find_element_by_id("wrong_id").text

        if  wrong==u"您的账号不存在或没有在该服创建角色":
        #若该充值服务器下未创建角色，服务器下会显示提示信息
            try:
                self.driver.find_element_by_id("payFormSubmitBtn").click()
                time.sleep(3)
                alert=self.driver._switch_to.alert
                self.assertEqual(u"您的账号不存在或没有在该服创建角色", alert.text,u'未出现弹出框或弹出框提示不正确')
                time.sleep(1)
                alert.accept()
                #无法充值，弹出提示框
            except Exception as e:
                print('Reason:', e)
        else:
            print(u'该服已创建角色')

if __name__ == "__main__":
    unittest.main()



