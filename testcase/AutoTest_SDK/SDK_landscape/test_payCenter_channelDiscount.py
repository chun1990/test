__author__ = 'zhangchun'

import os
import unittest
from appium import webdriver
from framework import android
import time
import math

class AndroidTests(unittest.TestCase):
    def setUp(self):
        self.driver =android.Android(__file__)

    def tearDown(self):
        self.driver.quit()
        #self.driver.remove_app('com.ppsgame.sdk')

    def test_buttonPayment_channelDiscount(self):

        """固定金额支付页面-渠道折扣"""

        print('验证固定支付页面各打折渠道抵扣金额是否正确')
        print('---------------------------------------------------------------')
        self.driver.login()
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        #进入固定金额支付中心
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        time.sleep(3)
        if self.driver.element_is_present('name','有折扣'):
            #查看页面是否有打折的渠道，若有则验证所有折扣金额是否正确
            eles=self.driver.find_elements_by_id('ppsgame_qudao_discount')
            for i in range(0,len(eles)):
                eles[i].click()
                payment_money=self.driver.find_element_by_id('payment_money').text
                #充值金额
                discount_money=self.driver.find_element_by_id('game_discount_count').text
                #渠道抵扣金额
                real_money=self.driver.find_element_by_id('payment_bottom_money').text
                #实际金额
                money1=int(payment_money[1:])-int(discount_money[2:])
                #实际充值金额=充值金额-抵扣金额
                self.assertEqual(money1,int(real_money[1:]),'实际充值金额显示错误')
                self.driver.find_element_by_name('我的优惠').click()
                self.driver.find_element_by_name('限时优惠').click()
                time.sleep(2)
                discount=self.driver.find_element_by_id('channel_discount_textview').text[2]

                money2=int(int(payment_money[1:])*int(discount)/10)
                #计算充值金额*折扣后向下取整
                print(discount,payment_money[1:],money2)
                self.assertEqual(money2,int(real_money[1:]),'实际充值金额计算错误')
                time.sleep(1)
                self.driver.find_element_by_id('payment_channel_choose_layout').click()
                time.sleep(2)
        else:
            print('没有渠道做打折活动')




    def test_arbitray_channelDiscount(self):

        """任意支付页面-渠道折扣"""

        print('验证任意支付页面各打折渠道抵扣金额是否正确')
        print('---------------------------------------------------------------')
        self.driver.login()
        self.driver.find_element_by_id('button_any_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入任意支付页面')
        #进入任意金额支付中心
        self.driver.WaitId(30,'payment_input_moneygridview')
        time.sleep(1)
        self.driver.find_element_by_id('payment_order_layout').click()
        list=self.driver.find_elements_by_id('ppsgame_payment_money')

        for i in range(0,len(list)):

            list[i].click()
            time.sleep(1)
            self.driver.find_element_by_name('支付方式').click()
            self.driver.WaitId(20,'ppsgame_qudao_logo')
            time.sleep(3)
            if self.driver.element_is_present('name','有折扣'):
                print('有渠道折扣活动')
                #查看页面是否有打折的渠道，若有则验证所有折扣金额是否正确
                eles=self.driver.find_elements_by_id('ppsgame_qudao_discount')
                for i in range(0,len(eles)):
                    eles[i].click()
                    payment_money=self.driver.find_element_by_id('payment_money').text
                    #充值金额
                    discount_money=self.driver.find_element_by_id('game_discount_count').text
                    #渠道抵扣金额
                    real_money=self.driver.find_element_by_id('payment_bottom_money').text
                    #实际金额
                    money1=int(payment_money[1:])-int(discount_money[2:])
                    #实际充值金额=充值金额-抵扣金额
                    self.assertEqual(money1,int(real_money[1:]),'实际充值金额显示错误')
                    self.driver.find_element_by_name('我的优惠').click()
                    self.driver.find_element_by_name('限时优惠').click()
                    time.sleep(2)
                    discount=self.driver.find_element_by_id('channel_discount_textview').text[2]
                    #抵扣金额
                    money2=math.ceil(float(payment_money[1:])*int(discount)/10)
                    #计算充值金额*折扣后向下取整
                    print(discount,payment_money[1:],money2)
                    self.assertEqual(money2,int(real_money[1:]),'实际充值金额计算错误')
                    time.sleep(1)
                    self.driver.find_element_by_id('payment_channel_choose_layout').click()
                    time.sleep(1)

                self.driver.find_element_by_id('payment_order_layout').click()
            else:
                print('没有渠道做打折活动')
                break


if __name__ == "__main__":
    unittest.main()






