.. SPDX-License-Identifier: GPL-2.0-or-later

Configuring SSH communication
=============================

SSH is an *optional* feature in kirk that allows running LTP tests on a remote
host over SSH.

Prerequisites
-------------

SSH support requires the `asyncssh <https://pypi.org/project/asyncssh/>`_
package, which can be installed via the ``ssh`` extra:

.. code-block:: bash

    pip install 'kirk[ssh]'

or directly:

.. code-block:: bash

    pip install asyncssh

Configuration options
---------------------

The SSH communication channel supports the following parameters:

* ``host``: IP address or hostname of the remote target (default: ``localhost``)
* ``port``: TCP port of the SSH service (default: ``22``)
* ``user``: Username to log in (default: ``root``)
* ``password``: Password for authentication
* ``key_file``: Path to private key file for key-based authentication
* ``reset_cmd``: Command to reset the remote target if it becomes unresponsive
* ``sudo``: Use sudo to access root shell (default: ``0``)
* ``known_hosts``: Path to a custom ``known_hosts`` file (optional)

Examples
--------

Run tests over SSH using key authentication:

.. code-block:: bash

    kirk --com ssh:host=192.168.0.1:user=root:key_file=/home/user/.ssh/id_rsa \
         --sut default:com=ssh \
         --run-suite syscalls

Run tests over SSH in parallel using password authentication:

.. code-block:: bash

    kirk --com ssh:host=192.168.0.1:user=root:password=secret \
         --sut default:com=ssh \
         --workers 16 \
         --run-suite syscalls
