__author__ = 'zhangchun'

#coding=utf-8
import unittest
#把testcase 目录添加到path 下，这里用的相对路径
import sys
import time
from framework import HTMLTestRunner
import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

list_case=sys.path.append("/testcase/AutoTest_SDK/")

def creatsuitel():
    testunit=unittest.TestSuite()
    #discover 方法定义
    discover=unittest.defaultTestLoader.discover(list_case,pattern ='test_*.py',top_level_dir=None)
    #discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for runner_case in test_suite:
            testunit.addTests(runner_case)
            print(runner_case)
    return testunit

if __name__ == "__main__":
    alltestnames = creatsuitel()

    #now = time.strftime('%Y-%m-%M-%H_%M_%S',time.localtime(time.time()))
    now =time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
    name = PATH('../../report/report'+now+'.html')
    fp =open(name,'wb')
    runner =HTMLTestRunner.HTMLTestRunner(
    stream=fp,
    title=u'测试报告',
    description=u'用例执行情况：')
    #执行测试用例
    runner.run(alltestnames)
    fp.close()
