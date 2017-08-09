__author__ = 'zhangchun'


import os
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import configparser
import pymysql




PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Android(WebDriver):

    def __init__(self,file):

        self.setting=file.split("\\")[-2]
        setting=self.setting
        desired_caps = {}
        desired_caps['platformName'] =self.config('platform_Name',setting)
        desired_caps['platformVersion'] = self.config('platform_Version',setting)
        desired_caps['deviceName'] =self.config('device_Name',setting)
        desired_caps['app'] =PATH('../resource/' + self.config('app_Path',setting))
        desired_caps['appPackage'] = self.config('app_Package',setting)
        desired_caps['appActivity'] = self.config('app_Activity',setting)
        command_executor='http://127.0.0.1:4723/wd/hub'

        browser_profile = None
        proxy = None
        keep_alive = False

        super(Android, self).__init__(command_executor, desired_caps, browser_profile, proxy, keep_alive)

    def config(self,option,path):

        config = configparser.ConfigParser()
        config.read(PATH("../manifest/"+path+".ini"))
        b=config.get('setting',option)
        return b


    def find_id(self, id_):
        """Finds an element by id.
        """
        return self.find_element(by=By.ID, value=id_)

    def find_name(self, name):
        """
        Finds an element by name.
        """
        return self.find_element(by=By.NAME, value=name)

    def find_tag_name(self, name):
        """
        Finds an element by tag name.
        """
        return self.find_element(by=By.TAG_NAME, value=name)


    def screenShot(self,name):
        #截图并保存在screenshot目录下

        now =time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))
        #获取当前时间并格式化
        image=PATH("../screenshot/AndroidSDK/"+self.setting+"/"+now+"_"+name+".jpg")
        self.save_screenshot(image)
        print(image)


    def wait_find_element(self, how, what):
        '''
        等待动态控件的id 出现
        '''
        time_out = 100
        while time_out > 0:
            try:
                self.find_element(by=how, value=what)
                isExist = True
            except NoSuchElementException:
                isExist = False

            if isExist:
                return self.find_element(by=how, value=what)
            time_out -= 1
            time.sleep(0.5)
        else:
            raise (NameError, 'find_element timeout')

    def element_is_present(self, how, what):
        #判断某个元素是否存在
        try:
            self.find_element(by=how, value=what)
            return True
        except NoSuchElementException:
            return False

    def alert_is_present(self):
   #判断弹出框是否出现
        try:
            self.switch_to_alert()
            return True
        except NoAlertPresentException:
            return False

    def WaitId(self,T,id):
        #等待某个元素出现
        WebDriverWait(self, T).until(lambda x: x.find_element_by_id(id))

    def NotWaitId(self,T,id):
        #等待某个元素消失
        WebDriverWait(self, T).until_not(lambda x: x.find_element_by_id(id))



    def switch_to_activity(self,activity):
        '''
        切换到activity界面
        '''
        time.sleep(2)
        if not activity in self.current_activity:
            time.sleep(1)
            self.keyevent(4)
            #手机返回键
            time.sleep(2)
            try:
                self.alert_is_present()
                self.switch_to_alert()
                if self.element_is_present('name','确认'):
                    self.find_element_by_name('确认').click()
                if self.element_is_present('name','确定'):
                    self.find_element_by_name('确定').click()
                else:
                    self.element_is_present('name','返回游戏')
                    self.find_element_by_name('返回游戏').click()

            except:
                pass

            if not activity in self.current_activity:
                self.switch_to_activity(activity)

    def selectSQL(self,sql,data):
        '''
        mysql数据查询，查询多条数据
        '''
        db_array = self.config('database',self.setting)
        dbs = db_array.split(',')
        dbm = pymysql.connect(host=dbs[0],user=dbs[1],passwd=dbs[2],db=data,port=int(dbs[3]),charset=dbs[4])
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


    def login(self):
        try:
            self.switch_to_alert()
            self.find_element_by_id('singlegame_btncancel').click()
        except:
            pass

        self.find_element_by_id('button_login').click()
        if self.current_activity=='.activity.PPSUserActivity':
            print('登录成功')
        else:
            self.screenShot('error')

        self.WaitId(30,'ppsgame_current_account')
        self.NotWaitId(30,'game_auto_login_relativelayout')
        time.sleep(5)
        try:
            self.switch_to_alert()
            self.find_element_by_id('btn_dialog_close').click()
            time.sleep(1)
        except:
            pass
        #若显示公告、代金券弹出框，则关闭
        #print(self.current_activity)

    def slidebar(self):
        y1=self.config('Y1',self.setting)
        y2=self.config('Y2',self.setting)
        a=False
        for x in range(10,20):
            for y in range(y1,y2):
            #点击侧边栏图标显示个人中心弹出框
            #循环点击坐标区域（x,y），当user icon的id存在时表示已显示弹出框，则跳出整个循环
                self.execute_script("mobile: tap", {"touchCount":"1", "x":x, "y":y})

                if self.element_is_present('id','pps_fragment_bady'):
                    a=True
                    print('点击侧边栏图标，弹出个人中心框')
                    break
                else:
                    y+=1
            if a==True:
                break
            else:
                x+=1


    def contrast_elem(self,show,sql):
        #比较SDK中显示的数据与数据库中查询出的数据信息是否一致
        isExist = True
        for orderID in show:
            if orderID not in sql:
                isExist = False
                break

        for orderID in sql:
            if orderID not in show:
                isExist = False
                break
        if isExist and len(show)==len(sql):
            return True


    def swipe_load_item(self,page_size,id):
        '''
        列表滑动，装载每一页的（订单号或虚拟卡、礼包号）
        '''
        datas = ()
        list=[]

        while page_size>0:

            sub_tup = ()
            ids=self.find_elements_by_id(id)
            for i in range(0,len(ids)):

                try:
                    sub_txt = ids[i].text
                    sub_tup += (sub_txt,)
                    #将每一页的元素信息sub_txt装入元组中
                except NoSuchElementException:
                    pass

            if len(sub_tup) > 0 and sub_tup not in datas:
                #当下一页的元素信息与上一页的完全一致时，说明已滑动到最后一页，则退出滑动循环
                datas += (sub_tup,)
                #print(datas)
                #定位元素的原位置
                origin_el =ids[-1]
                #定位元素要移动到的目标位置
                destination_el =ids[0]
                #执行元素的移动操作
                self.drag_and_drop(origin_el,destination_el)
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
