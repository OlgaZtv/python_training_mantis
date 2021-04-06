# main fixture class (init driver/helpers)
from selenium import webdriver

from fixture.project import ProjectHelper
from fixture.session import SessionHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper

class Application:
    # init driver
    def __init__(self, browser, config):
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
        self.james = JamesHelper(self)
        self.singup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.config = config
        self.base_url = config["web"]["baseUrl"]

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
