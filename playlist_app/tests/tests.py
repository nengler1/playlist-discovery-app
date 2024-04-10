from django.test import TestCase, LiveServerTestCase
from playlist_app.models import *

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class SeleniumTests(LiveServerTestCase):
    def testHomePage(self):
        browser = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
        )  

        browser.get("http://127.0.0.1:8000")
        assert 'Music Discovery App' in browser.title
        browser.quit()
    
    # run specified test: 
    # python manage.py test playlist_app.tests.tests.SeleniumTests.testCreatePlaylist
    def testCreatePlaylist(self):
        browser = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
        )

        browser.get("http://127.0.0.1:8000")
        browser.find_element(By.NAME, "create_playlist_btn").click()
