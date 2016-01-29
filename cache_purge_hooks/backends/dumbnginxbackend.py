import os
import shutil
import requests
from django.conf import settings

def clear_dir(target_dir):
    # Gather directory contents
    contents = [os.path.join(target_dir, i) for i in os.listdir(target_dir)]

    # Iterate and remove each item in the appropriate manner
    [shutil.rmtree(i) if os.path.isdir(i) else os.unlink(i) for i in contents]

class DumbNginxManager(object):
    def purge(self, path):
        clear_dir(settings.DUMB_NGINX_CACHE_PURGE_DIR)
