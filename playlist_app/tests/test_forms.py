from django.test import TestCase, LiveServerTestCase, TransactionTestCase
from playlist_app.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time

from django.forms import ModelForm
from playlist_app.forms import *

class FormTestCase(TestCase):
    def setUp(self):
        # Setting Artists and Genres
        artist_list = ['Artist1']
        self.artists = Artist.objects.bulk_create([Artist(name=n) for n in artist_list])

        genre_list = ['Genre1']
        self.genres = Genre.objects.bulk_create([Genre(name=n) for n in genre_list])

        # Setting User
        self.user = User.objects.create(
            username='Test_User',
            first_name='John',
            last_name='Doe',
            email='test@uccs.edu',
            password='12345',
            is_staff=False,
        )

        #print('\nTESTING:', [str(self.artists[0].pk)],'\n')

    class PlaylistForm(ModelForm):
        class Meta:
            model = Playlist
            fields = fields = ('title', 'artists', 'genres', 'cover', 'user',)
    
    def test_valid_form(self):
        data = {
            'title': 'Form Test Playlist',
            'artists': [str(self.artists[0].pk)],
            'genres': [str(self.genres[0].pk)],
            'cover': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            'user': self.user,
        }
        form = PlaylistForm(data=data)
        self.assertTrue(form.is_valid())

class SeleniumFormTest(LiveServerTestCase):
    # set up selenium browser
    def setUp(self):
        self.browser = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install())
        )

        self.user = User.objects.create(
            username='Test_User',
            first_name='John',
            last_name='Doe',
            email='test@uccs.edu',
            password='12345',
            is_staff=False,
        )

    def test01_register(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element(
            By.XPATH,
            "//div[@class='navbar-nav']/a[@href='/accounts/register/?next=/']"
        ).click()

        self.browser.find_element(By.ID, "id_username").send_keys("Test_User1")
        self.browser.find_element(By.ID, "id_email").send_keys("test1@uccs.edu")
        self.browser.find_element(By.ID, "id_password1").send_keys("cs3300_app!")
        self.browser.find_element(By.ID, "id_password2").send_keys("cs3300_app!")
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()

        self.browser.find_element(By.ID, "id_username").send_keys("Test_User1")
        self.browser.find_element(By.ID, "id_password").send_keys("cs3300_app!")
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()

        self.browser.quit()
    
    def test02_create_playlist(self):
        self.browser.get(self.live_server_url + "/accounts/login")
        
        # Logging in
        self.browser.find_element(By.ID, "id_username").send_keys("Test_User")
        self.browser.find_element(By.ID, "id_password").send_keys("12345")
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()

        self.browser.find_element(By.LINK_TEXT, "Create Playlist").click()
        self.browser.find_element(By.NAME, "title").send_keys("Selenium Title Test")

        # Clicking Artists and Genres
        self.browser.find_element(By.XPATH, "//select[@id='id_artists']/option[2]").click()
        self.browser.find_element(By.XPATH, "//select[@id='id_artists']/option[3]").click()
        self.browser.find_element(By.XPATH, "//select[@id='id_genres']/option[6]").click()
        self.browser.find_element(By.XPATH, "//select[@id='id_genres']/option[2]").click()

        # Browsing image file
        self.browser.find_element(By.ID, "id_cover").send_keys("C:\\Users\\natha\\Downloads\\selenium_test.jpg")

        #submitting
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()

        