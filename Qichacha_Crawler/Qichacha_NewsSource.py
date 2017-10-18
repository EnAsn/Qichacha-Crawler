# -*- coding: UTF-8 -*-

import time
import random
import math
import csv
import lxml.html

from SeleniumModel import automation
from selenium.webdriver.common.action_chains import ActionChains

class QichachaNewsSource(automation):
    def loginChecker(self):
        pass
    
    def getMovingTrail(self, distance):
        '''
            Simulate Human Drag and Drop Operations Trail
        '''
        moving_steps = []
        remaining_distance = distance
        step_length = [1.0/3, 1.0/4, 1.0/5, 2.0/5, 1.0/6,2.0/7, 3.0/8, 2.0/9]
        current_step = math.ceil(distance * random.choice(step_length))
        while remaining_distance - current_step >= 0:
            moving_times = random.randint(12, 23) / 100.0
            moving_steps.append((current_step, moving_times))
            remaining_distance -= current_step
            current_step = math.ceil(distance * random.choice(step_length))
        return moving_steps

    def normalLogin(self):
        #Select the login function on page
        login_btn = self.driver.find_element_by_css_selector('a.V3_index_loginbt:nth-child(3)')
        login_btn.click()
        time.sleep(3)

        #Select normal login
        while True:
            try:
                self.driver.save_screenshot('try_to_login.jpeg')
                normal_login_btn = self.driver.find_element_by_xpath('//*[@id="normalLogin"]')
                normal_login_btn.click()
                break
            except:
                time.sleep(1)
                continue

        #Input username and password
        usr_bar = self.driver.find_element_by_xpath('//*[@id="user_login_normal"]/div[1]/input')
        pwd_bar = self.driver.find_element_by_xpath('//*[@id="user_login_normal"]/div[2]/input')
        usr_bar.send_keys('18420153144')
        pwd_bar.send_keys('testing123')

        #Drag and Drop function
        btn_2_drag = self.driver.find_element_by_css_selector('#nc_2_n1z')
        ActionChains(self.driver).click_and_hold(on_element = btn_2_drag).perform()
        time.sleep(0.3)

        horizen_moving_trail = self.getMovingTrail(500)
        pic_num = 0
        for x_moving_distance, moving_time in horizen_moving_trail:
            pic_num += 1
            self.driver.save_screenshot('drag_bar_' + str(pic_num) + '.jpeg')
            ActionChains(self.driver).move_to_element_with_offset(to_element = btn_2_drag, xoffset=x_moving_distance, yoffset=0.0).perform()
            time.sleep(moving_time)
        time.sleep(3)
        self.driver.save_screenshot('login_page_snapshot.jpeg')
        
        #clickCaptcha_text

        ActionChains(self.driver).release(on_element = btn_2_drag).perform

        time.sleep(20)
        #Click to login
        send_login_request_btn = self.driver.find_element_by_xpath('//*[@id="user_login_normal"]/div[5]/button')
        send_login_request_btn.click()
        time.sleep(3)
    
    def getSourceList(self):
        source_list = []
        with open('urls.txt', 'r') as source_file:
            source_list = [x.split()[0] for x in source_file.readlines()]
            source_file.close()
        
        print 'Source List Loaded!'
        return source_list

    def getSearchList(self, file_list):
        search_list = []
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
                        search_list.append(company_info[-1])
                    else:
                        continue
                fin.close()
        print len(search_list), ' to be Searched!'
        return search_list

    def choseInfoCategory(self):
        category_select_btn = self.driver.find_element_by_css_selector('li.text-lg:nth-child(7) > a:nth-child(1)')
        if category_select_btn:
            category_select_btn.click()
            time.sleep(3)
            return True
        else:
            print 'Element Not Found, Error with click'
            self.driver.refresh()
            return False

    def collectNewsPublisher(self, news_source_list, output_file):
        while ~self.choseInfoCategory():
            time.sleep(random.uniform(3, 5))

        #Whether We Come to the Last Page = If NEXT Button is no longer availble
        while True:
            print 'Start Collecting Data'
            self.driver.save_screenshot('error.jpeg')

            a_items = None
            a_items = self.driver.find_elements_by_xpath('//*[@id="newslist"]/ul/a')
            
            if a_items != None:
                dom_content = lxml.html.fromstring(str(self.driver.page_source))
                a_tag_list = dom_content.xpath('//*[@id="newslist"]/ul/a')
                print 'No. of News', len(a_tag_list)

                #Scroll One Element Size Down, Simulating Human Behavior
                scroll_height = 300
                for a_tag in a_tag_list:
                    source_url = a_tag.get('href')
                    source_name = a_tag.xpath('./span[2]/small/text()')[1].strip()
                    print source_name, source_url
                    if source_name not in news_source_list:
                        news_source_list.append(source_name)
                        output_file.write(source_name + ' ' + news_source_list + '\n')
                    #Scroll the page
                    scroll_height += random.uniform(120, 130)
                    self.driver.execute_script("window.scrollTo(0, " + str(scroll_height) + ");")
                    time.sleep(random.uniform(1, 2))
                
                print 'Finish with Current Page'

                page_btns = self.driver.find_elements_by_xpath('//*[@id="newslist"]/nav/ul/li')
                print 'No. of Page Button', len(page_btns)
                #print str(page_btns)
                if page_btns:
                    next_page_btn = page_btns[-2].find_elements_by_tag_name('a')[0]
                    #print str(next_page_btn)
                    if next_page_btn.text == '>':
                        page_btns = self.driver.find_elements_by_xpath('//*[@id="newslist"]/nav/ul/li')[-2].find_elements_by_tag_name('a')[0]
                        next_page_btn.click()
                        print 'Click and Go to Next Page'
                        time.sleep(random.uniform(40, 60))
                    else:
                        break
                else:
                    break
            else:
                self.driver.execute_script("window.history.go(-1)")
                time.sleep(random.uniform(20, 30))

if __name__ == '__main__':
    BROWSER_DIRVER = QichachaNewsSource()
    BROWSER_DIRVER.start()

    HOME_URL = 'https://www.qichacha.com/'
    BROWSER_DIRVER.getWebpage(HOME_URL)
    #Read cookies and Login
    BROWSER_DIRVER.cookieLogin('cookies.pkl')
    source_list = BROWSER_DIRVER.getSourceList()
    SEARCH_LIST = BROWSER_DIRVER.getSearchList(['new_500.csv','old500_makeup.csv','company_url_error.txt'])

    for company_url in SEARCH_LIST:
        fout = open('urls.txt', 'a+')
        try:
            BROWSER_DIRVER.getWebpage(company_url)
            print 'Open Company Page'
            BROWSER_DIRVER.collectNewsPublisher(source_list, output_file = fout)
        except:
            print 'Error with Current Url!'
            print company_url
            with open('company_url_error.txt', 'a+') as error_file:
                error_file.write(company_url + '\n')
                error_file.close()
        finally:
            print 'Finish with', company_url
            fout.close()
    print 'Total Collected Sources', len(source_list)
    BROWSER_DIRVER.close()
