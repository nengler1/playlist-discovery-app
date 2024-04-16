from django.test import TestCase, LiveServerTestCase
from playlist_app.models import *

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class SeleniumTests(LiveServerTestCase):
    # set up selenium browser
    def setUp(self):
        self.browser = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
        )

    def testHomePage(self):
        self.browser.get("http://127.0.0.1:8000")
        assert 'Music Discovery App' in self.browser.title
        self.browser.quit()
    
    # run specified test: 
    # python manage.py test playlist_app.tests.tests.SeleniumTests.testCreatePlaylist
    def testCreatePlaylist(self):
        self.browser.get("http://127.0.0.1:8000")
        self.browser.find_element(By.NAME, "create_playlist_btn").click()
        self.browser.find_element(By.NAME, "title").send_keys("Selenium Title Test")
        time.sleep(5)
        self.browser.quit()
