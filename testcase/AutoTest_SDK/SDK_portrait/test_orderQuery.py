__author__ = 'zhangchun'

import os
import unittest
from appium import webdriver
from framework import android
import time
import datetime

class AndroidTests(unittest.TestCase):
    def setUp(self):
        self.driver =android.Android(__file__)

    def tearDown(self):
        self.driver.quit()

    def test_orderQuery(self):

        """验证当前用户订单显示"""

        print('查看侧边栏-个人账号-充值查询，验证各页面订单号是否显示正确')
        print('---------------------------------------------------------------------')

        self.driver.login()
        #自动登录
        self.driver.slidebar()
        #点击侧边栏

        UID=self.driver.find_element_by_id('nine_grid_account').text
        username=self.driver.find_element_by_id('nine_grid_phone').text
        #获取用户的user_id及昵称并打印
        print(UID,username)

        self.driver.find_element_by_id('nine_grid_user_icon').click()
        time.sleep(3)
        self.driver.find_element_by_name('充值查询').click()
        print(self.driver.current_activity)

        y=datetime.date.today().year
        m=datetime.date.today().month
        a1= datetime.datetime(y,m,1,00,00,00)#获取本月第一天时间
        a2=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#获取当前时间
        if m==1:
            b1=datetime.datetime(y-1,12,1,00,00,00)
        else:
            b1=datetime.datetime(y,m-1,1,00,00,00)
            #获取上月第一天时间

        if m==1:
            c1=datetime.datetime(y-1,11,1,00,00,00)
        else:
            c1=datetime.datetime(y,m-2,1,00,00,00)
            #获取前月第一天时间

        time_list=((str(a1),str(a2)),(str(b1),str(a1)),(str(c1),str(b1)))
        buttons=['本月','上月','前月']

        ids=['item_1','item_2','item_3']
        for i in range(0,len(buttons)):
            print('-----------------进入当前游戏-'+buttons[i]+'订单页面----------------')
            #遍历点击各月当前游戏获取订单号，并进行截图

            self.driver.find_element_by_name(buttons[i]).click()
            self.driver.find_element_by_name('当前游戏').click()

            print(time_list[i][0],time_list[i][1],UID)
            orders_sql=self.order_select(UID,time_list[i][0],time_list[i][1])
            #查询当前用户数据库中的订单

            if len(orders_sql)==0:
                print('当前游戏无订单')
                self.driver.WaitId(40,'no_data_icon')
                self.driver.screenShot(buttons[i])
                self.assertTrue(self.driver.find_element_by_id(ids[i]).find_element_by_id('no_data_icon').is_displayed(),'无订单时页面显示错误')
            else:
                self.driver.WaitId(40,'sliderbar_recharge_item_tf2')
                self.driver.screenShot(buttons[i])
                #Layout=self.driver.find_element_by_id(ids[i]).find_elements_by_id('sliderbar_recharge_item_tf3')
                orders=self.swipe_up(40,ids[i],'sliderbar_recharge_item_tf3')
                #向下滑动页面获取所有订单
                orders_show=[]
                for order in orders:
                    orders_show.append(order.split('：')[1])
                    #去掉"订单编号："
                print(orders_show,orders_sql)
                self.assertTrue(self.driver.contrast_elem(orders_show,orders_sql),'订单显示错误')
                #比较订单是否一致
                time.sleep(2)


        for i in range(0,len(buttons)):
            print('--------进入所有游戏-'+buttons[i]+'订单页面--------')
            #遍历点击各月所有游戏获取订单号，并进行截图
            self.driver.find_element_by_name(buttons[i]).click()
            time.sleep(2)
            self.driver.find_element_by_name('所有游戏').click()
            orders_sql=self.order_selectAll(UID,time_list[i][0],time_list[i][1])

            if len(orders_sql)==0:
                print('当前游戏无订单')
                self.driver.WaitId(40,'no_data_icon')
                self.driver.screenShot(buttons[i])
                self.assertTrue(self.driver.find_element_by_id(ids[i]).find_element_by_id('no_data_icon').is_displayed(),'无订单时页面显示错误')
            else:
                self.driver.WaitId(40,'sliderbar_recharge_item_tf2')
                self.driver.screenShot(buttons[i])
                #Layout=self.driver.find_element_by_id(ids[i]).find_elements_by_id('sliderbar_recharge_item_tf3')
                orders=self.swipe_up(40,ids[i],'sliderbar_recharge_item_tf3')
                #向下滑动页面获取所有订单
                orders_show=[]
                for order in orders:
                    orders_show.append(order.split('：')[1])
                    #去掉"订单编号：
                print(orders_show,orders_sql)
                self.assertTrue(self.driver.contrast_elem(orders_show,orders_sql),'订单显示错误')

                time.sleep(2)

    def swipe_up(self,page_size,ids,id):
        '''
        列表滑动，装载每一页的（订单号或虚拟卡、礼包号）
        '''
        datas = ()
        list=[]

        while page_size>0:

            sub_tup = ()
            a=self.driver.find_element_by_id(ids).find_elements_by_id(id)
            for i in range(0,len(a)):

                try:
                    sub_txt = a[i].text
                    sub_tup += (sub_txt,)
                    #将每一页的元素信息sub_txt装入元组中
                except :
                    pass

            if len(sub_tup) > 0 and sub_tup not in datas:
                #当下一页的元素信息与上一页的完全一致时，说明已滑动到最后一页，则退出滑动循环
                datas += (sub_tup,)
                #print(datas)
                #定位元素的原位置
                origin_el =a[-1]
                #定位元素要移动到的目标位置
                destination_el =a[0]
                #执行元素的移动操作
                self.driver.drag_and_drop(origin_el,destination_el)
                page_size -= 1
                time.sleep(3)
            else:
                break

        for i in range(0,len(datas)):
            #将元组中所有的元素存入list,去重
            for j in range(0,len(datas[i])):
                if datas[i][j] not in list:
                    list.append(datas[i][j])
                else:
                    pass
                j+=1
            i+=1
        return list

    def order_select(self,id,time_first,time_last):
        #查询数据库中该用户10003游戏的充值订单，time为本月或上月、前月
        orders_id=self.driver.selectSQL('SELECT order_id from pps_user_game_order where user_id="'+id+'" and order_status=1 and pay_date>="'+time_first+'" and pay_date<="'+time_last+'" and order_type=10003','pay_game_pps_tv')
        list_orderId=[]
        for order_id in orders_id :
            list_orderId.append(str(order_id[0]))
        return list_orderId

    def order_selectAll(self,id,time_first,time_last):
        #查询数据库中用户所有游戏的充值订单，time为本月或上月、前月
        orders_id=self.driver.selectSQL('SELECT order_id from pps_user_game_order where user_id="'+id+'"and order_status=1 and pay_date>="'+time_first+'" and pay_date<="'+time_last+'"','pay_game_pps_tv')
        list_orderId=[]
        for order_id in orders_id :
            list_orderId.append(str(order_id[0]))
        return list_orderId


if __name__ == "__main__":
    unittest.main()


