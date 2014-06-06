import logging
import subprocess

from django.conf import settings

logger = logging.getLogger('django.cache_purge_hooks')

VARNISHADM_HOST = getattr(settings, 'VARNISHADM_HOST', 'localhost')
VARNISHADM_PORT = getattr(settings, 'VARNISHADM_PORT', 6082)
VARNISHADM_SECRET = getattr(settings, 'VARNISHADM_SECRET', '/etc/varnish/secret')
VARNISHADM_SITE_DOMAIN = getattr(settings, 'VARNISHADM_SITE_DOMAIN', '.*')
VARNISHADM_BIN = getattr(settings, 'VARNISHADM_ADM_BIN', '/usr/bin/varnishadm')

class VarnishManager(object):

    def purge(self, url):
        command = 'ban req.http.host ~ "{host}" && req.url ~ "{url}"'.format(
            host=VARNISHADM_SITE_DOMAIN.encode('ascii'),
            url=url.encode('ascii'),
        )
        self.send_command(command)

    def purge_all(self):
        self.purge('.*')

    def send_command(self, command):
        args = [VARNISHADM_BIN, '-S', VARNISHADM_SECRET, '-T', VARNISHADM_HOST+':'+str(VARNISHADM_PORT), command]
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as error:
            logger.error('Command "{0}" returned {1}'.format(' '.join(args), error.returncode))
            return False
        else:
            logger.debug('Command "{0}" executed successfully'.format(' '.join(args)))
            return True
