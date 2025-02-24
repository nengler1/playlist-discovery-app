from django.test import TestCase, LiveServerTestCase, Client
from django.urls import reverse
from playlist_app.models import *

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class ViewsTestCase(TestCase):
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
    
    def test_index_view(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'playlist_app/index.html')

class SeleniumViewsTest(LiveServerTestCase):
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

    def test_playlist_detail(self):
        self.browser.get(self.live_server_url)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//div[@class='col-md-8']//a[@href='/playlist/1']").click()