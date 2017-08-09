__author__ = 'zhangchun'

# coding=utf-8

import pymysql

class DBManager():

    def __init__(self,url,usr,pwd,db_name,port):
        self.conn = pymysql.connect(url,usr,pwd,db_name,port,charset='utf8')

    def get_cursor(self):
        return self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def insert_values(self, sql, data):
        '''插入数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    cu.execute(sql, d)
                    self.conn.commit()
                cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    def fetchall(self, sql):
        '''查询所有数据'''
        if sql is not None and sql != '':
            cu = self.get_cursor()
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
                cu = self.get_cursor()
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

    def update(self, sql, data):
        '''更新数据'''
        if sql is not None and sql != '':
            if data is not None:
                cu = self.get_cursor()
                for d in data:
                    cu.execute(sql, d)
                    self.conn.commit()
                cu.close()
        else:
            print('the [{}] is empty or equal None!'.format(sql))
