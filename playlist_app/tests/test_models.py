from django.test import TestCase
from playlist_app.models import *

class ModelTestCase(TestCase):
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

        # Setting Playlist
        self.playlist = Playlist.objects.create(
            title='Test Playlist',
            user=self.user,
        )
        self.playlist.artists.set(self.artists)
        self.playlist.genres.set(self.genres)

    
    def test_playlist_model(self):
        self.assertEqual(self.playlist.title, 'Test Playlist')
        self.assertEqual(self.playlist.artists.all()[0], self.artists[0])
        self.assertEqual(self.playlist.genres.all()[0], self.genres[0])
        self.assertTrue(self.playlist.user, self.user)
        self.assertEqual(self.playlist.get_absolute_url(), '/playlist/1')
        

    def test_user_model(self):
        self.assertEqual(self.user.username, 'Test_User')
        self.assertEqual(self.user.get_username(), 'Test_User')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.get_short_name(), 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.get_full_name(), 'John Doe')

        self.assertEqual(self.user.email, 'test@uccs.edu')
        self.assertEqual(self.user.password, '12345')
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_authenticated)