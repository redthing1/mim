import os
import time
from typing import List, Optional, Any, Dict

import typer
import sh
from minlog import logger, Verbosity

from .util import set_option, get_option
from . import __VERSION__

from .containers import (
    PODMAN,
    FORMAT_PODMAN_OUTPUT,
    get_containers,
    container_exists,
    container_is_running,
    container_is_mim,
)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

APP_NAME = "mim"
app = typer.Typer(
    name=APP_NAME,
    help=f"{APP_NAME}: integrated mini machines",
    no_args_is_help=True,
    context_settings=CONTEXT_SETTINGS,
    pretty_exceptions_show_locals=False,
)


def version_callback(value: bool):
    if value:
        logger.error(f"{APP_NAME} v{__VERSION__}")
        raise typer.Exit()


@app.callback()
def app_callback(
    verbose: List[bool] = typer.Option([], "--verbose", "-v", help="Verbose output"),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Quiet output"),
    version: Optional[bool] = typer.Option(
        None, "--version", "-V", callback=version_callback
    ),
):
    if len(verbose) == 1:
        logger.be_verbose()
    elif len(verbose) == 2:
        logger.be_debug()
    elif quiet:
        logger.be_quiet()


@app.command(help="build an image from a dockerfile", no_args_is_help=True)
def build(
    dockerfile: str = typer.Option(
        ...,
        "-f",
        "--dockerfile",
        help="path to the dockerfile to build an image from.",
    ),
    image_name: str = typer.Option(
        ...,
        "-n",
        "--image-name",
        help="name of the image to build.",
    ),
    context_dir: str = typer.Option(
        ".",
        "-C",
        "--context-dir",
        help="path to context directory for the docker build.",
    ),
):
    logger.info(f"building docker image from [{dockerfile}]")
    build_cmd = PODMAN.bake(
        "build",
        "-f",
        dockerfile,
        "-t",
        image_name,
        context_dir,
        **FORMAT_PODMAN_OUTPUT,
    )
    logger.debug(f"running command: {build_cmd}")
    try:
        build_proc = build_cmd()
    except sh.ErrorReturnCode as e:
        logger.error(f"build failed with error code {e.exit_code}")
        raise typer.Exit(1)

    logger.info(f"build complete, image [{image_name}] created")


@app.command(help="create a container from an image", no_args_is_help=True)
def create(
    image_name: str = typer.Option(
        ...,
        "-n",
        "--image-name",
        help="name of the image to run.",
    ),
    container_name: str = typer.Option(
        None,
        "-c",
        "--container-name",
        help="name to give the container.",
    ),
):
    if container_name is None:
        container_name = image_name

    if container_exists(container_name):
        logger.error(f"container [{container_name}] already exists")
        raise typer.Exit(1)

    logger.info(f"creating mim container [{container_name}] from image [{image_name}]")
    create_cmd = PODMAN.bake(
        "create",
        "--name",
        container_name,
        "--label",
        f"mim=1",
        image_name,
    )

    logger.debug(f"running command: {create_cmd}")
    try:
        create_cmd(**FORMAT_PODMAN_OUTPUT)
        logger.info(f"container [{container_name}] created")
    except sh.ErrorReturnCode as e:
        logger.error(f"run failed with error code {e.exit_code}")
        raise typer.Exit(1)


@app.command(help="destroy a container", no_args_is_help=True)
def destroy(
    container_name: str = typer.Option(
        ...,
        "-c",
        "--container-name",
        help="name of the container to destroy.",
    ),
):
    if not container_exists(container_name):
        logger.error(f"container [{container_name}] does not exist")
        raise typer.Exit(1)

    if not container_is_mim(container_name):
        logger.error(f"container [{container_name}] is not a mim container")
        raise typer.Exit(1)

    logger.info(f"destroying mim container [{container_name}]")
    destroy_cmd = PODMAN.bake(
        "rm",
        container_name,
    )

    logger.debug(f"running command: {destroy_cmd}")
    try:
        destroy_proc = destroy_cmd()
    except sh.ErrorReturnCode as e:
        logger.error(f"destroy failed with error code {e.exit_code}")
        raise typer.Exit(1)

    logger.info(f"container [{container_name}] destroyed")


@app.command(help="get a shell in a running container", no_args_is_help=True)
def shell(
    container_name: str = typer.Option(
        ...,
        "-c",
        "--container-name",
        help="name of the container to get a shell in.",
    ),
    shell: str = typer.Option(
        "/bin/zsh",
        "-s",
        "--shell",
        help="shell to run in the container.",
    ),
):
    if not container_exists(container_name):
        logger.error(f"container [{container_name}] does not exist")
        raise typer.Exit(1)

    if not container_is_mim(container_name):
        logger.error(f"container [{container_name}] is not a mim container")
        raise typer.Exit(1)

    if not container_is_running(container_name):
        logger.info(f"container [{container_name}] is not running, starting it")
        start_cmd = PODMAN.bake(
            "start",
            container_name,
        )

        logger.debug(f"running command: {start_cmd}")
        try:
            start_proc = start_cmd()
        except sh.ErrorReturnCode as e:
            logger.error(f"start failed with error code {e.exit_code}")
            raise typer.Exit(1)

    if not container_is_running(container_name):
        logger.error(f"container [{container_name}] could not be started")
        raise typer.Exit(1)

    logger.info(f"getting shell in container [{container_name}]")
    shell_cmd = PODMAN.bake(
        "exec",
        "-it",
        container_name,
        shell,
    )

    logger.debug(f"running command: {shell_cmd}")
    try:
        shell_proc = shell_cmd(_fg=True)
    except sh.ErrorReturnCode as e:
        logger.error(f"shell failed with error code {e.exit_code}")
        raise typer.Exit(1)