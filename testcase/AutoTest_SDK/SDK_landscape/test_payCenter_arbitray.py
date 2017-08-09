__author__ = 'zhangchun'

from selenium.webdriver.common.keys import Keys
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

    def test_payCenter_selectMoney(self):

        """任意金额支付页面-选择充值金额"""

        print('选择充值金额，充值金额显示正确')
        print('----------------------------------------------------------')
        self.driver.login()
        self.driver.find_element_by_id('button_any_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入任意支付页面')
        #进入任意金额支付中心
        self.driver.WaitId(20,'payment_input_moneygridview')
        time.sleep(1)
        self.driver.screenShot('任意金额支付中心')
        self.driver.find_element_by_name('请输入金额').click()
        self.driver.find_element_by_name('确认付款').click()
        time.sleep(6)
        self.driver.switch_to_alert()
        self.driver.screenShot('输入金额为空')
        self.assertEqual(self.driver.find_element_by_id('ppsgame_dialog_message').text,'请输入或指定一个金额','未显示弹出框')
        #未输入任何金额，直接点击确认付款按钮，弹出框错误提示框
        self.driver.find_element_by_name('确认').click()
        time.sleep(2)
        list=self.driver.find_elements_by_id('ppsgame_payment_money')
        for i in range(0,len(list)):
            money_selected=list[i].text
            list[i].click()
            time.sleep(1)
            payment_money=self.driver.find_element_by_id('payment_money').text
            print(money_selected,payment_money)
            self.assertEqual(payment_money[1:],money_selected[:-1],'选择充值金额，金额显示错误')
        #点击选择充值金额中的金额，左侧显示相应的金额


    def test_payCenter_inputMoney(self):

        """任意金额支付页面-输入充值金额"""

        print('选择充值金额，充值金额显示正确')
        print('--------------------------------------------------------------')
        self.driver.login()
        self.driver.find_element_by_id('button_any_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入任意支付页面')
        #进入任意金额支付中心
        self.driver.WaitId(40,'payment_input_moneygridview')
        time.sleep(1)
        self.driver.find_element_by_name('请输入金额').click()
        time.sleep(2)
        money_input=[3,0,10,99998,1000,1000000]
        money_show=['3','1','10','99998','1000','99999']
        for i in range(0,len(money_input)):
            self.driver.find_element_by_id('payment_input_edittext').clear()
            self.driver.find_element_by_id('payment_input_edittext').send_keys(money_input[i])
            self.driver.keyevent(4)
            time.sleep(2)
            self.driver.find_element_by_name('确认').click()
            self.driver.screenShot('输入支付金额')
            payment_money=self.driver.find_element_by_id('payment_money').text
            print(payment_money)
            self.assertEqual(money_show[i],payment_money[1:],'输入金额，金额显示错误')
            time.sleep(2)


    def test_payCenter_paymentProcess(self):

        """任意金额支付页面-正向支付流程"""

        print('选择充值金额、优惠、支付方式，查看支付流程是否正常')
        print('------------------------------------------------------------------------')
        self.driver.login()
        self.driver.find_element_by_id('button_any_payment').click()
        self.assertEqual('.activity.PaymentFragmentActivity',self.driver.current_activity,'未进入任意支付页面')
        #进入任意金额支付中心
        self.driver.WaitId(40,'payment_input_moneygridview')
        time.sleep(1)
        self.driver.find_element_by_name('请输入金额').click()
        time.sleep(2)
        self.driver.find_elements_by_id('ppsgame_payment_money')[3].click()
        time.sleep(2)
        self.driver.find_element_by_id('payment_channel_choose_layout').click()
        self.driver.WaitId(10,'ppsgame_qudao_logo')
        self.driver.find_element_by_name('支付宝钱包').click()
        time.sleep(2)
        self.driver.find_element_by_name('确认付款').click()
        #选择金额，支付方式，点击确认支付按钮
        time.sleep(2)
        try:
            self.driver.alert_is_present()
            self.driver.switch_to_alert()
            time.sleep(2)
            current_activity=self.driver.current_activity
            if current_activity=='com.alipay.android.app.flybird.ui.window.FlyBirdWindowActivity':
                print('已安装支付宝客户端，弹出支付宝页面')
                self.driver.screenShot('支付宝客户端支付页面')

            else:
                print('未安装支付宝客户端，进入支付宝网页')
                self.assertEqual(self.driver.current_activity,'com.alipay.mobile.security.login.ui.AlipayUserLoginActivity','未进入支付宝支付页面')
                self.driver.screenShot('支付宝网页支付页面')

        except Exception as e:
            print('Reason:', e)
            self.driver.screenShot('error')

if __name__ == "__main__":
    unittest.main()









