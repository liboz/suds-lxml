Overview 

.. image:: https://travis-ci.org/liboz/suds-lxml.svg?branch=master
    :target: https://travis-ci.org/liboz/suds-lxml
.. image:: https://coveralls.io/repos/github/liboz/suds-lxml/badge.svg?branch=master 
    :target: https://coveralls.io/github/liboz/suds-lxml?branch=master 

=================================================

Based on the original 'suds' project by Jeff Ortel (jortel at redhat
dot com) hosted at 'http://fedorahosted.org/suds' and 'suds-jurko' by 
Jurko Gospodnetić ( jurko.gospodnetic@pke.hr ) 
hosted at https://bitbucket.org/jurko/suds.

"Suds" is a lightweight SOAP-based web service client for Python licensed under
LGPL (see the ``LICENSE.txt`` file included in the distribution).

One major problem with suds is that it is slow. 
This is a fork of suds that tries to solve it by parse the xml returned 
with the **fast** lxml parser instead of the default suds implementation.
It requires lxml to be installed.

I was initially inspired by http://stackoverflow.com/questions/22171100/python2-sax-parser-best-speed-and-performance-for-large-files.

**Forked project information**

* Project site - https://github.com/liboz/suds-lxml
* Official releases can be downloaded from:

  * PyPI - http://pypi.python.org/pypi/suds-lxml

**Original suds Python library development project information**

* Project site - http://fedorahosted.org/suds
* Documentation - http://fedorahosted.org/suds/wiki/Documentation
* Epydocs - http://jortel.fedorapeople.org/suds/doc

.. For development notes see the ``HACKING.rst`` document included in the
.. distribution.


Installation
=================================================

Standard Python installation.

Here are the basic instructions for 3 different installation methods:

#. Using ``pip``

   * Have the ``pip`` package installed.
   * Run ``pip install suds-lxml``.

#. Using ``easy-install``

   * Have the ``setuptools`` package installed.
   * Run ``easy_install suds-lxml``.

#. From sources

   * Unpack the source package somewhere.
   * Run ``python setup.py install`` from the source distribution's top level
     folder.

Usage
=================================================

I attempt to give the same APIs to call webservices as the original suds, 
the only difference is what the calls themselves do. The python objects 
that are created are not the standard suds objects either and are just a simple
dict like object.

Simple:


.. code-block:: python

    from suds.lxmlclient import Client
    c = Client('https://www.yourwsdl.com?wsdl')
    
To Access to the original client:


.. code-block:: python

    from suds.lxmlclient import Client
    c = Client('https://www.yourwsdl.com?wsdl')
    original_client = c.suds_client
    
To convert the returned SoapObject to a dictionary (note that this isn't recursive):

.. code-block:: python

    from suds.lxmlclient import Client
    c = Client('https://www.yourwsdl.com?wsdl')
    result = c.service.test()
    result.as_dict()

To accessing a property on a SoapObject:

.. code-block:: python

    from suds.lxmlclient import Client
    c = Client('https://www.yourwsdl.com?wsdl')
    result = c.service.test()
    success = result.success
     
 
Benchmarks
=================================================

This project was started because I had to deal with large SOAP return envelopes
and wanted to use suds. However, it was simply too slow.

Here are some initial benchmarks for just the parsing on a 30 MB return envelope.
We take the average over 10 iterations:

``suds-jurko baseline:` 18.1 seconds for deserialize/to_python`

``suds-lxml: 0.115s for lxml deserialize, 4.09s for to_python``

Or about 4 times faster.