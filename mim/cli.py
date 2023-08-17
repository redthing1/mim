import os
import time
from typing import List, Optional, Any, Dict

import typer
from minlog import logger, Verbosity


from .util import set_option, get_option
from . import __VERSION__

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
        print(f"{APP_NAME} v{__VERSION__}")
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

