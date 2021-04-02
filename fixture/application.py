# main fixture class (init driver/helpers)
from selenium import webdriver

from fixture.project import ProjectHelper
from fixture.session import SessionHelper


class Application:
    # init driver
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
             raise ValueError("Unrecognized browser %s" % browser)
        # self.wd.implicitly_wait(20)
        # init our helpers
        #self.wd.implicitly_wait(10)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    # navigation method(s)
    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        # close driver
        self.wd.quit()
