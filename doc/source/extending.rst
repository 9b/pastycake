Extending pastycake
===================

Adding a new Paste Source
-------------------------

Adding support for a paste source is simply following these steps:

  * create a new file with the pattern ``<servicename>_source.py`` where
    ``<servicename>`` is the name of the paste that you want to support.

  * add ``from pastesource import PasteSource`` to the top of the file.
  * create a class ``<Servicename>Source`` that inherits ``PasteSource``.
  * implement all methods of the ``PasteSource`` abc.
  * (optional) write a setup.py that specifies the proper entry point for the
    ``<ServiceName>Source``. The namespace for this is
      
      - ``pastycake`` if you want to submit it for inclusion into the core, or
      - ``pastycake.ext`` otherwise.


Adding a new Storage Backend
----------------------------

.. important::

   This section reflects the latest development but the requirements still
   change quite often as new functionality is added.

Supporting a new storage backend is a bit more complicated:

  * create a new file with the pattern ``<storagename>_backend.py`` where
    ``<storagename>`` is the name of the backend that you want to support.

  * add ``from storage_backend import StorageBackend`` to the top of the file.
  * create a class ``<Storagename>Backend`` that inherits ``StorageBackend``.
  * implement all methods of the ``StorageBackend`` abc.

  * (optional) write a setup.py that specified the proper entry point for the
    ``<Storagename>Backend``. The namespace for this is the same as above.


Adding a new Storage Backend that supports Keyword refreshing
-------------------------------------------------------------

combine the above steps with the following:

  * also add ``from keywords import KeywordStorage``
  * also inherit from ``KeywordStorage``
  * also implement all methods/params of the ``KeywordStorage`` abc.
.. important::

    You have to re-decorate the ``@abc.abstractproperty`` methods with
    ``@property``
