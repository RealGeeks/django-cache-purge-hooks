from cache_purge_hooks.backends.varnishbackend import VarnishManager

class CacheManager(object):
	def __init__(self):
		self.manager = VarnishManager()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.manager.close()

	def purge(self, command):
		self.manager.purge(command)

	def purge_all(self):
		self.manager.purge_all()
