.. SPDX-License-Identifier: GPL-2.0-or-later

Configuring LTX communication
=============================

LTX is an *optional* feature in kirk that allows running LTP tests using the
LTX communication protocol.

Prerequisites
-------------

LTX support requires the `msgpack <https://pypi.org/project/msgpack/>`_ package,
which can be installed via the ``ltx`` extra:

.. code-block:: bash

    pip install 'kirk[ltx]'

or directly:

.. code-block:: bash

    pip install msgpack

Configuration options
---------------------

The LTX communication channel supports the following parameters:

* ``infile``: Path to the input file where LTX is reading data
* ``outfile``: Path to the output file where LTX is writing data

Examples
--------

Run tests using LTX communication channel:

.. code-block:: bash

    kirk --com ltx:infile=/path/to/in:outfile=/path/to/out \
         --sut default:com=ltx \
         --run-suite syscalls
