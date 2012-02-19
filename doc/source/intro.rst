Introduction to Pastycake
=========================

Pastycake by itself is a package that allows one to collect data off of paste
services such as pastebin.com .

It provides 3 scripts, ``pastycake``, ``pastycake-harvest`` and
``pastycake-snatch``, to make it easy to use right out of the box. The two
latter scripts are merely frontends to ``pastycake`` as they define the gather
mode.

Gather modes
------------

There are two gather modes so far:

  * ``harvest`` Continue forever with the gathering while taking small naps in
    between.
  * ``snatch`` Check for the latest&greatest, then stop.

Program Options
---------------

See the output of ``pastycake -h`` for details.

