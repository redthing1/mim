import sh
import json

PODMAN = sh.Command("podman")

FORMAT_PODMAN_OUTPUT = {
    "_out": lambda line: print(f"  {line}", end=""),
    "_err": lambda line: print(f"  {line}", end=""),
}


def get_containers():
    ps_cmd = PODMAN.bake("ps", "-a", "--format", "json")
    podman_containers_json = ps_cmd()
    podman_containers = json.loads(podman_containers_json)
    return podman_containers


def container_exists(container_name):
    podman_containers = get_containers()
    for container in podman_containers:
        if container_name in container["Names"]:
            return True
    return False


def container_is_running(container_name):
    podman_containers = get_containers()
    for container in podman_containers:
        if container_name in container["Names"]:
            if container["State"] == "running":
                return True
    return False


def container_is_mim(container_name):
    podman_containers = get_containers()
    for container in podman_containers:
        if container_name in container["Names"]:
            if container["Labels"]["mim"] == "1":
                return True
    return False
