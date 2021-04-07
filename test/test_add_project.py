# -*- coding: utf-8 -*-
from model.project import Project


def test_add_project(app, db, json_project):
    project = json_project
    app.navigation.open_home_page()
    old_projects = db.get_projects_list()
    app.project.create(project)
    new_project = db.get_projects_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_project, key=Project.id_or_max)