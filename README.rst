========
Overview
========

django-cache-purge-hooks is a reusable Django app to handle
cache invalidation.

This app basically provides a mechanism to easily hook into the
model callbacks to invalidate your front-end cache when needed.

Currently, only a varnish backend is implemented, but the design
was created with other possible backends in mind.

Dependencies
============

django-facebook-comments was created in Django 1.3.  Please let me
know if you have success with it in lower versions.

Also requires python-varnish package for varnish backends.

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

No configuation options yet.

Contributors
============

  * `Shu Zong Chen`_

.. CONTRIBUTORS

.. _`Shu Zong Chen`: http://freelancedreams.com/
