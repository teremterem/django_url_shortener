from django.test import TestCase

from ..models import ShortenedUrl
from ..shortener import shortener_storage


class TestShortenVariousInputs(TestCase):
    """
    Feature: shortener_storage.py::shorten_url function accepts various long url formats and processes them correctly
    """

    def test_shorten_url_with_https(self):
        """
        Scenario: User submits long url with https:// protocol specified
            Given no other long urls have been shortened yet

             When User submits long url with https:// protocol specified

             Then only one record exists in shortenedurl DB table
              And long url is stored as is with no modification other than leading/training whitespaces stripped
        """
        shortener_storage.shorten_url('   https://hello.world.com/how_are_you_doing/you_world      ')

        rows = ShortenedUrl.objects.all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].long_url, 'https://hello.world.com/how_are_you_doing/you_world')
