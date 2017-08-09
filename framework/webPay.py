___author__ = 'zhangchun'

# coding=utf-8
import os
import time
from selenium import webdriver
from selenium.common.exceptions import *
import configparser
import pymysql


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
#取当前文件所在目录的上一级目录


def get_value(self):
    cookies = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
    print (cookies)
    for cookie in cookies:
        if cookie.split('=')[0]=='P00001':
            value=cookie.split('=')
            return value


def screenShot(self,browser,name):
    #截图并保存在screenshot目录下
    now =time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
    #获取当前时间并格式化
    image=PATH("../screenshot/"+browser +"/"+now+"_"+name+".jpg")
    self.driver.save_screenshot(image)
    print(image)


def banktitle(self):
    #获取当前页面加载完成后的title
    time_out=80
    elm=u'支付宝 - 网上支付 安全快速！'
    while time_out > 0:
        if len(self.driver.title)>1 and self.driver.title!=elm:
           # print(self.driver.title)
            return self.driver.title
        time_out -= 1
        time.sleep(0.5)
    else:
        pass
            #raise (NameError, 'switch timeout')

def switch_to_newPage(self,nowhandle):
    #跳转到当前的页面窗口
    try:
        allhandles=self.driver.window_handles
        for handle in allhandles:
            if len(handle)>1 and handle !=nowhandle:
                self.driver.switch_to.window(handle)
    except TimeoutError:
            pass


def enum(self,key,val):
    bank_enum = {
#设置枚举型
        'channel':{
            '网上银行':'网上银行','支付宝':'支付宝','微信支付':'微信支付','PayPal':'PayPal',
            '神州行移动卡':'神州行移动卡','财付通':'财付通','游戏卡':'骏卡','固定电话':'固定电话和手机支付(电信&联通)',
            '港澳台充值':'PayPal', '联通卡':'19pay联通卡','电信卡':'19pay电信卡'
        },
        'paypage':{
            '支付宝':'支付宝 - 网上支付 安全快速！','PayPal':'PayPal结账 - 登录','神州行移动卡':'卡兑换平台',
            '财付通':'财付通 - 支付中心','联通卡':'卡兑换平台','电信卡':'卡兑换平台',
            '固定电话和手机支付(电信&联通)':'[支付申请]','电信固定电话充值':'易充-支付信息',
            '信用卡':'GASH','WebATM':'GASH','點卡&會員儲值':'Global Payment System',
            '電信小額支付':'Global Payment System'
        },
        'bank':{
            'CCB':u'中国建设银行 个人网上银行','ICBC':u'中国工商银行网上银行',
            'ABC':u'中国农业银行 - 网上支付中心','PSBC':u'',
            'BOC':u'中国银行-在线支付','CMB':'招商银行网上支付',
            'COMM':u'交通银行网上支付','CEB':u'支付宝 - 网上支付 安全快速！',
            'CIB':u'兴业银行网上支付','GDB':u'广发银行支付网关',''
            'SPABANK':u'平安银行—网上支付','SDB':u'平安银行—网上支付',
            'SPDB':u'浦发银行支付登录','CMBC':u'中国民生银行网上支付',
            'CITIC':u'','NBBANK':u'宁波银行支付平台',
            'SHBANK':u'上银快付','BJRCB':u'北京农商银行 - 电子支付系统',
            'BJBANK':u'北京银行网上支付','HZCB':u'杭州银行支付平台',
            'SHRCB':u'上海农商银行网上支付','FDB':u'富滇银行网上支付',
            'NJCB':u'南京银行个人网上银行','CBHB':u'渤海银行-网上支付中心',
            'HKBEA':u'东亚中国-网上支付系统'
        }
    }
    return bank_enum[key][str(val)]


def alert_is_present(self):
    """ Expect an alert to be present."""
    try:
        alert = self.driver.switch_to.alert
        print(alert.text)
        return True
    except NoAlertPresentException:
        return False


def close_allAlert(self):

    while alert_is_present(self):
        alert = self.driver.switch_to.alert
        alert.accept()



def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
            return True
        except NoSuchElementException:
            return False


def config(self,sections,option):
    config = configparser.ConfigParser()
    config.read(PATH("../manifest/webpay.ini"))
    b=config.get(sections,option)
    return b

def selectSQL(self, sql,data):
    '''
    mysql数据查询，查询多条数据
    '''
    # db_array = self.config('database')
    # dbs = db_array.split(',')
    dbm = pymysql.connect(host='10.221.48.17',user='game_testDb',passwd='Hl+DEIb3',db=data,port=int(8581),charset='utf8')
        #获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
    cu = dbm.cursor()
        #获取一个游标
    cu.execute(sql)
        #查询操作
    r = cu.fetchall()

    cu.close()
    dbm.close()
        #关闭库表
    return r

def fetchall(self, sql):
    '''查询所有数据'''
    if sql is not None and sql != '':
        cu = self.cursor()
        cu.execute(sql)
        r = cu.fetchall()
        cu.close()
        if len(r) > 0:
            return r
                # for e in range(len(r)):
                #     print(r[e])
    else:
        return None

def fetchone(self, sql, data):
    '''查询一条数据'''
    if sql is not None and sql != '':
        if data is not None:
                #Do this instead
            d = (data,)
            cu = self.cursor()
            cu.execute(sql, d)
            r = cu.fetchall()
            cu.close()
            if len(r) > 0:
                for e in range(len(r)):
                    print(r[e])
        else:
            print('the [{}] equal None!'.format(data))
    else:
        print('the [{}] is empty or equal None!'.format(sql))


