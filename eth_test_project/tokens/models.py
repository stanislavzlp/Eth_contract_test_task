from django.db import models


class Token(models.Model):
    """
    Token model
    """
    unique_hash = models.CharField(max_length=20, unique=True, blank=True)
    tx_hash = models.CharField(max_length=80, blank=True)
    media_url = models.URLField()
    owner = models.CharField(max_length=50)
