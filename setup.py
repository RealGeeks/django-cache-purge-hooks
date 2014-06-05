from setuptools import setup, find_packages

setup(
    name = 'django-cache-purge-hooks',
    version = '0.3.1',
    packages = find_packages(),
    author = 'Shu Zong Chen',
    author_email = 'shu.chen@freelancedreams.com',
    description = 'Drop-in cache (e.g. varnish) purging hooks for django',
    long_description = "Pluggable django app to purge caches.",
    license = "MIT License",
    keywords = "django cache purge varnish nginx hook",
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
    url = 'https://github.com/RealGeeks/django-cache-purge-hooks'
)
