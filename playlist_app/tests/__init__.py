import unittest

def suite():   
    return unittest.TestLoader().discover("playlist_app.tests", pattern="*.py")