from django.db import models

class TestModel(models.Model):
    a_field = models.CharField(max_length=20)

    def get_absolute_url(self):
        return 'foo'
