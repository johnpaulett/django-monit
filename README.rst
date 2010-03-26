django-monit - A Simple Monit Collector
=======================================


.. warning::

    django-monit is currently very preliminary and is best for people who
    are comfortable installing reusable apps in Django projects.

django-monit is a very dumb (but free) replacement for `M/Monit`_, the commerical 
product built around the amazing Monit_ management and monitoring tool.

django-monit is a reusable Django_ application providing a central Monit 
"collector" and storage of the Monit nodes' information and events.  Currently,
django-monit can be installed as an app within an existing Django site.
In the future, a tool could build a simple Django project if someone wished
to only deploy django-monit.

At this point, django-monit only acts as a collector of information from any 
number of Monit nodes, and can not push restart commands to the nodes as M/Monit
can do.

My goal currently is to create a tool for making Monit data easily accessible
from a Django project, rather than acting as a replacement for M/Monit. 

django-monit has been tested on the Django 1.2 trunk using Monit 5.0.3 provided
as a Ubuntu 9.10 package.

.. _Monit: http://mmonit.com/monit/
.. _`M/Monit`: http://mmonit.com/
.. _Django: http://www.djangoproject.com

 
Installation
-------------

The easiest way to install django-monit is via pip::

    pip install django-monit

Add `'monit'` to the INSTALLED_APPS in your settings.py

Add `url(r'^monit/', include('monit.urls'))` in your urls.py::

    urlpatterns = patterns('',
        url(r'^app/', include('yourapp.urls')),
        url(r'^monit/', include('monit.urls')),
        (r'^admin/', include(admin.site.urls)),
    )


Configure Monit
---------------

In the `monitrc`, you should configure your django-monit instance as a collector::

    set mmonit http://monit:monit@192.168.1.10:8000/monit/collector


Dependencies
-------------

 - Django (tested on pre-1.2 trunk)
 - lxml

Testing
-------

If you have `checked out <http://github.com/johnpaulett/django-monit>`_ the 
source, you can run the test suite, which uses a simple Django project
in the test_project folder::

    cd test_project
    # create a virtualenv and install the dependencies
    create_env.sh
    # run the tests
    ./manage.py test monit

