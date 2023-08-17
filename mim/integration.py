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

CONTAINER_INTEGRATION_MOUNTS = [
    # "$/.zsh_history:/root/.zsh_history",
    # "$/.bash_history:/root/.bash_history",
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


def get_os_integration_home_env() -> str:
    home_dir = get_home_dir()
    current_user = get_current_user()
    container_home_dir = None

    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            container_home_dir = f"{MOUNT_BASE}/Users/{current_user}"
        elif os.uname().sysname == "Linux":
            container_home_dir = f"{MOUNT_BASE}/home/{current_user}"
        else:
            raise NotImplementedError(f"unknown posix system: {os.uname().sysname}")
    elif os.name == "nt":
        container_home_dir = f"{MOUNT_BASE}/Users/{current_user}"
    else:
        raise NotImplementedError(f"unknown os: {os.name}")

    home_env = f"HOME={container_home_dir}"
    return home_env


def get_container_integration_mounts(data_dir) -> List[str]:
    return [x.replace("$", data_dir) for x in CONTAINER_INTEGRATION_MOUNTS]


# get a path to storable data for this app
def get_app_data_dir(app_name: str) -> str:
    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            return os.path.join(
                os.environ["HOME"], f"Library/Application Support/{app_name}"
            )
        elif os.uname().sysname == "Linux":
            return os.path.join(os.environ["HOME"], f".local/share/{app_name}")
        else:
            raise NotImplementedError(f"unknown posix system: {os.uname().sysname}")
    elif os.name == "nt":
        return os.path.join(os.environ["APPDATA"], app_name)
    else:
        raise NotImplementedError(f"unknown os: {os.name}")


def get_home_dir() -> str:
    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            return os.environ["HOME"]
        elif os.uname().sysname == "Linux":
            return os.environ["HOME"]
        else:
            raise NotImplementedError(f"unknown posix system: {os.uname().sysname}")
    elif os.name == "nt":
        return os.environ["USERPROFILE"]
    else:
        raise NotImplementedError(f"unknown os: {os.name}")


def get_current_user() -> str:
    if os.name == "posix":
        if os.uname().sysname == "Darwin":
            return os.environ["USER"]
        elif os.uname().sysname == "Linux":
            return os.environ["USER"]
        else:
            raise NotImplementedError(f"unknown posix system: {os.uname().sysname}")
    elif os.name == "nt":
        return os.environ["USERNAME"]
    else:
        raise NotImplementedError(f"unknown os: {os.name}")
