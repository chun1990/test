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

    def test_payCenter_page(self):

        """固定金额支付页面-支付渠道"""

        print('切换点击右方的支付渠道icon，左方显示相应的支付方式')
        print('-----------------------------------------------')
        self.driver.login()
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        #进入固定金额支付中心
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        self.driver.screenShot('固定金额支付中心')
        #获取支付中心页面截图

        list=self.driver.find_elements_by_id('ppsgame_qudao_name')
        for i in range(0,len(list)):
            #循环点击右方支付渠道列表的各个支付渠道icon
            text_qudao=list[i].text
            list[i].click()
            self.driver.screenShot('icon')
            time.sleep(2)
            print(text_qudao)
            text_channel=self.driver.find_element_by_id('payment_channel').text
            self.assertEqual(text_qudao,text_channel)
            if text_qudao in ('游戏卡','充值卡'):
                self.driver.find_element_by_id('payment_channel').click()

        self.driver.find_element_by_name('关闭').click()
        #点击关闭按钮，回到主界面
        self.driver.WaitId(30,'ppsgame_dialog_title')
        self.assertEqual('请确认是否退出支付中心',self.driver.find_element_by_id('ppsgame_dialog_message').text,'提示信息错误')
        self.driver.find_element_by_id('ppsgame_dialog_commint').click()
        self.assertEqual(self.driver.current_activity,'.activity.TestActivity','未回到主界面')



    def test_payCenter_payment(self):

        """遍历支付渠道进行支付"""

        print('切换选择支付渠道点击确认支付，进入对应充值页面')
        print('-----------------------------------------------------------------')
        self.driver.login()

        self.payCenter_weixin()
        time.sleep(2)
        self.driver.switch_to_activity('.activity.TestActivity')
        self.payCenter_aliplay()
        time.sleep(2)
        self.driver.switch_to_activity('.activity.TestActivity')
        self.payCenter_unionpay()
        time.sleep(2)
        self.driver.switch_to_activity('.activity.TestActivity')
        self.payCenter_tenpay()
        time.sleep(2)
        self.driver.switch_to_activity('.activity.TestActivity')
        self.payCenter_Alipayweb()
        time.sleep(2)
        self.driver.switch_to_activity('.activity.TestActivity')
        self.payCenter_Unionpayweb()



    def payCenter_weixin(self):
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('微信支付').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()
        self.driver.NotWaitId(20,'loading_text')
        time.sleep(2)
        try:
            self.driver.alert_is_present()
            self.driver.switch_to_alert()
            if self.driver.element_is_present('id','ppsgame_dialog_title'):
                #未安装微信客户端，点击支付按钮弹出提示框
                print('1、选择微信支付方式，未安装微信或者已经生成订单，弹出提示')
                self.driver.switch_to_alert()
                time.sleep(5)
                self.driver.screenShot('微信支付')
                message=self.driver.find_element_by_id('ppsgame_dialog_message').text
                self.assertTrue('交易状态:失败' in message,'弹出框提示信息错误')
                self.driver.find_element_by_name('确认').click()

            else:
                #已安装微信客户端，进入微信登录界面
                print('1、选择微信支付方式，进入微信登录界面')
                self.driver.WaitId(10,'text1')
                self.driver.screenShot('微信支付')
                current_activity=self.driver.current_activity
                self.assertTrue(current_activity in '.ui.account.SimpleLoginUI or .plugin.wallet.pay.ui.WalletPayUI','未进入微信登录界面')
                #进入微信支付页面
                self.driver.switch_to_activity('.activity.TestActivity')
                #返回到主界面
                print(self.driver.current_activity)

        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')

    def payCenter_aliplay(self):

        """支付宝客户端支付方式"""
        print('2、选择支付宝钱包，进入支付宝支付页面')
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('支付宝钱包').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()

        try:
            self.driver.alert_is_present()
            self.driver.switch_to_alert()
            time.sleep(5)
            current_activity=self.driver.current_activity
            if current_activity=='com.alipay.android.app.flybird.ui.window.FlyBirdWindowActivity':
                print('已安装支付宝客户端，弹出支付宝页面')

            else:
                print('未安装支付宝客户端，进入支付宝网页')
                self.assertEqual(self.driver.current_activity,'com.alipay.mobile.security.login.ui.AlipayUserLoginActivity','未进入支付宝支付页面')

            self.driver.screenShot('支付宝钱包')
            self.driver.switch_to_activity('.activity.TestActivity')

        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')

    def payCenter_unionpay(self):
        print('3、选择银行卡，进入银行卡支付页面')
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        self.driver.WaitId(30,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('银行卡').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()
        try:
            self.driver.NotWaitId(20,'loading_text')
            time.sleep(10)
            self.driver.screenShot('银行卡')
            current_activity=self.driver.current_activity
            self.assertEqual(current_activity,'com.unionpay.uppay.PayActivity')
            #进入网银支付页面
            self.driver.switch_to_activity('.activity.TestActivity')
            #返回到主界面
        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')


    def payCenter_tenpay(self):
        print('4、选择财付通，进入财付通支付网页')
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('财付通网页').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()
        time.sleep(5)
        try:
            self.driver.NotWaitId(20,'loading_text')
            time.sleep(5)
            #等待页面加载完成
            self.assertEqual(self.driver.find_element_by_id('title').text,'充值中心','未进入充值页面')
            self.driver.screenShot('财付通')

            self.driver.switch_to_activity('.activity.TestActivity')
            #返回到主界面
        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')

    def payCenter_Alipayweb(self):
        print('5、选择支付宝网页，进入支付宝网页')
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('支付宝网页').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()
        time.sleep(5)
        try:
            self.driver.NotWaitId(20,'loading')
            time.sleep(5)
            self.driver.screenShot('支付宝网页')
            #print(self.driver.find_element_by_id('title').text)
            self.assertEqual(self.driver.find_element_by_id('title').text,'充值中心','未进入充值页面')

            self.driver.switch_to_activity('.activity.TestActivity')
                #返回到主界面
        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')

    def payCenter_Unionpayweb(self):
        print('6、选择银联网页，进入银联支付网页')
        self.driver.find_element_by_id('button_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入固定支付页面')
        self.driver.WaitId(40,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('银联网页').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()
        time.sleep(10)
        try:
            self.driver.NotWaitId(20,'loading')
            self.driver.WaitId(20,'title')
            #print(self.driver.find_element_by_id('title').text)
            self.assertEqual(self.driver.find_element_by_id('title').text,'充值中心','未进入充值页面')
            self.driver.screenShot('银联网页')

        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')


if __name__ == "__main__":
    unittest.main()








