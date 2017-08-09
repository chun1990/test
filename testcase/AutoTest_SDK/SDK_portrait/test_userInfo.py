__author__ = 'zhangchun'

import os
import unittest
from appium import webdriver
from framework import android

import time


class AndroidTests(unittest.TestCase):
    def setUp(self):
        self.driver =android.Android(__file__)

    def tearDown(self):

        self.driver.quit()
        #self.driver.remove_app('com.ppsgame.sdk')

    def test_userInfo_page(self):

        """验证启动自动登录功能"""

        print('查看侧边栏-个人账号，进入个人信息页面，遍历点击各页面')
        print('--------------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        self.driver.screenShot('侧边栏')
        UID=self.driver.find_element_by_id('nine_grid_account').text
        username=self.driver.find_element_by_id('nine_grid_phone').text
        #获取用户的user_id及昵称并打印
        print(UID,username)
        self.driver.find_element_by_id('nine_grid_user_icon').click()
        time.sleep(2)
        self.driver.screenShot('个人信息')
        buttons1=['充值查询','修改密码','常见问题']
        buttons2=['充值查询','绑定手机','常见问题']
        if self.driver.element_is_present('id','user_center_bind_phone'):

            for button in buttons2:
                #遍历点击个人信息的三个页面，并进行截图
                self.driver.find_element_by_name(button).click()
                time.sleep(5)
                title=self.driver.find_element_by_id('title').text
                self.driver.screenShot(button)
                self.assertEqual(title,button,'未进入对应界面')
                self.driver.find_element_by_id('slidebar_close_btn_2').click()
                time.sleep(2)
        else:
            for button in buttons1:
                #遍历点击个人信息的三个页面，并进行截图
                self.driver.find_element_by_name(button).click()
                time.sleep(5)
                title=self.driver.find_element_by_id('title').text
                self.driver.screenShot(button)
                self.assertEqual(title,button,'未进入对应界面')
                self.driver.find_element_by_id('slidebar_close_btn_2').click()
                time.sleep(2)

    def test_jiugonge(self):

        """遍历进入九宫格各页面"""

        print('查看侧边栏-九宫格，遍历点击各页面')
        print('-------------------------------------------------------------------')

        self.driver.login()
        #自动登录

        buttons=['论坛','消息盒','客服','福利']
        for i in range(0,len(buttons)):
            #遍历点击九宫格的各页面，并进行截图
            self.driver.slidebar()
                #点击侧边栏
            self.driver.find_element_by_name(buttons[i]).click()
            time.sleep(6)
            title=self.driver.find_element_by_id('title_bar_title').text
            self.driver.screenShot(buttons[i])
            print(title,buttons[i])
            self.assertEqual(title,buttons[i],'未进入对应界面')
            self.driver.find_element_by_id('title_bar_close_icon').click()
            time.sleep(2)



if __name__ == "__main__":
    unittest.main()






