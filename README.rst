Overview
=================================================

"Suds" is a lightweight SOAP-based web service client for Python licensed under
LGPL (see the ``LICENSE.txt`` file included in the distribution).

This is a fork of suds that gives the option to parse the lxml with xml 
instead of the default suds implementation.

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

Installation troubleshooting:
-----------------------------

* Released prior to ``0.7`` have many known installation issues requiring the
  target Python environment to be manually prepared when using some ancient
  Python versions, e.g. 2.4, 2.5 or 3.1.
* Releases ``0.4.1. jurko 5 < x <= 0.6`` may not be installed using ``pip`` into
  a Python environment with an already installed ``setuptools`` package older
  than the version expected by our project. Displayed error message includes
  instructions on how to manually upgrade the installed ``setuptools`` package
  before rerunning our installation.

  * ``pip`` internally imports existing ``setuptools`` packages before running
    our setup, thus preventing us from upgrading the existing ``setuptools``
    installation inplace.

* If automated ``setuptools`` Python package installation fails (used in
  releases ``0.4.1 jurko 5`` and later), e.g. due to PyPI web site not being
  available, user might need to install it manually and then rerun the
  installation.
* Releases prior to ``0.4.1. jurko 5`` will fail if the ``distribute`` Python
  package is not already installed on the system.
* Python 2.4.3 on Windows has problems using automated ``setuptools`` Python
  package downloads via the HTTPS protocol, and therefore does not work
  correctly with PyPI which uses HTTPS links to all of its packages. The same
  does not occur when using Python version 2.4.4.
