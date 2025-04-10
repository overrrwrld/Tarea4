import os
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from pytest_html import extras

@pytest.fixture(scope="class")
def driver(request):
    service = Service(executable_path="msedgedriver.exe")
    driver = webdriver.Edge(service=service)
    driver.maximize_window()
    driver.get("http://biblioteca.infy.uk/contact.php?i=1")
    request.cls.driver = driver
    request.cls.extra = []
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and hasattr(item.cls, "extra"):
        rep.extra = item.cls.extra
