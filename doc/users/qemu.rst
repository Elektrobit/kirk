.. SPDX-License-Identifier: GPL-2.0-or-later

Configuring a Qemu instance
===========================

Kirk provides support for running LTP tests inside a Qemu virtual machine.

VM configuration
----------------

To enable console on a tty device for a VM, follow these steps:

* open the ``/etc/default/grub`` file.
* add ``console=ttyS0,console=tty0`` to the ``GRUB_CMDLINE_LINUX`` line.
* run the following command to update the GRUB configuration:

   .. code-block:: bash

       grub-mkconfig -o /boot/grub/grub.cfg

.. warning::

    If you set the ``serial=virtio`` backend option, then use ``console=hvc0`` instead.

Configuration options
---------------------

The Qemu communication channel supports the following parameters:

* ``image``: Path to the Qemu disk image
* ``kernel``: Path to a custom kernel image (optional)
* ``initrd``: Path to an initrd image (optional)
* ``user``: Username to log in (default: ``''``)
* ``password``: User password (default: ``''``)
* ``prompt``: Shell prompt character (default: ``#``)
* ``system``: System architecture (default: ``x86_64``)
* ``ram``: RAM allocated to the VM (default: ``2G``)
* ``smp``: Number of CPUs (default: ``2``)
* ``serial``: Serial protocol: ``isa`` or ``virtio`` (default: ``isa``)
* ``virtfs``: Directory to mount inside VM via 9p (optional)
* ``options``: Additional Qemu options (optional)

Examples
--------

Run tests on a Qemu VM disk image:

.. code-block:: bash

    kirk --com qemu:image=/path/to/image.qcow2:user=root:password=root \
         --sut default:com=qemu \
         --run-suite syscalls
