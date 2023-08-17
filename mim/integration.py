import os
from typing import List

# docker mounts from each host system to the container

MOUNT_BASE = "/mim"

MACOS_MOUNTS = [
    f"/Users:{MOUNT_BASE}/Users",
    f"/Volumes:{MOUNT_BASE}/Volumes",
]

LINUX_MOUNTS = [
    f"/home:{MOUNT_BASE}/home",
]

WINDOWS_MOUNTS = [
    f"C:\\Users:{MOUNT_BASE}\\Users",
]


def get_os_integration_mounts() -> List[str]:
    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            return MACOS_MOUNTS
        elif os.uname().sysname == "Linux":
            return LINUX_MOUNTS
        else:
            raise NotImplementedError(f"unknown posix system: {os.uname().sysname}")
    elif os.name == "nt":
        return WINDOWS_MOUNTS
    else:
        raise NotImplementedError(f"unknown os: {os.name}")
