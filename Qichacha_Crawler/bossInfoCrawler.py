# -*- coding: UTF-8 -*-
import sys

import requests

from requests import Request, Session
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    searchKey = 'name=%E9%A9%AC%E5%8C%96%E8%85%BE&companyname=深圳市腾讯计算机系统有限公司'
    CUSTOM_HEADER = {
        'accept':'text/html, */*; q=0.01',
        'authority': 'www.qichacha.com',
        'method': 'GET',
        'scheme': 'https',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,la;q=0.2',
        'referer':'https://www.qichacha.com/people?' + searchKey,
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'x-requested-with':'XMLHttpRequest',
    }
    jsonBaseUrl = 'https://www.qichacha.com/people_getChartData?'
    s = Session()
    req = Request('GET',  jsonBaseUrl + searchKey, headers=CUSTOM_HEADER)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    print resp.status_code
    print resp.encoding

    jsonKeys = ['Status', 'SXCount', 'EcoKind', 'ZXCount', 'Name', 'Area', 'RegCap', 'FundedRatio', 'RegNo', 'KeyNo', 'Industry']
    jsonData = resp.json()
    for dataUnit in jsonData:
        for key in jsonKeys:
            if key in dataUnit:
                if key == 'Industry':
                    print '- Industry -'
                    print dataUnit[key]['Industry'], dataUnit[key]['IndustryCode']
                    print dataUnit[key]['SubIndustry'], dataUnit[key]['SubIndustryCode']
                elif key == 'Area':
                    print 'Area', dataUnit[key]['Province'], dataUnit[key]['City'], dataUnit[key]['County']
                else:
                    print key, dataUnit[key]
        print '-----------------------'

    print '#####################ß'
    searchKey = 'name=马化腾&companyname=深圳市腾讯计算机系统有限公司'
    htmlBaseUrl = 'https://www.qichacha.com/people_companyColleagues?'
    s = Session()
    req = Request('GET',  htmlBaseUrl + searchKey, headers=CUSTOM_HEADER)
    prepped = s.prepare_request(req)
    resp = s.send(prepped)
    print resp.status_code
    print resp.encoding
    #print resp.content
    htmlDoc = BeautifulSoup(resp.content,'html.parser')
    colleagueList = htmlDoc.findAll('section', {'class': 'panel panel-default'})
    for colleague in colleagueList:
        name = colleague.find('a').text
        personLink = colleague.find('a')['href']
        position = colleague.find('small').text
        print name, position, personLink
