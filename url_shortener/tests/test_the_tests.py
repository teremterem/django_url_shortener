from django.test import TestCase

from ..models import ShortenedUrl


class TestTestCase(TestCase):
    """
    Test the tests (make sure test interactions with the database are isolated).
    """

    def test_only_one_table_row_1(self):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        ShortenedUrl.objects.create(id='111')

        rows = ShortenedUrl.objects.all()
        id_list = [row.id for row in rows]
        self.assertCountEqual(id_list, ['111'])

    def test_only_one_table_row_2(self):
        """
        Make sure test_only_one_table_row_1 and test_only_one_table_row_2 don't influence each other.
        """
        ShortenedUrl.objects.create(id='222')

        rows = ShortenedUrl.objects.all()
        id_list = [row.id for row in rows]
        self.assertCountEqual(id_list, ['222'])

    def test_two_table_rows(self):
        ShortenedUrl.objects.create(id='444')
        ShortenedUrl.objects.create(id='333')

        rows = ShortenedUrl.objects.all()
        id_list = [row.id for row in rows]
        self.assertCountEqual(id_list, ['333', '444'])
