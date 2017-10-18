# -*- coding: UTF-8 -*-
import time

import pymysql.cursors

class MyDAO():
    def __init__(self):
        self.db = None
        self.cursor = None
        self.host = None
        self.usr = None
        self.pwd = None
        self.dbname = None
        self.charset = None

    def db_auto_connect(self):
        connection_timer = 0
        while True:
            connection_timer += 1
            try:
                self.db = pymysql.connect(host = self.host,
                                user = self.usr,
                                password = self.pwd,
                                db = self.dbname,
                                charset = self.charset,
                                cursorclass = pymysql.cursors.DictCursor)
                self.cursor = self.db.cursor()
                return True
            except:
                print 'Cannot Connect to MySQLdb'
                if connection_timer > 30:
                    return False
                time.sleep(30)

    def db_connect(self, host, usr, pwd, dbname, charset = 'utf8mb4'):
        connection_timer = 0
        while True:
            connection_timer += 1

            try:
                self.db = pymysql.connect(host=host,
                                user=usr,
                                password=pwd,
                                db=dbname,
                                charset=charset,
                                cursorclass=pymysql.cursors.DictCursor)
                self.cursor = self.db.cursor()
                self.host = host
                self.usr = usr
                self.pwd = pwd
                self.dbname = dbname
                self.charset = charset
                return True
            except:
                print 'Cannot Connect to MySQLdb'
                if connection_timer > 30:
                    return False
                time.sleep(30)

    def db_close(self):
        try:
            self.db.close()
        except:
            print 'DAO not found'

    def db_reconnect_after(self, sleeping_time = 1):
        self.db_close()
        time.sleep(sleeping_time)
        self.db_auto_connect()

    def db_retrieve(self, sql):
        if self.cursor:
            try:
                print sql
                results = []
                counter = 0
                retrieve_flag = False
                while ~retrieve_flag:
                    self.cursor.execute(sql)
                    results = self.cursor.fetchall()
                    if results:
                        break
                    else:
                        print 'No Result Retrieved! Waiting for Data...'
                        counter += 1
                        if counter >= 20:
                            break
                        else:
                            time.sleep(30)
                return results         
            except pymysql.err.IntegrityError as e:
                print e[0] + '\n' + e[1]
                print 'Error with sql: ' + sql
                self.db.rollback()
                return None
        else:
            print 'DAO not available'
            return None

    def db_insert_sql(self, sql):
        insert_flag = False
        if self.cursor:
            try:
                print sql
                self.cursor.execute(sql)
                self.db.commit()
                insert_flag = True
            except pymysql.err.IntegrityError as e:
                if not e[0] == 1062:
                    print e[0] + '\n' + e[1]
                    print sql
                    self.db.rollback()
                else:
                    print e[1]
                    self.db.rollback()
        else:
            print 'DAO not available'
        return insert_flag

    def db_insert_sqls(self, sqls):
        insert_flag = False
        if self.cursor:
            for sql in sqls:
                try:
                    print sql
                    self.cursor.execute(sql)
                    self.db.commit()
                    insert_flag = True
                except pymysql.err.IntegrityError as e:
                    if not e[0] == 1062:
                        print e[0] + '\n' + e[1]
                        print sql
                        self.db.rollback()
                    else:
                        print e[1]
                        self.db.rollback()
        else:
            print 'DAO not available'
        return insert_flag

    def db_update(self, sql):
        if self.cursor:
            try:
                print sql
                self.cursor.execute(sql)
                self.db.commit()
            except:
                print 'UPDATE FAILURE!'
                self.db.rollback()