from unittest.mock import patch

from django.test import TestCase, Client

from ..models import ShortenedUrl
from ..shortener import shortener_storage


class TestShortenVariousInputs(TestCase):
    """
    Feature: shorten_url view accepts various long url formats and processes them correctly
    """

    def setUp(self):
        """
        Initialize http client.
        """
        self.client = Client()

    def test_shorten_url_with_https(self):
        """
        Scenario: User submits a long url with hTTps:// protocol specified
            Given http client is initialized
              And no other long urls have been shortened yet

             When User submits a long url with hTTps:// protocol specified (in mixed case)

             Then only one record exists in shortenedurl DB table
              And the long url is stored as is with no modification other than leading/training whitespaces stripped
              And the service redirects from short url using 302 (temporary) redirect
              And the service redirects from short url to the long url that was stored
        """
        self._test_shorten_then_expand(
            long_url_input='   hTTps://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20      ',
            expected_redirect_url='hTTps://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20',
        )

    def test_shorten_url_without_protocol(self):
        """
        Scenario: User submits a long url without protocol specified
            Given http client is initialized
              And no other long urls have been shortened yet

             When User submits a long url without protocol specified

             Then only one record exists in shortenedurl DB table
              And leading/trailing whitespaces are stripped from the long url
              And the long url is prepended with http:// and only then stored
              And the service redirects from short url using 302 (temporary) redirect
              And the service redirects from short url to the long url that was stored
        """
        self._test_shorten_then_expand(
            long_url_input='  \n\thello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20 \t\n      ',
            expected_redirect_url='http://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20',
        )

    @patch.object(shortener_storage, 'generate_url_handle', return_value='abc')
    def _test_shorten_then_expand(self, mock_generate_url_handle, long_url_input, expected_redirect_url):
        self.client.post('/shorten-url/', {
            'long_url': long_url_input,
        })

        rows = ShortenedUrl.objects.all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].long_url, expected_redirect_url)

        response = self.client.get('/abc')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect_url)
