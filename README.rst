Purpose
=======
Search through Paste services such as pastebin.com for interesting pastes
based on keywords

Supported Pastes
================
* pastebin.com
* pastie.org

License
=======
`3-Clause "New" BSD License`__ , see the file LICENSE.rst for details.

.. __: http://www.opensource.org/licenses/BSD-3-Clause

Files
=====
* ``pastycake-snatch.py`` -
  outputs to the command line and uses the ``tracker.txt`` file to monitor
  previously seen URLs
* ``pastycake-harvest.py`` -
  stores data inside of SQLite instead of a text file

Plans
=====
* Create easy way to add in keywords (done)
* Replace nesting with generators (done)
* Add in emailer (done)
