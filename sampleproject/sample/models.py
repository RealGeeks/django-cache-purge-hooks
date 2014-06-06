from django.db import models
from cache_purge_hooks import cache_purge_hook

class TestModel(models.Model):
    a_field = models.CharField(max_length=20)

    def get_absolute_url(self):
        return '/foo'

cache_purge_hook(TestModel)
