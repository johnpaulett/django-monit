from setuptools import setup, find_packages
import monit

setup(
    name = 'django-monit',
    version = monit.__version__,
    packages = find_packages(),
    author = 'John Paulett',
    author_email = 'john@paulett.org',
    description = 'A simple Django-based Monit collector',
    license = 'BSD',
    keywords = 'monit monitoring django',
    url = 'http://github.com/johnpaulett/django-monit',
    install_requires = ['lxml'],
)
