# -*- coding: UTF-8 -*-
import sys
import time
import random

import requests
import pymysql.cursors
from requests import Request, Session

reload(sys)
sys.setdefaultencoding('utf-8')

from mydao import MyDAO

class AllOwnedComapanies(MyDAO):
    def getKeyWords(self):
        data = self.db_retrieve('SELECT bossName, companyName FROM BossInfo WHERE bossNameId IS NULL')
        result = [(item['bossName'], item['companyName']) for item in data]
        return result

    def insertDate(self, item, id_num):
        sql = 'INSERT INTO EnterpriseInfo.BossInfo ({}) VALUES ({})'.format(
            ", ".join(item.keys()), ", ".join(item.values())
        )
        if ~self.db_insert_sql(sql):
            sql = 'UPDATE BossInfo SET bossNameId = {} WHERE bossName = {} AND companyName = {}'.format(
                str(id_num), item['bossName'], item['companyName']
            )
            self.db_update(sql)

    def paser(self, json_data, p_name, c_name, id_num):
        if json_data:
            for data_unit in json_data:
                json_keys = ['Status', 'SXCount', 'EcoKind', 'ZXCount', 'Name', 'Area', 'RegCap', 'FundedRatio', 'RegNo', 'KeyNo', 'Industry']
                for key in json_keys:
                    if key in data_unit:
                        if key == 'Industry':
                            print '- Industry -'
                            print data_unit[key]['Industry'], data_unit[key]['IndustryCode']
                            print data_unit[key]['SubIndustry'], data_unit[key]['SubIndustryCode']
                        elif key == 'Area':
                            print 'Area', data_unit[key]['Province'], data_unit[key]['City'], data_unit[key]['County']
                        else:
                            print key, data_unit[key]

                data_item = {
                    'bossName': '"' + p_name + '"',
                    'bossNameId': str(id_num),
                    'companyName': '"' + data_unit['Name'] + '"',
                    'companyId': '"' + data_unit['KeyNo'] + '"'
                }
                self.insertDate(data_item, id_num)
        else:
                data_item = {
                    'bossName': '"' + p_name + '"',
                    'bossNameId': str(id_num),
                    'companyName': '"' + c_name + '"'
                }
                self.insertDate(data_item, id_num)
        print '-----------------------'

if __name__ == '__main__':
    DB_OBJ = AllOwnedComapanies()
    DB_OBJ.db_connect('127.0.0.1', 'root', '2016leichen', 'EnterpriseInfo', charset = 'utf8mb4')

    timer_counter = 0
    while True:
        boss_company_list = DB_OBJ.getKeyWords()
        print 'Retrieve Unchecked Boss and Company List'
        timer = 0

        for person_name, company_name in boss_company_list:
            search_key = 'name=' + person_name + '&companyname=' + company_name
            CUSTOM_HEADER = {
                'accept':'text/html, */*; q=0.01',
                'authority': 'www.qichacha.com',
                'method': 'GET',
                'scheme': 'https',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,la;q=0.2',
                'referer':'https://www.qichacha.com/people?' + search_key,
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'x-requested-with':'XMLHttpRequest',
                'connection': 'keep-alive',
            }

            jsonBaseUrl = 'https://www.qichacha.com/people_getChartData?'
            s = Session()
            req = Request('GET',  jsonBaseUrl + search_key, headers=CUSTOM_HEADER)
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            print resp.status_code

            if resp.status_code == 200:
                try:
                    person_id_upper_bond = DB_OBJ.db_retrieve('SELECT max(bossNameId) FROM BossInfo WHERE bossName = "' + person_name + '"')
                    new_id = 1
                    try:
                        new_id = int(person_id_upper_bond[0]) + 1
                    except:
                        pass
                    print 'Current Name Appears', new_id, 'Times'
                    sqls = DB_OBJ.paser(resp.json(), person_name, company_name, new_id)
                except:
                    time.sleep(random.uniform(1, 2))
            else:
                pass
            
            sleeping_time = random.uniform(20, 40)
            timer += sleeping_time
            time.sleep(sleeping_time)
            if timer > 7200 + random.uniform(60, 180):
                DB_OBJ.db_reconnect_after(sleeping_time = random.uniform(3600, 7200))
                timer = 1
        
        if timer == 0:
            timer_counter += 1
            if timer_counter > 20:
                print 'Finish with All Bosses and Companies'
                break


