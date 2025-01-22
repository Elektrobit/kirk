import os
from libkirk.sut import IOBuffer
# from typing import override (Not working for SDK [Python 3.10 < 3.12])
from libkirk.qemu import QemuSUT
from libkirk.sut import SUTError
from logging import getLogger

class EbclQemuSUT(QemuSUT):
    
    def __init__(self):
        super().__init__()
        self._logger = getLogger("kirk.ebclqemu")
        self._format = None
        self._kernel_append = None
        self._machine = None
        self._system = None
        self._cpu = None
    
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self._user = kwargs.get("user", "root")
        self._password = kwargs.get("password", "linux")
        self._ram = kwargs.get("ram", "4G")
        self._format = kwargs.get("format", "raw")
        self._kernel_append = kwargs.get("kernel_append", "")
        self._machine = kwargs.get("machine", "")
        self._system = kwargs.get("system", "")
        self._cpu = kwargs.get("cpu", "")
        
        if self._system == "aarch64":
            if not self._cpu or not self._machine:
                raise SUTError(
                    f"For aarch64 machine (\"{self._machine}\") and cpu (\"{self._cpu}\") parameters must be set!")
    
#   @override
#   Reason: Fit the QEMU commands better to our needs and enable arguments for kernel_append
    @property
    def config_help(self) -> dict:
        return {
            "image": "qemu image location",
            "kernel": "kernel image location",
            "kernel_append": "kernel append options",
            "initrd": "initrd image location",
            "user": "user name (default: 'root')",
            "password": "user password (default: 'linux')",
            "prompt": "prompt string (default: '#')",
            "system": "system architecture (default: x86_64)",
            "ram": "RAM of the VM (default: 4G)",
            "smp": "number of CPUs (default: 2)",
            "machine": "virt qemu machine to use",
            "cpu": "cpu arch to use",
            "serial": "type of serial protocol. isa|virtio (default: isa)",
            "virtfs": "directory to mount inside VM",
            "format": "Image format (default: 'raw')",
            "options": "user defined options",
        }
    
#   @override
#   Reason: Fit the QEMU commands better to our needs and enable arguments for kernel_append
    def _get_command(self) -> str:
        """
        Return the full qemu command to execute.
        """
        pid = os.getpid()
        tty_log = os.path.join(self._tmpdir, f"ttyS0-{pid}.log")

        params = []
        params.append("-display none")
        params.append(f"-m {self._ram}")
        params.append(f"-smp {self._smp}")
        params.append("-device virtio-rng-pci")
        params.append(f"-chardev stdio,id=tty,logfile={tty_log}")

        if self._serial_type == "isa":
            params.append("-serial chardev:tty")
            params.append("-serial chardev:transport")
        elif self._serial_type == "virtio":
            params.append("-device virtio-serial")
            params.append("-device virtconsole,chardev=tty")
            params.append("-device virtserialport,chardev=transport")
        else:
            raise NotImplementedError(
                f"Unsupported serial device type {self._serial_type}")

        _, transport_file = self._get_transport()
        params.append(f"-chardev file,id=transport,path={transport_file}")

        if self._virtfs:
            params.append(
                "-virtfs local,"
                f"path={self._virtfs},"
                "mount_tag=host0,"
                "security_model=mapped-xattr,"
                "readonly=on")

        if  self._system == "aarch64" and self._cpu and self._machine:
            params.append(f"-machine {self._machine} -cpu {self._cpu}")
            
        if self._image:
            params.append(f"-drive if=virtio,cache=unsafe,file={self._image},format={self._format}")

        if self._initrd:
            params.append(f"-initrd {self._initrd}")

        if self._kernel:
            console = "ttyS0"
            if self._serial_type == "virtio":
                console = "hvc0"

            params.append(f"-append 'console={console} ignore_loglevel {self._kernel_append}'")
            params.append(f"-kernel {self._kernel}")

        if self._opts:
            params.append(self._opts)

        cmd = f"{self._qemu_cmd} {' '.join(params)}"

        return cmd

#   @override
#   Reason: Avoid duplicate Naming
    @property
    def name(self) -> str:
        return "ebclqemu"

#   @override 
#   Reason: SDK Setup inserts copy/paste support ANSI characters, remove them from super's return set
    async def _exec(self, command: str, iobuffer: IOBuffer) -> set:
        """
        Execute a command and return set(stdout, retcode, exec_time) without ANSI escape sequences.
        """ 
        stdout, retcode, exec_time = await super()._exec(command, iobuffer)
        # Strip ANSI escape sequences from the stdout
        if stdout is not None:
            stdout = stdout.replace("\n\x1b[?2004h\x1b[?2004l\r", "")

        return stdout, retcode, exec_time
