import mock
from django.test.utils import override_settings
from cache_purge_hooks.backends.nginxbackend import NginxManager

@override_settings(NGX_CACHE_PURGE_HOST='localhost', NGX_CACHE_PURGE_PORT='80')
@mock.patch('cache_purge_hooks.backends.nginxbackend.requests')
def test_purge_url(requests):
    nm = NginxManager()
    nm.purge('/test/')
    requests.request.assert_called_with('PURGE', 'http://localhost:80/test/')
