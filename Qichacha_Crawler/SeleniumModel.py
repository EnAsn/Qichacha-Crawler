# -*- coding: UTF-8 -*-
import pickle
import time

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException,\
    WebDriverException
from selenium.webdriver.common.by import By

class automation():
    def __init__(self):
        self.display = Display(visible=0, size=(1920, 1080))
        #self.DISPLAY.start()

        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("browser.cache.disk.enable", False)
        self.profile.set_preference("browser.cache.memory.enable", False)
        self.profile.set_preference("browser.cache.offline.enable", False)
        self.profile.set_preference("network.http.use-cache", False)

        self.driver = webdriver.Firefox(self.profile)
        # Resize the window to the screen width/height
        self.driver.maximize_window()

    def start(self):
        self.display.start()

    def getWebpage(self, url):
        self.driver.get(url)
        counter = 0
        try:
            web_element = None
            web_element = WebDriverWait(self.driver, 60, 10).until(EC.presence_of_all_elements_located)
            while web_element == None:
                '''
                    Retry Connection Strategy
                '''
                self.driver.refresh()
                web_element = WebDriverWait(self.driver, 60, 10).until(EC.presence_of_all_elements_located)
                counter += 1
                if counter > 5:
                    break
        finally:
            return web_element
    
    def locateElementByClass(self, class_name):
        WebDriverWait(self.driver, 60, 3).until(EC.presence_of_all_elements_located)
        try:
            web_element = None
            web_element = WebDriverWait(self.driver, 60, 3).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        except:
            return None
        return web_element
    
    def getElementByXpath(self, xpath):
        WebDriverWait(self.driver, 60, 3).until(EC.presence_of_all_elements_located)
        try:
            web_element = None
            web_element = self.driver.find_element_by_xpath(xpath)
        except:
            return None
        return web_element 

    def switch2NewWindow(self):
        print 'Switch to New Page'
        window_handles = self.driver.window_handles
        time.sleep(1)
        self.driver.switch_to_window(self.driver.window_handles[-1])
        time.sleep(3)

    def close(self):
        self.driver.quit()
        self.display.stop()

    def loginChecker(self):
        pass

    def cookieLogin(self, cookiesPath):
        cookies = pickle.load(open(cookiesPath, 'rb'))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()
        print 'Cookie Loaded!'

    def normalLogin(self):
        pass

if __name__ == '__main__':
    BROWSER_DIRVER = automation()
    BROWSER_DIRVER.start()
    print BROWSER_DIRVER.getWebpage('https://www.qichacha.com/')
    BROWSER_DIRVER.close()
