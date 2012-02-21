Installing pastycake
====================

Installation of pastycake is not (yet) totally straight forward.

Requirements
------------

Required packages, besides Python ..math:`>= 2.6`, are:

  * Louie
  * httplib2
  * lxml

In case of Python 2.6 and Python 3.x ..math:`< 3.2`, it also needs the
``argparse`` module.

Optional packages, that enable certain features/extensions, are:

  * pymongo (for MongoDB backend support)


Python 3 Compatibility
----------------------

Pastycake by itself is Python 3 compatible through the use of 2to3.
However, some libraries that it needs to work are not.


Installing pastycake
--------------------

Except for the above Python 3 compatibility issue, the install is fairly easy::

  python setup.py sdist
  pip install dist/pastycake-<version>.tar.gz

or simply::

  python setup.py install
