from django.db import models


class ShortenedUrl(models.Model):
    id = models.BigIntegerField(primary_key=True)
    long_url = models.TextField(blank=False, null=False)
