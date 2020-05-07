# -*- coding: utf-8 -*-
"""Command line interface to the CADIO application.

:Author: **Francois Roy**
:Date: |today|

.. moduleauthor:: Francois Roy <frns.roy@gmail.com>
"""
import sys
import click
import traceback

from cadio import __version__, __app__, logging
from cadio import *
from cadio.geometry import Geometry


def print_version(ctx, param, value):
    r"""Prints the version and exits the program in the callback.

    :param param:
    :param ctx: Click internal object that holds state
                              relevant for the script execution.
    :param value: Close the program without printing the version if False.
    :type ctx: click.context
    :type value: bool
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo('{} {} (Python {})'.format(
        __app__, __version__, sys.version[:3])
    )
    ctx.exit()


@click.command()
@click.option(
    '-v', '--version',
    is_flag=True, help='Show version information and exit.',
    callback=print_version, expose_value=False, is_eager=True,
)
def main():
    r"""CADIO: A general code for numerical analysis.
    """
    pass


if __name__ == '__main__':
    main()
