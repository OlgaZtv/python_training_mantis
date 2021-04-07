import time
from fixture.navigation import NavigationHelper
from model.project import Project

class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def create(self, project):
        wd = self.app.wd
        NavigationHelper.open_manage_page(self)
        NavigationHelper.open_project_page(self)
        self.fill_project_form(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()

    def fill_project_form(self, project):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.change_fileld_value("name", project.name)
        self.change_fileld_value("description", project.description)

    def change_fileld_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def delete_project(self, project):
        wd = self.app.wd
        NavigationHelper.open_manage_page(self)
        NavigationHelper.open_project_page(self)
        wd.find_element_by_xpath("//a[contains(@href, 'manage_proj_edit_page.php?project_id=%s')]" % project.id).click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()






