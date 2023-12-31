#!/usr/bin/env python3

import logging

from functools import lru_cache, partial
from rich.console import Console
from rich.logging import RichHandler
from rich.markup import escape
from rich.traceback import install as install_rich_tracebacks


@lru_cache()
def get_logger(name: str = None) -> logging.Logger:
    parent_logger = logging.getLogger("shadow")

    if name:
        if not name.startswith(parent_logger.name + "."):
            logger = parent_logger.getChild(name)
        else:
            logger = logging.getLogger(name)
    else:
        logger = parent_logger

    add_logging_methods(logger)
    return logger


def setup_logging():
    logger = get_logger()
    logger.setLevel(shadow.settings.log_level)

    if not any(isinstance(h, RichHandler) for h in logger.handlers):
        handler = RichHandler(
            rich_tracebacks=True,
            markup=False,
            console=Console(width=shadow.settings.log_console_width),
        )
        formatter = logging.Formatter("%(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def add_logging_methods(logger):
    def log_style(level: int, message: str, style: str = None):
        if not style:
            style = "default on default"
        message = f"[{style}]{escape(str(message))}[/]"
        logger.log(level, message, extra={"markup": True})

    def log_kv(
        level: int,
        key: str,
        value: str,
        key_style: str = "default on default",
        value_style: str = "default on default",
        delimiter: str = ": ",
    ):
        logger.log(
            level,
            f"[{key_style}]{escape(str(key))}{delimiter}[/][{value_style}]{escape(str(value))}[/]",
            extra={"markup": True},
        )

    logger.debug_style = partial(log_style, logging.DEBUG)
    logger.info_style = partial(log_style, logging.INFO)
    logger.warning_style = partial(log_style, logging.WARNING)
    logger.error_style = partial(log_style, logging.ERROR)
    logger.critical_style = partial(log_style, logging.CRITICAL)

    logger.debug_kv = partial(log_kv, logging.DEBUG)
    logger.info_kv = partial(log_kv, logging.INFO)
    logger.warning_kv = partial(log_kv, logging.WARNING)
    logger.error_kv = partial(log_kv, logging.ERROR)
    logger.critical_kv = partial(log_kv, logging.CRITICAL)


setup_logging()
if shadow.settings.rich_tracebacks:
    install_rich_tracebacks()