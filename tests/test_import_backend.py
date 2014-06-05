from django.test.utils import override_settings
from cache_purge_hooks.manager import _get_manager

@override_settings(CACHE_PURGE_HOOKS_BACKEND='cache_purge_hooks.backends.varnishbackend.VarnishManager')
def test_import_varnish_backend():
    assert _get_manager()

@override_settings(CACHE_PURGE_HOOKS_BACKEND='cache_purge_hooks.backends.nginxbackend.NginxManager')
def test_import_nginx_backend():
    assert _get_manager()
