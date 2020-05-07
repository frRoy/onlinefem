# -*- coding: utf-8 -*-
r"""
.. module:: modeling.geometry.tests.test_geometry
   :platform: Unix, Windows
   :synopsis: Tests the geometry module.

.. moduleauthor:: Francois Roy <frns.roy@gmail.com>
"""
import pytest
from cadio import *
from cadio.geometry.geometry import Geometry


SAMPLE_DIR = APP_DIR / "geometry" / "tests" / "samples"


def test_two_instances():
    r"""Make sure we don't initialize/finalize gmsh when there is more
    than one geometry instance."""
    geom = [Geometry(), Geometry()]
    actual = []
    desired = [0, 0]
    for g in geom:
        actual.append(g.__del__())
    assert actual == desired


def test_geom_a():
    r""""""
    g = Geometry()
    #g.geom_a()
    # TODO: assertion below


def test_geom_b():
    r""""""
    g = Geometry()
    g.geom_b()
    g.generate_mesh()
    # TODO: assertion below


def test_geom_c():
    r""""""
    g = Geometry()
    # g.geom_c()
    # g.generate_mesh()
    # TODO: assertion below


def test_open_fail():
    r""""""
    m = r".* file.*"
    with pytest.raises(ValueError, match=m):
        Geometry(filename=str(SAMPLE_DIR / "fail_assembly3d.STEP"))


def test_step_assembly_3d():
    r""""""
    g = Geometry()
    # g.open(str(SAMPLE_DIR / "assembly3d.STEP"))
    # TODO: assertion below


def test_save():
    r""""""
    # TODO: assertion below
    pass
