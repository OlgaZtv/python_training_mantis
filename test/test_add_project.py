# -*- coding: utf-8 -*-
from model.project import Project


def test_add_project(app):
    app.session.login("administrator", "root")
    app.project.create(Project(name="Test"))
    app.session.logout()
