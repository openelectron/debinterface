Tests
============

We use pytest, but unittest is still the used style.
I plan on linking this codecov or similar.

Full test
---------
.. sourcecode:: shell

    cd test
    py.test --cov=debinterface test

To have it work with breakpoints
--------------------------------
.. sourcecode:: shell

    cd test
    py.test --cov=debinterface test -s
