import os

GLOBAL_OPTIONS = {
    "test": False,
}


def set_option(option, value):
    GLOBAL_OPTIONS[option] = value


def get_option(option):
    return GLOBAL_OPTIONS[option]
