from django.db.models.signals import (
    post_save,
    post_delete,
    pre_delete,
    pre_save
)
from functools import partial
from cache_purge_hooks.manager import CacheManager
import logging


def __get_urls(instance, func):
    if func is not None:
        return func(instance)
    if hasattr(instance, 'get_absolute_urls'):
        return instance.get_absolute_urls()
    if hasattr(instance, 'get_absolute_url'):
        return [instance.get_absolute_url()]
    return []


def __pre_save_hook(model, func, instance, sender, **kwargs):
    """
    In case the url changes on the save, we need to save the
    old urls because those pages need to be invalidated.
    """
    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    instance.__cache_prehook_urls = set(__get_urls(old, func))


def __post_save_hook(model, func, instance, **kwargs):
    urls = set(__get_urls(instance, func))
    try:
        urls = urls.union(instance.__cache_prehook_urls)
    except AttributeError:
        pass
    with CacheManager() as cm:
        for url in urls:
            logging.info("expire:", url)
            cm.purge(url)


def __pre_delete_hook(model, func, instance, **kwargs):
    instance.__cache_prehook_urls = set(__get_urls(instance, func))


def __post_delete_hook(model, func, instance, **kwargs):
    urls = instance.__cache_prehook_urls
    with CacheManager() as cm:
        for url in urls:
            logging.info("expire:", url)
            cm.purge(url)


def cache_purge_hook(model, func=None):
    pre_save.connect(
        partial(__pre_save_hook, model, func),
        dispatch_uid="cache_purge_hook",
        sender=model,
        weak=False,
    )
    post_save.connect(
        partial(__post_save_hook, model, func),
        dispatch_uid="cache_purge_hook",
        sender=model,
        weak=False,
    )
    pre_delete.connect(
        partial(__pre_delete_hook, model, func),
        dispatch_uid="cache_purge_hook",
        sender=model,
        weak=False,
    )
    post_delete.connect(
        partial(__post_delete_hook, model, func),
        dispatch_uid="cache_purge_hook",
        sender=model,
        weak=False,
    )
