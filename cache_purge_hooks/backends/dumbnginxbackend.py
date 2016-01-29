import shutil
import requests
from django.conf import settings

class DumbNginxManager(object):
    def purge(self, path):
        shutil.rmtree(settings.DUMB_NGINX_CACHE_PURGE_DIR)
