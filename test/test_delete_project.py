from fixture.project import Project
import random


def test_delete_project(app, db):
    if len(db.get_projects_list()) == 0:
        app.project.add_project(Project(name="Project to delete"))
    old_projects = db.get_projects_list()
    project = random.choice(old_projects)
    app.project.delete_project(project)
    new_projects = app.soap.get_projects_list_for_user(app.config['webadmin']['user'], app.config['webadmin']['password'])
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)