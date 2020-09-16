from unittest.mock import patch

from django.test import TestCase, Client

from ..models import ShortenedUrl
from ..shortener import shortener_storage


class TestShortenVariousInputs(TestCase):
    """
    Feature: shorten_url view accepts various long url formats and processes them correctly

    https://martinfowler.com/bliki/GivenWhenThen.html
    https://docs.djangoproject.com/en/3.1/intro/tutorial05/#test-a-view
    """

    def setUp(self):
        """
        Initialize http client.
        """
        self.client = Client()

    def test_shorten_url_with_https_protocol(self):
        """
        Scenario: User submits a long url with hTTps:// protocol specified
            Given http client is initialized
              And no other long urls have been shortened yet

             When User submits a long url with hTTps:// protocol specified (in mixed case)

             Then only one record exists in shortenedurl DB table
              And the long url is stored as is with no modification other than leading/training whitespaces stripped
                  (and empty query string and fragment removed and protocol lower-cased)
              And the service redirects from short url using 302 (temporary) redirect
              And the service redirects from short url to the long url that was stored
        """
        self._test_shorten_then_expand(
            long_url_input='   hTTps://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20      ',
            stored_long_url='https://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20',
            expected_redirect_url='https://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20',
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
            stored_long_url='http://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20',
            expected_redirect_url='http://hello.World.com/how_are_you_doing/you_World+?one=two&three#four+%20',
        )

    def test_shorten_url_with_ftp_protocol(self):
        """
        Scenario: User submits a long url with FtP:// protocol specified
            Given http client is initialized
              And no other long urls have been shortened yet

             When User submits a long url with FtP:// protocol specified (in mixed case)

             Then only one record exists in shortenedurl DB table
              And the long url is stored as is with no modification other than leading/training whitespaces stripped
                  (and empty query string and fragment removed and protocol lower-cased)
              And the service redirects from short url using 302 (temporary) redirect
              And the service redirects from short url to the long url that was stored (all illegal chars are escaped)
        """
        self._test_shorten_then_expand(
            long_url_input='   FtP://some/free/text-GOES%20here \n'
                           ' In [561]: %time method = [a for a in data if b.startswith(‘http’)] \t ?#      ',
            stored_long_url='ftp://some/free/text-GOES%20here \n'
                            ' In [561]: %time method = [a for a in data if b.startswith(‘http’)] \t ',
            expected_redirect_url='ftp://some/free/text-GOES%20here%20%0A'
                                  '%20In%20[561]:%20%time%20method%20=%20['
                                  'a%20for%20a%20in%20data%20if%20b.startswith(%E2%80%98http%E2%80%99)]%20%09%20',
        )

    @patch.object(shortener_storage, 'generate_url_handle', return_value='abc')
    def _test_shorten_then_expand(
            self, mock_generate_url_handle, long_url_input, stored_long_url, expected_redirect_url
    ):
        self.client.post('/shorten-url/', {
            'long_url': long_url_input,
        })

        rows = ShortenedUrl.objects.all()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].long_url, stored_long_url)

        response = self.client.get('/abc')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, expected_redirect_url)

    def test_unlimited_clicks(self):
        pass

    @patch.object(shortener_storage, 'generate_url_handle', return_value='abc')
    def test_404_after_3_clicks(self, mock_generate_url_handle):
        self.client.post('/shorten-url/', {
            'long_url': 'www.google.com',
        })

        shortened_url = ShortenedUrl.objects.all()[0]
        shortened_url.click_limit = 3
        shortened_url.save()

        for _ in range(3):
            response = self.client.get('/abc')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, 'http://www.google.com')

        response = self.client.get('/abc')
        self.assertEqual(response.status_code, 404)
