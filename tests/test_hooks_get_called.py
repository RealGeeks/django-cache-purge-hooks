from cache_purge_hooks import cache_purge_hook
from sampleproject.sample.models import TestModel
from django.test.utils import override_settings
import pytest


cache_purge_hook(TestModel)

@pytest.mark.django_db
def test_purge_on_save():
    with override_settings(CACHE_PURGE_HOOKS_BACKEND='cache_purge_hooks.backends.nginxbackend.NginxManager'):
        a = TestModel()
        a.save()
