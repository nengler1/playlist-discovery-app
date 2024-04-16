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

        artist_list = ['Artist1', 'Artist2', 'Artist3', 'Artist4', 'Artist5', 'Artist6']
        self.artists = Artist.objects.bulk_create([Artist(name=n) for n in artist_list])

        genre_list = ['Genre1', 'Genre2', 'Genre3', 'Genre4', 'Genre5', 'Genre6']
        self.genres = Genre.objects.bulk_create([Genre(name=n) for n in genre_list])

        self.playlist = Playlist.objects.create(
            title='Test Playlist',
        )
        self.playlist.artists.set(
            Artist.objects.all().filter(name__in=['Artist1', 'Artist2'])
        )
        self.playlist.genres.set(
            Genre.objects.all().filter(name__in=['Genre3', 'Genre4'])
        )

    # python manage.py test playlist_app.tests.tests.SeleniumTests.testHomePage
    def testHomePage(self):
        self.browser.get(self.live_server_url)
        assert 'Music Discovery App' in self.browser.title
        self.browser.quit()

    # python manage.py test playlist_app.tests.tests.SeleniumTests.testPlaylistDetail
    def testPlaylistDetail(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.XPATH, "//div[@class='col-md-8']//a[@href='/playlist/1']").click()
    
    # run specified test: 
    # python manage.py test playlist_app.tests.tests.SeleniumTests.testCreatePlaylist
    def testCreatePlaylist(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, "create_playlist_btn").click()
        time.sleep(1)
        self.browser.find_element(By.NAME, "title").send_keys("Selenium Title Test")

        # Clicking Artists and Genres
        self.browser.find_element(By.XPATH, "//select[@id='id_artists']/option[2]").click()
        self.browser.find_element(By.XPATH, "//select[@id='id_artists']/option[3]").click()
        self.browser.find_element(By.XPATH, "//select[@id='id_genres']/option[6]").click()
        self.browser.find_element(By.XPATH, "//select[@id='id_genres']/option[2]").click()

        # Browsing image file
        self.browser.find_element(By.XPATH, "//input[@id='id_cover']").send_keys("C:\\Users\\natha\\Downloads\\selenium_test.jpg")
        time.sleep(1)

        #submitting
        self.browser.find_element(By.XPATH, "//button[@type='submit']").submit()
        time.sleep(1)
        self.browser.quit()
