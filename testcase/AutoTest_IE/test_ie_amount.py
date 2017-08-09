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

    def test_amount(self):

        """
        充值金额输入错误，提示框验证
        ①金额为小数、
        ②不是10的倍数、
        ③小于10、
        ④大于100000、
        ⑤字母、汉字，
        ⑥为空
        ⑦为0
        """


        base_url=webPay.config(self,'setting','url')
        self.driver.get(base_url)
        self.driver.find_element_by_id('account_id').send_keys('zhifuceshi')
        self.driver.find_element_by_id('serverListTitleLink').click()
        time.sleep(1)
        self.driver.find_element_by_id('server_list').find_element_by_id(webPay.config(self,'setting','server_id')).click()
        self.driver.find_element_by_id('server_1580501').click()

        time.sleep(1)
        moneylist=['.5','35','8','100001','aaa',u'十','0','']
        for money in moneylist:
            #遍历输入数组moneylist中的元素
            moneyBox=self.driver.find_element_by_id('more_money')
            moneyBox.send_keys(Keys.CONTROL,'a')
            moneyBox.send_keys(money+Keys.ENTER)
            self.driver.find_element_by_id("payFormSubmitBtn").click()
            time.sleep(2)
            try:
                alert=self.driver._switch_to.alert
                #获取弹出框
                self.assertTrue(alert.text in "充值金额是10的整数倍 or 充值金额不能小于10，且为10的倍数，上限为100000",u'未出现弹出框或弹出框提示不正确')
                #验证弹出框的提示内容是否与预期相符
                alert.accept()
                #关闭弹出框
                time.sleep(1)
            except Exception as e:
                 print('Reason:'+money, e)


if __name__ == "__main__":
    unittest.main()
