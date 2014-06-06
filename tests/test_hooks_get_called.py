import mock
from sampleproject.sample.models import TestModel
from django.test.utils import override_settings
import pytest


@pytest.mark.django_db
@mock.patch('cache_purge_hooks.backends.varnishbackend.VarnishManager.purge')
def test_purge_on_save(purge):
    with override_settings(CACHE_PURGE_HOOKS_BACKEND='cache_purge_hooks.backends.varnishbackend.VarnishManager'):
        a = TestModel()
        a.save()
        purge.assert_called_with('/foo')
