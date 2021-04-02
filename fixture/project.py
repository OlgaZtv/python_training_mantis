import time


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def create(self, name):
        wd = self.app.wd
        link: str = "http://localhost/mantisbt-1.2.20/manage_overview_page.php"
        wd.get(link)
        wd.find_element_by_link_text("Manage Projects").click()
        wd.find_element_by_css_selector("input.button-small").click()
        time.sleep(20)
        wd.find_element_by_name("name").clear()
        wd.find_element_by_name("name").send_keys(name)
        wd.find_element_by_name("name").click()
        wd.find_element_by_name("submit").click()
        self.project_cache = None

