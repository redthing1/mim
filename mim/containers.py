import sh
import json

PODMAN = sh.Command("podman")

FORMAT_PODMAN_OUTPUT = {
    "_out": lambda line: print(f"  {line}", end=""),
    "_err": lambda line: print(f"  {line}", end=""),
}


def get_containers(only_mim=False):
    ps_args = ["-a", "--format", "json"]
    if only_mim:
        ps_args.append("--filter")
        ps_args.append("label=mim=1")
    ps_cmd = PODMAN.bake("ps", *ps_args)
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


def get_images():
    images_cmd = PODMAN.bake("images", "--format", "json")
    podman_images_json = images_cmd()
    podman_images = json.loads(podman_images_json)
    return podman_images


def image_exists(image_name):
    image_exists_cmd = PODMAN.bake("image", "exists", image_name)
    try:
        image_exists_cmd()
        return True
    except sh.ErrorReturnCode:
        return False
