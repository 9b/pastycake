Keyword (Re-)loading
--------------------

pastycake can query an instance of the ``KeywordStorage`` abc for a(n updated)
list of keywords to use.

It checks the (in SQL lingo) table ``matchers`` for rows where the ``enabled``
field is equal to ``True``. For each matching row, it'll return the
``match_expression`` field.

En-/Dis-abling a Keyword
~~~~~~~~~~~~~~~~~~~~~~~~

The abc offers the methods ``enable_keyword`` and ``disable_keyword`` to do
that from within python in a backend-neutral manner (as in you don't have to
write custom SQL instructions).

