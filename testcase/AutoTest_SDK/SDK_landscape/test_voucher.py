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


    def test_voucher(self):

        """代金券页面校验"""

        print('进入代金券页面，查看该用户代金券')
        print('------------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        UID=self.driver.find_element_by_id('nine_grid_account').text
        self.driver.find_element_by_name('福利').click()
        self.driver.WaitId(15,'title_bar_title')
        #点击福利图标
        self.assertEqual(self.driver.find_element_by_id('title_bar_title').text,'福利','未进入福利页面')
        self.driver.find_element_by_name('代金券').click()
        time.sleep(5)
        self.driver.screenShot('代金券页面')
        if self.driver.element_is_present('id','no_data_icon'):
            print('代金券页面为空')
            now =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            num_voucher=self.driver.selectSQL('SELECT COUNT(user_id) FROM game_user_voucher WHERE user_id="'+UID+'"and use_status=0 and game_id=10003 and expire_at>="'+now+'"','vip_game_pps_tv')
            #print(num_voucher)
            self.assertEqual(num_voucher[0][0],int('0'),'该用户代金券数目不会0')
        else:
            print('代金券页面不为空')

if __name__ == "__main__":
    unittest.main()


