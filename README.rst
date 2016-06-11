Overview 

.. image:: https://travis-ci.org/liboz/suds-lxml.svg?branch=master :target: https://travis-ci.org/liboz/suds-lxml
.. image:: https://coveralls.io/repos/github/liboz/suds-lxml/badge.svg?branch=master :target: https://coveralls.io/github/liboz/suds-lxml?branch=master 

=================================================

"Suds" is a lightweight SOAP-based web service client for Python licensed under
LGPL (see the ``LICENSE.txt`` file included in the distribution).

One major problem with suds is that it is slow. 
This is a fork of suds that tries to solve it by parse the xml returned 
with the **fast** lxml parser instead of the default suds implementation.

**Forked project information**

* Project site - https://github.com/liboz/suds-lxml
* Official releases can be downloaded from:

  * BitBucket - http://bitbucket.org/jurko/suds/downloads
  * PyPI - http://pypi.python.org/pypi/suds-jurko

**Original suds Python library development project information**

* Project site - http://fedorahosted.org/suds
* Documentation - http://fedorahosted.org/suds/wiki/Documentation
* Epydocs - http://jortel.fedorapeople.org/suds/doc

For development notes see the ``HACKING.rst`` document included in the
distribution.


Installation
=================================================

Standard Python installation.

Here are the basic instructions for 3 different installation methods:

#. Using ``pip``

   * Have the ``pip`` package installed.
   * Run ``pip install suds-jurko``.

#. Using ``easy-install``

   * Have the ``setuptools`` package installed.
   * Run ``easy_install suds-jurko``.

#. From sources

   * Unpack the source package somewhere.
   * Run ``python setup.py install`` from the source distribution's top level
     folder.
