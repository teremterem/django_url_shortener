from django.db import models


class ShortenedUrl(models.Model):
    url_uuid = models.CharField(max_length=50, unique=True)
