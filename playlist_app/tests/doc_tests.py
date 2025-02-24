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
        self.browser.get("https://www.google.com")
        assert 'Google' in self.browser.title
        self.browser.quit()
