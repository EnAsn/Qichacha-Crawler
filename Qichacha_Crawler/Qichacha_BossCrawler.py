# -*- coding: UTF-8 -*-
import sys
import csv
import time
import random

import requests
from requests import Request, Session
import json
from bs4 import BeautifulSoup
from mydao import MyDAO

reload(sys)
sys.setdefaultencoding('utf-8')

class BossDAO(MyDAO):
    def insertSequence(self, sqls):
        self.db_connect('127.0.0.1', 'root', '', 'EnterpriseInfo', charset = 'utf8mb4')
        self.db_insert_sqls(sqls)
        self.db_close()
    
    def getSearchedList(self):
        self.db_connect('127.0.0.1', 'root', '', 'EnterpriseInfo', charset = 'utf8mb4')
        result = self.db_retrieve('SELECT DISTINCT companyId FROM BossInfo')
        output = [item['companyId'] for item in result]
        self.db_close()
        print len(output), 'Companies to be Searched'
        return output
    
def parser(content, url):
    data = {}
    company_id = url.split('firm_')[1].split('.')[0]
    data['companyId'] = '"' + company_id + '"'
    html_doc = BeautifulSoup(content,'html.parser')
    company_name = html_doc.find('div', {'class': 'text-big font-bold company-top-name'}).text
    data['companyName'] = '"' + company_name + '"'
    main_member_section = html_doc.find('section', {'id': 'Mainmember', 'class':'panel b-a clear'})
    main_member_table = main_member_section.find('table')
    main_member_list = main_member_table.findAll('tr')[1:]
    result = []
    for member in main_member_list:
        boss_name = member.find('div').text
        data['bossName'] = '"' + boss_name + '"'
        print boss_name, company_name, company_id
        data.update((key, value) for key, value in data.iteritems())
        sql = 'INSERT INTO EnterpriseInfo.BossInfo ({}) VALUES ({})'.format(
            ", ".join(data.keys()), ", ".join(data.values())
        )
        print sql
        result.append(sql)
    return result

reload(sys)
sys.setdefaultencoding('utf-8')

def getSearchList(file_list):
    result = []
    for file_name in file_list:
        with open(file_name, 'rb') as fin:
            file_type = file_name.split('.')[1]
            if file_type == 'csv':
                reader = csv.reader(fin)
            else:
                reader = [x.split(',') for x in fin.readlines()]
                    
            for company_info in reader:
                #print str(company_info), len(company_info)
                if company_info[-1]:
                    result.append(company_info[-1])
                else:
                    continue
            fin.close()
    print len(result), 'to be Searched!'
    return result

def reformData(data_string):
    return '`' + data_string + '`'

if __name__ == '__main__':
    search_list = getSearchList(['new_500.csv','old500_makeup.csv','company_url_error.txt'])
    INITIAL_PAGE_HEADER = {
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'host': 'www.qichacha.com',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,la;q=0.2',
        'connection': 'keep-alive',
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'upgrade-insecure-requests': '1',
        'cache-control': 'max-age=0',
        'cookie': 'UM_distinctid=15e9d34341754b-0d3afdc86db793-143c6c55-13c680-15e9d343418b87; _uab_collina=150587606580112869908915; acw_tc=AQAAAF7Ntk0ZqgcANX6fr8O8XhS8EtqW; _umdata=C234BF9D3AFA6FE7C0B4A4D091E7E1ACFC4A05F69288643539ABC7570D62A68441784DCBC7F8536CCD43AD3E795C914C1736616EE442D54C90E8263C189B5745; PHPSESSID=i3bi4p6s2rj2og3krcok3iims3; zg_did=%7B%22did%22%3A%20%2215e9d251dbd22d-0b852fa96624fa-143c6c55-13c680-15e9d251dbf131%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201507604237915%2C%22updated%22%3A%201507605565585%2C%22info%22%3A%201507258440378%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%224ddd83b6a6b7752de9cd07d1f3c8c9a6%22%7D; CNZZDATA1254842228=262366834-1505449625-%7C1507602187',
    }

    DB_OBJ = BossDAO()
    searched_list = DB_OBJ.getSearchedList()
    total_sleeping_time = 0

    for company_url in search_list:
        print company_url
        try:
            candidate_id = company_url.split('firm_')[1].split('.')[0]
        except:
            print 'url Format Error!'
            continue
        if candidate_id in searched_list:
            continue

        while True:
            print 'Starting Crawling', company_url
            try:
                s = Session()
                req = Request('GET', company_url, headers=INITIAL_PAGE_HEADER)
            except:
                break
            prepped = s.prepare_request(req)
            resp = s.send(prepped)
            print resp.status_code
            if resp.status_code == 200:
                try:
                    queries = parser(resp.content, company_url)
                    print 'Queries Created'
                    DB_OBJ.insertSequence(queries)
                    break
                except:
                    with open('boss_error_html.txt', 'w+') as fout:
                        fout.write(resp.content)
                        fout.close()
                    time.sleep(random.uniform(3, 5))
                    print 'Missing Data'
                    break
            else:
                with open('boss_crawler_error_url.txt', 'a+') as fout:
                    fout.write(company_url + '\n')
                    fout.close()
                break

        sleeping_time = random.uniform(20, 40)
        time.sleep(sleeping_time)
        total_sleeping_time += sleeping_time
        if total_sleeping_time > 7200 + random.uniform(60, 180):
            time.sleep(random.uniform(3600, 7200))
            total_sleeping_time = 0
