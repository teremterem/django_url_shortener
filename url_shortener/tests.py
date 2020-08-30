from django.test import TestCase

from url_shortener.models import ShortenedUrl


class TestTestCase(TestCase):
    """
    Test the tests (make sure interactions with the database are isolated).
    """

    def test_only_one_table_row_1(self):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        ShortenedUrl.objects.create(url_uuid='uuid1')

        rows = ShortenedUrl.objects.all()
        uuid_list = [u.url_uuid for u in rows]
        self.assertCountEqual(uuid_list, ['uuid1'])

    def test_only_one_table_row_2(self):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        ShortenedUrl.objects.create(url_uuid='uuid2')

        rows = ShortenedUrl.objects.all()
        uuid_list = [u.url_uuid for u in rows]
        self.assertCountEqual(uuid_list, ['uuid2'])

    def test_two_table_rows(self):
        ShortenedUrl.objects.create(url_uuid='uuid3')
        ShortenedUrl.objects.create(url_uuid='uuid4')

        rows = ShortenedUrl.objects.all()
        uuid_list = [u.url_uuid for u in rows]
        self.assertCountEqual(uuid_list, ['uuid3', 'uuid4'])
