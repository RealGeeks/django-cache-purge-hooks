#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = 'django-cache-purge-hooks',
	version = '0.3.0',
	packages = find_packages(),
	#include_package_data = True,
	#package_data={
	#	'cache_purge_hooks': ['templates/cache_purge_hooks/*.html',],
	#},
	author = 'Shu Zong Chen',
	author_email = 'shu.chen@freelancedreams.com',
	description = 'Drop-in cache (e.g. varnish) purging hooks for django',
	long_description = \
"""
Pluggable django app to purge caches. (Only works for varnish currently, but we intend this to work with multiple backends)
""",
	license = "MIT License",
	keywords = "django cache purge varnish hook",
	classifiers = [
		'Development Status :: 5 - Production/Stable',
		'Environment :: Web Environment',
		'Framework :: Django',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Application Frameworks',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	platforms = ['any'],
	url = 'https://bitbucket.org/realgeeks/django-cache-purge-hooks',
	download_url = 'https://bitbucket.org/realgeeks/django-cache-purge-hooks/downloads',
)

