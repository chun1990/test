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


    def test_virtual(self):

        """虚拟卡页面校验"""

        print('进入虚拟卡页面，查看该用户虚拟卡')
        print('-------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        UID=self.driver.find_element_by_id('nine_grid_account').text
        self.driver.find_element_by_name('福利').click()
        self.driver.WaitId(15,'title_bar_title')
        #点击福利图标
        self.assertEqual(self.driver.find_element_by_id('title_bar_title').text,'福利','未进入福利页面')
        self.driver.find_element_by_name('虚拟卡').click()
        virtuals_name=self.driver.selectSQL('SELECT b.card_name FROM game_cardsys_number a,game_cardsys_info b WHERE a.user_id="'+UID+'"AND a.card_id=b.card_id AND b.type=1 AND a.hide=0','libao_game_pps_tv')
        virtual_sql=[]
        for virtual_name in virtuals_name :
            virtual_sql.append(virtual_name[0])
            #获取数据库中当前用户的所有虚拟卡

        if len(virtual_sql)==0:
            print('当前用户没有虚拟卡')
            self.driver.WaitId(40,'no_data_icon')
            self.driver.screenShot('虚拟卡页面')
            self.driver.element_is_present('id','no_data_icon')

        else:
            #若礼包页面有礼包，则滑动页面获取所有礼包卡号
            self.driver.WaitId(40,'virtual_card_title')
            self.driver.screenShot('虚拟卡页面')
            #num=self.driver.find_elements_by_id('virtual_card_title')
            virtual_show=self.driver.swipe_load_item(30,'virtual_card_title')
            #向下滑动页面，获取页面上的所有虚拟卡name

            print(virtual_sql,virtual_show)
            self.assertTrue(self.driver.contrast_elem(virtual_sql,virtual_show),'虚拟卡显示错误')
            #比较virtual_show,virtual_name


if __name__ == "__main__":
    unittest.main()









