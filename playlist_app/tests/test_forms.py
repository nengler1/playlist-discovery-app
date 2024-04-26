from django.test import TestCase, LiveServerTestCase
from playlist_app.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By

from django.forms import ModelForm
from playlist_app.forms import *

class FormTestCase(TestCase):
    def setUp(self):
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

    def test_register(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element(
            By.XPATH,
            "//div[@class='navbar-nav']/a[@href='/accounts/register/?next=/']"
        ).click()

        self.browser.find_element(By.ID, "id_username").send_keys("Test_User1")
        self.browser.find_element(By.ID, "id_email").send_keys("test1@uccs.edu")
        self.browser.find_element(By.ID, "id_password1").send_keys("cs3300_app!")
        self.browser.find_element(By.ID, "id_password2").send_keys("cs3300_app!")
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()

        self.browser.find_element(
            By.XPATH,
            "//div[@class='navbar-nav']/a[@href='/accounts/login/?next=/']"
        ).click()

        self.browser.find_element(By.ID, "id_username").send_keys("Test_User1")
        self.browser.find_element(By.ID, "id_password").send_keys("cs3300_app!")
        self.browser.find_element(By.XPATH, "//input[@type='submit']").click()

        self.browser.quit()