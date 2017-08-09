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

    def test_buttonPayment_voucher(self):

        """固定支付-代金券抵扣"""

        print('固定金额页面，使用代金券抵扣，实际支付金额及抵扣金额显示正确')
        print('---------------------------------------------------------------------------')

        self.driver.login()
        self.driver.find_element_by_id('button_payment').click()
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        time.sleep(1)
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity)
        #进入固定金额支付中心
        payment_money=self.driver.find_element_by_id('payment_money').text#充值金额
        discount_money=self.driver.find_element_by_id('game_discount_count').text#抵扣金额

        self.driver.find_element_by_name('我的优惠').click()
        time.sleep(5)
        self.driver.screenShot('固定支付-代金券')
        if not self.driver.element_is_present('id','payment_dicount_voucher'):
            print('该用户没有代金券，抵扣金额为0')
            real_money=self.driver.find_element_by_id('payment_bottom_money').text#实际金额
            money=int(payment_money[1:])-int(discount_money[2:])
            self.assertEqual(int(real_money[1:]),money)
            #支付金额显示正确
        else:
            self.driver.find_element_by_id('payment_dicount_voucher').click()
            self.driver.WaitId(15,'voucher_validitytime')
            self.assertEqual(self.driver.find_elements_by_id('voucher_textview')[-1].text,'不抵扣','不抵扣选项未显示')
            list=self.driver.find_element_by_id('voucher_gridview').find_elements_by_id('voucher_textview')
            print('点击我的优惠中的代金券,查看代金券抵扣金额及实际充值金额是否正确')
            for i in range(0,len(list)):

                voucher_money=list[i].text
                #代金券金额
                list[i].click()
                discount_money=self.driver.find_element_by_id('game_discount_count').text
                #抵扣金额
                real_money=self.driver.find_element_by_id('payment_bottom_money').text
                #实际金额
                print(voucher_money,discount_money,real_money)

                money=int(payment_money[1:])-int(voucher_money[1:])
                    #实际充值金额=充值金额-抵扣金额
                self.assertEqual(money,int(real_money[1:]),'实际充值金额显示错误')
                self.assertEqual(discount_money[2:],voucher_money[1:],'优惠抵扣金额显示错误')
                time.sleep(1)

            self.driver.find_element_by_name('不抵扣').click()
            real_money1=self.driver.find_element_by_id('payment_bottom_money').text
            discount_money1=self.driver.find_element_by_id('game_discount_count').text
            self.assertEqual(discount_money1[2:],'0','优惠抵扣金额显示错误')
            self.assertEqual(payment_money[1:],real_money1[1:],'选择不抵扣，支付金额显示错误')

        self.driver.find_element_by_name('关闭').click()
        #点击关闭按钮，回到主界面
        self.driver.WaitId(10,'ppsgame_dialog_title')
        self.assertEqual('请确认是否退出支付中心',self.driver.find_element_by_id('ppsgame_dialog_message').text)
        self.driver.find_element_by_id('ppsgame_dialog_commint').click()
        self.assertEqual(self.driver.current_activity,'.activity.TestActivity')

    def test_arbitray_voucher(self):

        """任意支付-代金券抵扣"""

        print('任意金额页面，使用代金券抵扣，查看实际支付金额及抵扣金额显示正确')
        print('-------------------------------------------------------------------------')

        self.driver.login()
        self.driver.find_element_by_id('button_any_payment').click()
        time.sleep(1)
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入任意支付页面')
        #进入任意金额支付中心
        self.driver.WaitId(30,'payment_input_moneygridview')
        time.sleep(1)
        self.driver.find_element_by_id('payment_order_layout').click()
        time.sleep(3)
        self.driver.find_element_by_name('1000元').click()
        time.sleep(2)
        payment_money=self.driver.find_element_by_id('payment_money').text#充值金额
        discount_money=self.driver.find_element_by_id('game_discount_count').text#抵扣金额
        self.driver.find_element_by_name('我的优惠').click()
        time.sleep(3)
        self.driver.screenShot('任意支付-代金券')
        if not self.driver.element_is_present('id','payment_dicount_voucher'):
            print('该用户没有代金券，抵扣金额为0')
            real_money=self.driver.find_element_by_id('payment_bottom_money').text#实际金额
            money=int(payment_money[1:])-int(discount_money[2:])
            self.assertEqual(int(real_money[1:]),money)
            #支付金额显示正确
        else:
            self.driver.find_element_by_id('payment_dicount_voucher').click()
            self.driver.WaitId(20,'voucher_validitytime')
            self.assertEqual(self.driver.find_elements_by_id('voucher_textview')[-1].text,'不抵扣','不抵扣选项未显示')
            list=self.driver.find_element_by_id('voucher_gridview').find_elements_by_id('voucher_textview')
            print('点击我的优惠中的代金券,查看代金券抵扣金额及实际充值金额是否正确')
            for i in range(0,len(list)):

                voucher_money=list[i].text
                #代金券金额
                list[i].click()
                discount_money=self.driver.find_element_by_id('game_discount_count').text
                #抵扣金额
                real_money=self.driver.find_element_by_id('payment_bottom_money').text
                #实际金额
                print(voucher_money,discount_money,real_money)
                money=int(payment_money[1:])-int(voucher_money[1:])
                    #实际充值金额=充值金额-抵扣金额
                self.assertEqual(money,int(real_money[1:]),'实际充值金额显示错误')
                self.assertEqual(discount_money[2:],voucher_money[1:],'优惠抵扣金额显示错误')
                time.sleep(1)

            self.driver.find_element_by_name('不抵扣').click()
            real_money1=self.driver.find_element_by_id('payment_bottom_money').text
            discount_money1=self.driver.find_element_by_id('game_discount_count').text
            self.assertEqual(discount_money1[2:],'0','优惠抵扣金额显示错误')
            self.assertEqual(payment_money[1:],real_money1[1:],'选择不抵扣，支付金额显示错误')


if __name__ == "__main__":
    unittest.main()


