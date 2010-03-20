django-monit - A Simple Monit Collector
=======================================


.. warning::

    django-monit is currently very preliminary and is best for people who
    are comfortable installing reusable apps in Django projects.

django-monit is a very dumb (but free) replacement for `M/Monit`_, the commerical 
product built around the amazing Monit_ management and monitoring tool.

django-monit is a reusable Django_ application providing a central Monit 
"collector" and storage of the Monit nodes' information and events.  Currently,
django-monit is can be installed as an app within an existing Django site.
In the future, a tool could built a simple Django project if someone wished
to only deploy django-monit.

django-monit has been tested on the Django 1.2 RC using Monit 5.0.3 provided
as a Ubuntu 9.10 package.

.. _Monit: http://mmonit.com/monit/
.. _`M/Monit`: http://mmonit.com/
.. _Django: http://www.djangoproject.com

 
Installation
-------------

The easiest way to install django-monit is via pip::

    pip install django-monit

However, if you have the source, you can build it yourself::

    python setup.py install


Dependencies
-------------

 - Django
 - lxml

