# -*- coding: utf-8 -*-
"""Python interface to CAD.

:Author: **Francois Roy**
:Date: |today|

.. moduleauthor:: Francois Roy <frns.roy@gmail.com>
"""
import os
import logging
from pathlib import Path
import numpy as np
from pint import UnitRegistry
from mpi4py import MPI

from .node import Node


PROJECT_DIR = Path(os.path.abspath(__file__)).parents[1]
APP_DIR = PROJECT_DIR / "cadio"
DATA_DIR = APP_DIR / "data"
TEMP_DIR = APP_DIR / ".cadio"
GMSH_PATH = Path("/opt/gmsh/bin/gmsh")

ureg = UnitRegistry()
Q_ = ureg.Quantity

LOGGING_FORMAT = '[%(levelname)s] %(asctime)s - ' \
                 '%(module)s:%(lineno)d --> %(message)s'
# %(pathname)s%(filename)s
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

__app__ = "cadio"
__version__ = "0.1.0"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)
