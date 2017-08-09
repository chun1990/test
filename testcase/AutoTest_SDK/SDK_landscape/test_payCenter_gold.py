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

    def test_buttonPayment_gold(self):

        """固定支付-金币抵扣"""

        print('固定金额页面，使用金币抵扣，查看实际支付金额及抵扣金额显示正确')
        print('-------------------------------------------------------------------------')

        self.driver.login()
        self.driver.find_element_by_id('button_payment').click()
        self.driver.WaitId(30,'ppsgame_qudao_logo')
        time.sleep(1)
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity)
        #进入固定金额支付中心
        payment_money=self.driver.find_element_by_id('payment_money').text#充值金额
        discount_money=self.driver.find_element_by_id('game_discount_count').text#抵扣金额
        self.driver.find_element_by_name('我的优惠').click()
        time.sleep(5)
        self.driver.screenShot('金币抵扣')
        if not self.driver.element_is_present('name','金币抵扣'):
            print('该用户没有金币，抵扣金额为0')
            real_money=self.driver.find_element_by_id('payment_bottom_money').text#实际金额
            money=int(payment_money[1:])-int(discount_money[2:])
            self.assertEqual(int(real_money[1:]),money,'支付金额显示错误')
        else:
            self.driver.find_element_by_id('payment_discount_point').click()
            textbox=self.driver.find_element_by_id('payment_point_edittext')
            gold_inputs=['0','999','1000','2050','5000','40000']
            for i in range (0,len(gold_inputs)):
                textbox.clear()
                textbox.send_keys(gold_inputs[i])
                self.driver.keyevent(4)
                time.sleep(2)
                self.driver.screenShot('金币抵扣-'+gold_inputs[i])
                gold_show=self.driver.find_element_by_id('payment_point_actual_count').text
                #金币抵扣
                count=self.driver.find_element_by_id('payment_point_alreadycount').text[:-1]
                #金额抵扣
                real_money=self.driver.find_element_by_id('payment_bottom_money').text[1:]
                #实际支付金额
                money=int(payment_money[1:])-int(count)
                if int(gold_inputs[i])<=int(payment_money[1:])*1000:
                    self.assertEqual(int(gold_show),int(int(gold_inputs[i])/1000)*1000,'金币显示错误')
                    self.assertEqual(int(count),int(int(gold_inputs[i])/1000),'金币抵扣金额错误')
                    self.assertEqual(int(real_money),int(money),'实际支付金额显示正确')
                else:
                    #输入抵扣金币大于可抵扣的金额
                    self.assertEqual(int(gold_show),int(payment_money[1:])*1000,'金币显示错误')
                    self.assertEqual(int(count),int(payment_money[1:]),'金币抵扣金额错误')
                    self.assertEqual(int(real_money),0,'实际支付金额显示正确')




    def test_arbitray_gold(self):

        """任意支付-金币抵扣"""

        print('任意金额页面，使用金币抵扣，查看实际支付金额及抵扣金额显示正确')
        print('-------------------------------------------------------------------------')

        self.driver.login()
        self.driver.find_element_by_id('button_any_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入任意支付页面')
        #进入任意金额支付中心
        self.driver.WaitId(20,'payment_input_moneygridview')
        time.sleep(1)
        self.driver.find_element_by_name('请输入金额').click()
        self.driver.find_element_by_id('payment_input_edittext').clear()
        self.driver.find_element_by_id('payment_input_edittext').send_keys(50)
        self.driver.keyevent(4)
        time.sleep(2)
        self.driver.find_element_by_name('确认').click()
        time.sleep(2)
        payment_money=self.driver.find_element_by_id('payment_money').text#充值金额
        discount_money=self.driver.find_element_by_id('game_discount_count').text#抵扣金额
        self.driver.find_element_by_name('我的优惠').click()
        time.sleep(5)
        self.driver.screenShot('金币抵扣')
        if not self.driver.element_is_present('name','金币抵扣'):
            print('该用户没有金币，抵扣金额为0')
            real_money=self.driver.find_element_by_id('payment_bottom_money').text#实际金额
            money=int(payment_money[1:])-int(discount_money[2:])
            self.assertEqual(int(real_money[1:]),money,'支付金额显示错误')
        else:
            self.driver.find_element_by_id('payment_discount_point').click()

            textbox=self.driver.find_element_by_id('payment_point_edittext')
            gold_inputs=['0','999','1000','2050','5000','60000']
            for i in range (0,len(gold_inputs)):
                textbox.clear()
                textbox.send_keys(gold_inputs[i])
                self.driver.keyevent(4)
                time.sleep(2)
                self.driver.screenShot('金币抵扣-'+gold_inputs[i])
                gold_show=self.driver.find_element_by_id('payment_point_actual_count').text
                #金币抵扣
                count=self.driver.find_element_by_id('payment_point_alreadycount').text[:-1]
                #金额抵扣
                real_money=self.driver.find_element_by_id('payment_bottom_money').text[1:]
                #实际支付金额
                money=int(payment_money[1:])-int(count)
                if int(gold_inputs[i])<=int(payment_money[1:])*1000:
                    self.assertEqual(int(gold_show),int(int(gold_inputs[i])/1000)*1000,'金币显示错误')
                    self.assertEqual(int(count),int(int(gold_inputs[i])/1000),'金币抵扣金额错误')
                    self.assertEqual(int(real_money),int(money),'实际支付金额显示正确')
                else:
                    #输入抵扣金币大于可抵扣的金额
                    self.assertEqual(int(gold_show),int(payment_money[1:])*1000,'金币显示错误')
                    self.assertEqual(int(count),int(payment_money[1:]),'金币抵扣金额错误')
                    self.assertEqual(int(real_money),0,'实际支付金额显示正确')

if __name__ == "__main__":
    unittest.main()

