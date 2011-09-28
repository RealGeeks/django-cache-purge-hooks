from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from functools import partial
from cache_purge_hooks.manager import CacheManager
import logging

def __get_urls(instance, func):
	if func is not None:
		return func(instance)
	if hasattr(instance, 'get_absolute_urls'):
		return instance.get_absolute_urls()
	if hasattr(instance, 'get_absolute_url'):
		return [instance.get_absolute_url(),]
	return []

def __pre_save_hook(model, func, instance, sender, **kwargs):
	"""In case the url changes on the save, we need to see
	if the old url is different, because that needs to be
	invalidated."""
	try:
		old = sender.objects.get(pk=instance.pk)
	except sender.DoesNotExist:
		return
	old_urls = __get_urls(old, func)
	new_urls = __get_urls(instance, func)	
	if old_urls == new_urls:
		return
	with CacheManager() as cm:
		for url in old_urls:
			logging.info("expire:", url)
			cm.purge(url)

def __post_foo_hook(model, func, instance, **kwargs):
	urls = __get_urls(instance, func)
	with CacheManager() as cm:
		for url in urls:
			logging.info("expire:", url)
			cm.purge(url)

def cache_purge_hook(model, func=None):
	pre_save.connect(
		partial(__pre_save_hook, model, func),
		dispatch_uid="cache_purge_hook",
		sender = model,
		weak=False,
	)
	post_save.connect(
		partial(__post_foo_hook, model, func),
		dispatch_uid="cache_purge_hook",
		sender = model,
		weak=False,
	)
	post_delete.connect(
		partial(__post_foo_hook, model, func),
		dispatch_uid="cache_purge_hook",
		sender = model,
		weak=False,
	)

