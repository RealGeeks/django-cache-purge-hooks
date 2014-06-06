from django.conf import settings
try:
    from django.utils import import_string
except ImportError:
    try:
        from django.utils import import_by_path as import_string
    except ImportError:
        from cache_purge_hooks.utils import import_by_path as import_string

def _get_manager():
    manager_cls =  import_string(settings.CACHE_PURGE_HOOKS_BACKEND)
    return manager_cls()

class CacheManager(object):
	def __init__(self):
		self.manager = _get_manager()

	def __enter__(self):
		return self

        def __exit__(self, *args):
            if hasattr(self.manager, 'close'):
                self.manager.close()

	def purge(self, command):
		self.manager.purge(command)

	def purge_all(self):
		self.manager.purge_all()
