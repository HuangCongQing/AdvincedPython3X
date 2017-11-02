# -*- coding: utf-8 -*-
# @Author: hasee
# @Date:   2017-11-02 21:30:11
# @Last Modified by:   重庆
# @Last Modified time: 2017-11-02 21:30:43
#coding=utf-8
import pymysql 
import sys 
class TransferMoney: 
    def __init__(self,conn): 
        self.conn = conn 
    def check_acct_available(self, acctid): 
        try: 
            cursor = self.conn.cursor() 
            sql = "select * from account where acctid= %s " % acctid 
            cursor.execute(sql) 
            print ("check_acct_available:" + sql) 
            rs = cursor.fetchall() 
            if len(rs) != 1: 
                raise Exception("账号%s 不存在" % acctid) 
        finally:
            cursor.close() 
                
    def has_enough_money(self, acctid, money): 
        try: 
            cursor = self.conn.cursor() 
            sql = "select * from account where acctid=%s and money>=%s" % (acctid,money) 
            cursor.execute(sql) 
            print ("has_enough_money:" + sql) 
            rs = cursor.fetchall() 
            if len(rs) != 1: 
                raise Exception("账号%s余额不足 is not enough" % acctid) 
        finally: 
            cursor.close() 
    def reduce_money(self, acctid, money): 
        try: 
            cursor = self.conn.cursor() 
            sql = "update account set money= money-%s WHERE acctid=%s " % (money,acctid) 
            cursor.execute(sql) 
            print ("reduce_money:" + sql) 
            rs = cursor.rowcount 
            if rs != 1: 
                raise Exception("账号%s付款失败Eend is not enough" % acctid) 
        finally: 
            cursor.close() 
    def add_money(self, acctid, money): 
        try: 
            cursor = self.conn.cursor() 
            sql = "update account set money= money+%s WHERE acctid=%s " % (money,acctid) 
            cursor.execute(sql) 
            print("add_money:" + sql) 
            rs = cursor.rowcount 
            if rs != 1: 
                raise Exception("账号%s收款失败(Payment failure)get is not enough" % acctid) 
        finally: 
            cursor.close() 
    def transfer(self, source_acctid, target_acctid, money): 
        try: 
            self.check_acct_available(source_acctid) 
            self.check_acct_available(target_acctid) 
            self.has_enough_money(source_acctid,money) 
            self.reduce_money(source_acctid,money) 
            self.add_money(target_acctid,money) 
            self.conn.commit() 
        except Exception as e: 
            self.conn.rollback() 
            raise e 
if __name__=="__main__": 
    ## print("sys.argv[1:]:",sys.argv[1:])
    source_acctid = sys.argv[1] # 汇款发送账户
    target_acctid = sys.argv[2] # 收款账户
    money = sys.argv[3] 
    conn = pymysql.connect( 
        host = '127.0.0.1', 
        port = 3306, 
        user = 'root', 
        passwd = '123456', 
        db = 'imooc', 
        charset = 'utf8' ) 
    tr_money = TransferMoney(conn) 
    try: 
        tr_money.transfer(source_acctid,target_acctid,money) 
    except Exception as e: 
        print("出现问题(There is a problem)：" + str(e)) 
    finally: 
        conn.close()

