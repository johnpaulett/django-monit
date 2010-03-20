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

At this point, django-monit only acts as a collector of information from any 
number of Monit nodes, and can not push restart commands to the nodes as M/Monit
can do.

My goal currently is to create a tool for making Monit data easily accessible
from a Django project, rather than 

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

Configure Monit
---------------

In the `monitrc`, you should configure your django-monit instance as a collector::

    set mmonit http://monit:monit@192.168.1.10:8000/monit/collector


Dependencies
-------------

 - Django
 - lxml

