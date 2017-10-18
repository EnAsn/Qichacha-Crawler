# -*- coding: UTF-8 -*-
import pickle
import time

from NECIPS_Crawlers.SeleniumModel import automation

if __name__ == '__main__':
    BROWSER_DIRVER = automation()
    BROWSER_DIRVER.start()

    HOME_URL = 'https://www.qichacha.com/'
    BROWSER_DIRVER.getWebpage(HOME_URL)
    time.sleep(100)

    pickle.dump(BROWSER_DIRVER.driver.get_cookies(), open("cookies.pkl","wb"))

    BROWSER_DIRVER.close()

    