# -*- coding: UTF-8 -*-
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException,\
    WebDriverException
import pickle

class automation():
    def __init__(self):
        self.DISPLAY = Display(visible=0, size=(1920, 1080))
        #self.DISPLAY.start()

        self.PROFILE = webdriver.FirefoxProfile()
        self.PROFILE.set_preference("browser.cache.disk.enable", False)
        self.PROFILE.set_preference("browser.cache.memory.enable", False)
        self.PROFILE.set_preference("browser.cache.offline.enable", False)
        self.PROFILE.set_preference("network.http.use-cache", False)

        self.driver = webdriver.Firefox(self.PROFILE)
        # Resize the window to the screen width/height
        self.driver.set_window_size(1920, 1080)

    def start(self):
        self.DISPLAY.start()

    def get(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()
        self.DISPLAY.stop()

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
