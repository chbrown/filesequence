File sequences
--------------

A ``FileSequence`` allows you to write to multiple files using standard
Python file descriptor read / write functionality.

You specify the file size limit and naming scheme when opening the
sequence, but the library handles creating new files as needed.

Each call to the opened FileSequence's ``write`` function will
potentially create a new file, if the chunk you want to write will push
the file over the limit. So if you want to only split files on newlines,
call ``write()`` once for each line. If you want behavior more like
BSD's ``split`` command, you can write one byte at a time. Though, at
that rate, ``split`` is probably the better choice.

Installation |PyPI version|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pip install filesequence

API
~~~

You can simply use a FileSequence object as if it were a file.

-  ``filesequence.open(...)`` returns a ``FileSequence`` object.
-  ``my_file_sequence.write(line)`` takes a line and writes it to the
   next available file.

Note that FileSequence requires ``with`` wrapping, as opposed to the
Python built-in ``open()``:

::

    import filesequence

    filenames = filesequence.interpolator('numbers-%02d.txt', xrange(1000))

    with filesequence.open(filenames, 1000000) as out:
        for a in xrange(1000):
            for b in xrange(1000):
                out.write('# %d * %d = %d\n' % (a, b, a * b))

Now you have a huge multiplication table in 20 different files that are
1MB or less! So awesome!

Want to keep going?

::

    filenames = filesequence.interpolator('numbers-%02d.txt', xrange(1000))

    with filesequence.open(filenames, 1000000, 'a') as out:
        ...

The 'a' flag will make the sequence jump to the last existing file, and
start writing from there.

Bonus
~~~~~

A ``filesequence`` script will be installed to your ``PATH``. This
script reads STDIN line by line and command line arguments for the
filename ``pattern`` and filesize limit (see ``filesequence --help``),
and writes out a series of files of at most that filesize and without
breaking any lines.

::

    $ filesequence --help

    usage: cli.py [-h] [--limit LIMIT] [--pattern PATTERN] [--version]

    Write STDIN into a sequence of files, splitting only at newlines

    optional arguments:
      -h, --help         show this help message and exit
      --limit LIMIT      Maximum bytes per file (default: 50000000)
      --pattern PATTERN  Filename string pattern: generate filenames in sequence
                         by interpolating `pattern % indices.next()`
                         (default: split.%02d)
      --version          show program's version number and exit

TODO
----

-  Support reading (flags ``r`` and ``r+``).

Development
-----------

This package is published to PyPI at
`pypi.python.org/pypi/filesequence <https://pypi.python.org/pypi/filesequence/>`__.

-  Run ``python publish.py -n`` to print out the suggested publish
   sequence.
-  Run ``python publish.py`` to run the suggested publish sequence.

License
-------

Copyright (c) 2013 Christopher Brown. `MIT
Licensed <https://raw.github.com/chbrown/filesequence/master/LICENSE>`__.

.. |PyPI version| image:: https://badge.fury.io/py/filesequence.png
   :target: http://badge.fury.io/py/filesequence
