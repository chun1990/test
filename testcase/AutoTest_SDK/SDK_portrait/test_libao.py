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


    def test_libaoPage(self):

        """礼包页面校验"""

        print('进入礼包页面，查看已上线礼包的数目及礼包名称是否正确')
        print('---------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        self.driver.find_element_by_name('福利').click()
        self.driver.WaitId(15,'title_bar_title')
        #点击福利图标
        self.driver.screenShot('福利')
        self.assertEqual(self.driver.find_element_by_id('title_bar_title').text,'福利','未进入福利页面')
        self.driver.find_element_by_name('礼包').click()

        libao_sql=self.libao()
        if len(libao_sql)==0:
            print('目前没有礼包上线')
            self.driver.WaitId(40,'no_data_icon')
            self.driver.screenShot('礼包页面')
            self.driver.element_is_present('id','no_data_icon')

        else:
            #若礼包页面有礼包，则滑动页面获取所有礼包卡号
            self.driver.WaitId(40,'gift_title')
            #name=self.driver.find_elements_by_id('gift_title')
            libao_show=self.driver.swipe_load_item(30,'gift_title')
            libao_sql=self.libao()
            print(libao_show,libao_sql)
            self.assertTrue(self.driver.contrast_elem(libao_show,libao_sql),'礼包显示错误')

    def libao(self):

        now =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        libao=self.driver.selectSQL('SELECT card_name from pps_card_info a where a.game_id=10003 and a.show_flag=1 and a.card_id not in (SELECT b.card_id from pps_card_info b where b.card_stattime>="'+now+'" or b.card_endtime<="'+now+'")','libao_game_pps_tv')
        list_libao=[]
        for i in libao :
            list_libao.append(i[0])

        return list_libao


    def test_cardNumber(self):

        """礼包卡号校验"""

        print('进入礼包页面，查看已领礼包的礼包卡号是否正确')
        print('--------------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        UID=self.driver.find_element_by_id('nine_grid_account').text
        self.driver.find_element_by_name('福利').click()
        self.driver.WaitId(15,'title_bar_title')
        #点击福利图标
        self.assertEqual(self.driver.find_element_by_id('title_bar_title').text,'福利','未进入福利页面')
        self.driver.find_element_by_name('礼包').click()
        libao_sql=self.libao()
        if len(libao_sql)==0:
            print('目前没有礼包上线')
            self.driver.WaitId(40,'no_data_icon')
            self.driver.screenShot('礼包页面')
            self.driver.element_is_present('id','no_data_icon')

        else:
            #若礼包页面有礼包，则滑动页面获取所有礼包卡号
            self.driver.WaitId(40,'gift_title')
            buttons=self.driver.find_elements_by_id('get_gift_btn')
            list_card=[]
            for i in range(0,len(buttons)):
                if buttons[i].text=='复制':
                    libao_name=self.driver.find_elements_by_id('gift_title')[i].text
                    self.driver.find_elements_by_id('gift_title')[i].click()
                    self.driver.WaitId(15,'title')
                    self.assertEqual(self.driver.find_element_by_id('title').text,'礼包详情')
                    card_number=self.driver.find_element_by_id('slidebar_gift_detail_gift_code').text
                    list_card.append(card_number)
                    card_num=self.driver.selectSQL('SELECT card_number FROM pps_card_new_number a,pps_card_info b WHERE a.get_user_id="'+UID+'" and a.card_id =b.card_id and b.card_name="'+libao_name+'"','libao_game_pps_tv')
                    print(card_num,card_num[0][0])
                    self.assertEqual(card_number,card_num[0][0],'礼包卡号错误')
                    self.driver.find_element_by_id('slidebar_close_btn_2').click()


    def test_libaoDetail(self):

        """礼包详情校验"""

        print('进入礼包页面，查看礼包详情及使用方式与后台配置的是否一致')
        print('---------------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        self.driver.find_element_by_name('福利').click()
        self.driver.WaitId(15,'title_bar_title')
        #点击福利图标
        self.assertEqual(self.driver.find_element_by_id('title_bar_title').text,'福利','未进入福利页面')
        self.driver.find_element_by_name('礼包').click()
        libao_sql=self.libao()
        if len(libao_sql)==0:
            print('目前没有礼包上线')
            self.driver.WaitId(40,'no_data_icon')
            self.driver.screenShot('礼包页面')
            self.driver.element_is_present('id','no_data_icon')

        else:
            #若礼包页面有礼包，则滑动页面获取所有礼包卡号
            self.driver.WaitId(40,'gift_title')
            libao=self.driver.find_elements_by_id('gift_title')

            for i in range(0,len(libao)):
                libao_name=libao[i].text
                libao[i].click()
                self.driver.WaitId(15,'title')
                self.driver.screenShot('列表详情页'+libao_name)
                self.assertEqual(self.driver.find_element_by_id('title').text,'礼包详情')
                gift_name=self.driver.find_element_by_id('slidebar_gift_detail_name').text
                gift_content=self.driver.find_element_by_id('slidebar_gift_detail_content').text
                gift_way=self.driver.find_element_by_id('slidebar_gift_detail_get_gift_way').text
                print(gift_name,gift_content,gift_way)
                card_details=self.driver.selectSQL('SELECT card_name,tpl_contents,use_method FROM pps_card_info_new WHERE card_name="'+libao_name+'"','libao_game_pps_tv')

                self.assertEqual(gift_name,card_details[0][0],'礼包名不正确')
                self.assertTrue(gift_content in card_details[0][1],'礼包详情不正确')
                self.assertTrue(gift_way in card_details[0][2],'礼包使用方式不正确')
                self.driver.find_element_by_id('slidebar_close_btn_2').click()



    def test_getLibao(self):

        """礼包领取验证"""

        print('进入礼包页面，点击领取按钮，成功领取礼包码')
        print('-----------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏
        self.driver.find_element_by_name('福利').click()
        self.driver.WaitId(15,'title_bar_title')
        #点击福利图标
        self.assertEqual(self.driver.find_element_by_id('title_bar_title').text,'福利','未进入福利页面')
        self.driver.find_element_by_name('礼包').click()
        time.sleep(5)
        libao_sql=self.libao()
        if len(libao_sql)==0:
            print('目前没有礼包上线')
            self.driver.WaitId(40,'no_data_icon')
            self.driver.screenShot('礼包页面')
            self.driver.element_is_present('id','no_data_icon')

        else:
            #若礼包页面有礼包，则滑动页面获取所有礼包卡号
            self.driver.WaitId(40,'gift_title')
            buttons=self.driver.find_elements_by_id('get_gift_btn')
            libao=self.driver.find_elements_by_id('gift_title')
            buttonName=['领取','淘号']
            for i in range(0,len(buttons)):
                libao_name=libao[i].text
                if buttons[i].text in buttonName:
                    buttons[i].click()
                    time.sleep(5)
                    self.driver.switch_to_alert()
                    self.driver.screenShot('礼包领取成功')
                    self.driver.WaitId(30,'game_getgameok_code_text')

                    cardName=self.driver.find_element_by_id('game_getgameok_code_text').text
                    print('礼包领取成功，礼包码：'+cardName)
                    self.driver.find_element_by_id('game_getgameok_copy_how_use').click()
                    self.driver.WaitId(30,'slidebar_gift_detail_name')
                    self.assertEqual(self.driver.find_element_by_id('title').text,'礼包详情','未进入详情页')
                    self.assertEqual(self.driver.find_element_by_id('slidebar_gift_detail_name').text,libao_name,'未进入对应的礼包详情页')
                    self.driver.find_element_by_id('slidebar_close_btn_2').click()
                    time.sleep(1)
                else:
                    print('该用户目前没有未领取的礼包')

if __name__ == "__main__":
    unittest.main()

















