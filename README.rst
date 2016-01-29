========
Overview
========

.. image:: https://travis-ci.org/RealGeeks/django-cache-purge-hooks.svg?branch=master
    :target: https://travis-ci.org/RealGeeks/django-cache-purge-hooks

django-cache-purge-hooks is a reusable Django app to handle
cache invalidation.

This app basically provides a mechanism to easily hook into the
model callbacks to invalidate your front-end cache when needed.

There are currently two supported backends: varnish and Nginx

There were two hard things in computer science: naming things and cache
invalidation.  Now there is only one hard thing :neckbeard:

Support
=======

django-cache-purge hooks supports Django 1.4 - 1.7 and python versions 2.6 - 2.7

Usage
=====

Add 'cache_purge_hooks' to your INSTALLED_APPS.

::

    #our pretend model
    class Post(models.Model):
      title = models.CharField(max_length=200)
      slug = models.SlugField(unique=True,max_length=200)
      body = models.TextField(blank=True,null=True)

    from cache_purge_hooks import cache_purge_hook
    cache_purge_hook(Post)

As shown above, cache_purge_hooks module contains a function cache_purge_hook.  Pass in
as the first argument a model.  The cache mechanism piggy-backs on the model instance's
get_absolute_url() method and clears the backend cache for that particular url.

If any instance has multiple related urls, define a custom get_absolute_urls() method
that returns a list of urls to invalidate:

::

    class Category(models.Model):
      name = models.CharField(max_length=200)
      slug = models.SlugField(unique=True,max_length=200)
      title = models.CharField(max_length=127,blank=True)

      def get_absolute_url(self):
        return reverse("category", kwargs={
          "category": self.slug
        })

      def get_absolute_urls(self):
        gau = self.get_absolute_url()
        return [gau, reverse('blog_home'),]

In the above model, we have a blog post Category model. It's get_absolute_url() method
is tied to a particular named route defined in urls.py, but any change to the category
must also be reflected in the blog home page (say for example, the home page contains
a tag cloud of all categories).  That page must be invalidated when this information
is changed.

Notice you must also explicitly grab the get_absolute_url() value. It will not get
called if get_absolute_urls() exists.

If that isn't to your liking, you can also pass as a 2nd argument to purge_related_blog
a function that takes an instance and returns a list of urls.

For example:

::

    from facebook_comments.models import FacebookCommentCache
    def purge_related_blog(instance):
      pr = urlparse.urlparse(instance.url)
      return [pr.path, ]

    cache_purge_hook(FacebookCommentCache, purge_related_blog)

This is also useful because in the case above, the site is utilizing another reusable app
(facebook_cached_comments).  This is much better than hacking up a third party code to
provide a get_absolue_urls().


Configuration
=============

For Varnish backend:

`CACHE_PURGE_HOOKS_BACKEND = 'cache_purge_hooks.backends.varnishbackend.VarnishManager'`

or for (smart) Nginx backend:

`CACHE_PURGE_HOOKS_BACKEND = 'cache_purge_hooks.backends.nginxbackend.NginxManager'`

or for the dumb Nginx backend:

`CACHE_PURGE_HOOKS_BACKEND = 'cache_purge_hooks.backends.dumbnginxbackend.DumbNginxManager'`


Varnish Backend
---------------

NOTE: The varnish backend works by forking and calling `varnishadm`, so you'll
need that installed on your machine for it to work

All settings are optional.

- VARNISHADM_HOST: host of varnish management interface. Defaults to `"localhost"`
- VARNISHADM_PORT: port of varnish management interface. Defaults to `6082`
- VARNISHADM_SECRET: file path of varnish secret. Be sure to give read permission to your
  django process. Defaults to `"/etc/varnish/secret"`
- VARNISHADM_SITE_DOMAIN: the site domain used to purge the urls. Regex is allowed.
  Defaults to `".*"`
- VARNISHADM_BIN: path to `varnishadm` executable. Defaults to `"/usr/bin/varnishadm"`

You might want to configure a logger for `'django.cache_purge_hooks'` on `LOGGING`,
see the django docs for more details on `LOGGING` setting.

NGINX Backend
-------------

The nginx backend takes a bit of work to set up.  You'll need the
`ngx_cache_purge`_ module installed.  Then, you will need to set up the
nginx.conf like this.  If you already have your proxy_cache stuff set up, just
add the `proxy_cache_purge` section. (see `ngx_cache_purge`_ README for more):


::

    http {
        proxy_cache_path  /tmp/cache  keys_zone=tmpcache:10m;

        server {
            location / {
                proxy_pass         http://127.0.0.1:8000;
                proxy_cache        tmpcache;
                proxy_cache_key    $uri$is_args$args;
                proxy_cache_purge  PURGE from 127.0.0.1;
            }
        }
    }


Finally, Set the following configuration options in your settings.py:

- NGX_CACHE_PURGE_HOST: nginx hostname to send PURGE command to (defaults to
  localhost)
- NGX_CACHE_PURGE_PORT: port to send PURGE command to (defaults to
  80)
- NGX_CACHE_PURGE_HOST_HEADER: If you want to fake the "Host" header
  (maybe to get around DNS) you can do that with this option.

Dumb NGINX Backend
-------------

The dumb nginx backend works by just deleting the entire nginx cache directory.  You'll need to give it the path to the directory:

- DUMB_NGINX_CACHE_PURGE_DIR = '/tmp/nginx_cache'


Running Tests
=============

Run tests with ./runtests.sh.

You can run tests in all supported environments by running tox.

Changelog
============
  * 0.5.0: Add dumb nginx cache purge backend
  * 0.4.2: Add dummy cache backend that does nothing, for testing
  * 0.4.1: Add NGX_CACHE_PURGE_HOST_HEADER option
  * 0.4.0: Added nginx backend


Contributors
============

  * `Shu Zong Chen`_
  * `Igor Sobreira`_
  * `Kevin McCarthy`_

.. CONTRIBUTORS

.. _`Shu Zong Chen`: http://freelancedreams.com/
.. _`Igor Sobreira`: http://igorsobreira.com/
.. _`Kevin McCarthy`: http://kevinmccarthy.org/

.. _`ngx_cache_purge`: https://github.com/FRiCKLE/ngx_cache_purge
