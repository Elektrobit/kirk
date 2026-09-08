.. SPDX-License-Identifier: GPL-2.0-or-later

Customization with plugins
==========================

Kirk provides an extensible plugin system to support custom testing
environments and communication protocols. When default communication channels
or standard System Under Test (SUT) setups do not cover your target
infrastructure, you can implement custom plugins without modifying the kirk
codebase.

Overview
--------

Kirk defines two types of plugins:

* **SUT (System Under Test)**: Manages the target lifecycle, including
  initialization, firmware installation, health checks, and recovery/rebooting
  when a test crashes or panics.
* **ComChannel (Communication Channel)**: Handles the underlying transport
  mechanism used to execute commands, stream stdout/stderr, and transfer
  files (e.g., SSH, QEMU serial, Shell, LTX).

To inspect all available SUT and communication channel plugins:

.. code-block:: bash

    kirk --sut help
    kirk --com help

Custom plugins are discovered by passing the folder containing your Python
source files to the ``--plugins`` option:

.. code-block:: bash

    kirk --plugins /path/to/my_plugins ...

Kirk will automatically scan all ``.py`` files in the specified directory and
register any subclasses of ``SUT`` and ``ComChannel``.

Developing a Custom SUT
-----------------------

A custom SUT must inherit from ``libkirk.sut.SUT`` and implement the following
methods and properties:

* ``_name``: Unique string identifier for the SUT, used with ``--sut <name>``.
* ``setup(**kwargs)``: Called after communication channels are initialized.
  Use ``libkirk.com.get_channels()`` to retrieve the channels needed for your
  setup.
* ``config_help``: Property returning a dictionary of parameter names and their
  descriptions for ``kirk --sut help``.
* ``get_channel()``: Returns the primary ``ComChannel`` used by kirk to run
  tests on the target.
* ``start(iobuffer)``: Asynchronous method to start, boot, or provision the
  target before running tests.
* ``stop(iobuffer)``: Asynchronous method to cleanly stop or shut down the
  target.
* ``restart(iobuffer)``: Asynchronous method to reboot or recover the target
  if it panics, times out, or stops responding.
* ``is_running()``: Asynchronous method returning ``True`` if the target is
  operational and reachable.

Developing a Custom ComChannel
------------------------------

A custom communication channel must inherit from ``libkirk.com.ComChannel`` and
implement the following methods and properties:

* ``_name``: Unique string identifier used with ``--com <name>``.
* ``setup(**kwargs)``: Parse configuration parameters passed via ``--com``.
* ``config_help``: Property returning a dictionary of parameter names and
  descriptions for ``kirk --com help``.
* ``active()``: Asynchronous method returning ``True`` if the channel is
  open and active.
* ``communicate(iobuffer)``: Asynchronous method to establish communication.
* ``stop(iobuffer)``: Asynchronous method to close the connection.
* ``run_command(command, cwd, env, iobuffer)``: Asynchronous method to execute
  a command on the target and return a dictionary with ``returncode``,
  ``stdout``, and ``exec_time``.
* ``fetch_file(target_path)``: Asynchronous method to retrieve file contents
  from the target as ``bytes``.
* ``ping()``: Asynchronous method returning response latency in seconds.
* ``parallel_execution``: Property returning ``True`` if the channel supports
  concurrent command execution.

Practical Example: Embedded Target SUT
--------------------------------------

Suppose you want to test LTP on an embedded board connected to your workstation.
The setup requires:

1. Flashing a new firmware with ``install_firmware.sh`` using local shell.
2. Executing LTP tests over SSH.
3. Power-cycling the board with ``reboot_board.sh`` via local shell if the
   kernel panics or becomes unresponsive.

Create a Python file (e.g., ``embedded_sut.py``) inside a plugins directory:

.. code-block:: python

    import os
    from typing import Any, Dict, Optional

    import libkirk.com
    from libkirk.com import ComChannel, IOBuffer
    from libkirk.errors import SUTError
    from libkirk.sut import SUT


    class EmbeddedSUT(SUT):
        _name = "embedded"

        def __init__(self) -> None:
            self._ssh: Optional[ComChannel] = None
            self._shell: Optional[ComChannel] = None

            currdir = os.path.dirname(os.path.realpath(__file__))
            self._install_sh = os.path.join(currdir, "install_firmware.sh")
            self._reboot_sh = os.path.join(currdir, "reboot_board.sh")

        def setup(self, **kwargs: Dict[str, Any]) -> None:
            chan_name = kwargs.get("com", "ssh")

            self._ssh = next(
                (c for c in libkirk.com.get_channels() if c.name == chan_name),
                None,
            )
            self._shell = next(
                (c for c in libkirk.com.get_channels() if c.name == "shell"),
                None,
            )

            if not self._ssh:
                raise SUTError(f"Cannot find channel '{chan_name}'")

        @property
        def config_help(self) -> Dict[str, str]:
            return {
                "com": "Communication channel to use (default: ssh)",
            }

        def get_channel(self) -> ComChannel:
            return self._ssh

        async def start(self, iobuffer: Optional[IOBuffer] = None) -> None:
            if await self.is_running():
                return

            await self._shell.ensure_communicate(iobuffer=iobuffer)
            ret = await self._shell.run_command(
                self._install_sh, iobuffer=iobuffer
            )
            if ret["returncode"] != 0:
                raise SUTError(f"{self._install_sh} failed")

            await self._ssh.ensure_communicate(iobuffer=iobuffer)

        async def stop(self, iobuffer: Optional[IOBuffer] = None) -> None:
            if not await self.is_running():
                return

            await self._ssh.stop(iobuffer=iobuffer)

        async def restart(self, iobuffer: Optional[IOBuffer] = None) -> None:
            await self.stop(iobuffer=iobuffer)

            ret = await self._shell.run_command(
                self._reboot_sh, iobuffer=iobuffer
            )
            if ret["returncode"] != 0:
                raise SUTError(f"{self._reboot_sh} failed")

            await self._shell.stop(iobuffer=iobuffer)
            await self.start(iobuffer=iobuffer)

        async def is_running(self) -> bool:
            return await self._ssh.active() if self._ssh else False

Running with Custom Plugins
---------------------------

Execute kirk with your custom plugin folder, specifying the custom SUT and the
required communication parameters:

.. code-block:: bash

    kirk --plugins /path/to/my_plugins \
         --sut embedded \
         --com ssh:host=192.168.0.1:user=root:key_file=/home/user/.ssh/id_rsa \
         --run-suite syscalls
