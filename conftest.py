import pytest
import json
import os.path
import ftputil
from fixture.application import Application


fixture = None
target = None

# будет определять какой блок данных мы берем из target.json (web/db)
def load_config(file):
    global target
    # check if data from target.json not loaded - load it
    if target is None:
        # find path to file and join with filename (from option "target")
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        # open file only while load, then autoClose
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))["web"]

@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=config["web"]['baseUrl'])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config["ftp"]["host"],config["ftp"]["username"],config["ftp"]["password"])
    def fin():
        restore_server_configuration(config["ftp"]["host"],config["ftp"]["username"],config["ftp"]["password"])
    request.addfinalizer(fin)

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture

# run configuration - additional arguments
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

# # HOOK(check https://docs.pytest.org/en/stable/parametrize.html): Implement your own parametrization scheme or
# # implement some dynamism for determining the parameters or scope of a fixture. We implement inserting of testdata to
# # test (e.g. test_add_group) - removing annotation pytest and change input parameter to 'data_groups' in test
# def pytest_generate_tests(metafunc):
#     for fixture in metafunc.fixturenames:
#         if fixture.startswith("data_"):
#             testdata = load_from_module(fixture[5:])
#             # what we put: from - fixture, what - testdata, presented in string - ids
#             metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
#         elif fixture.startswith("json_"):
#             testdata = load_from_json(fixture[5:])
#             metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
#
#
# def load_from_module(module):
#     return importlib.import_module("data.%s" % module).testdata
#
#
# def load_from_json(file):
#     # open file
#     # os.path.dirname - project dir
#     # os.path.abspath(__file__) - path to file
#     # "data/%s.json" % file - join path to json file
#     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
#         # read file and decode to python object (testdata)
#         return jsonpickle.decode(f.read())
