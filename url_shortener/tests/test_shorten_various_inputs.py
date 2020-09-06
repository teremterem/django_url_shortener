from django.test import TestCase, Client

from ..models import ShortenedUrl


class TestShortenVariousInputs(TestCase):
    """
    Feature: shorten_url view accepts various long url formats and processes them correctly
    """

    def setUp(self):
        """
        Initialize http client
        """
        self.client = Client()

    def test_shorten_url_with_https(self):
        """
        Scenario: User submits long url with hTTps:// protocol specified
            Given http client is initialized
              And no other long urls have been shortened yet

             When User submits long url with hTTps:// protocol specified (in mixed case)

             Then only one record exists in shortenedurl DB table
              And long url is stored as is with no modification other than leading/training whitespaces stripped
              And the service redirects from short url to the long url that is stored
        """
        self.client.post('/shorten-url/', {
            'long_url': '   hTTps://hello.world.com/how_are_you_doing/you_world+%20      ',
        })

        rows = ShortenedUrl.objects.all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].long_url, 'hTTps://hello.world.com/how_are_you_doing/you_world+%20')

        # TODO
