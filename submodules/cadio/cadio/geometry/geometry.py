# -*- coding: utf-8 -*-
r"""
.. module:: modeling.geometry.geometry
   :platform: Unix, Windows
   :synopsis: Generate or import a geometry using Gmsh.

.. moduleauthor:: Francois Roy <frns.roy@gmail.com>
"""
import gmsh

from modeling import *


class Geometry(Node, gmsh.model):
    r"""Generate or import a geometry using `Gmsh <https://gmsh.info/>`_.

    The available predefined geometries are:

      * :func:`geom_a`: A two-rectangles assembly (2D).
      * :func:`geom_b`: 3D

    Usage:

    .. code-block:: python

        >>> from modeling.geometry.geometry import Geometry
        >>> g = Geometry()
        >>> g.geom_a()  # generate predefined geometry A
        >>> g.save()  # saves the geometry in temp directory

    :param tag: The name of the Gmsh model -- default = "geometry".
    :type tag: str
    :param filename: The path to a CAD file to be imported -- optional.
    :type filename: Path
    """
    _counter = 0

    def __init__(self, tag='geometry', parent=None, filename=None):
        try:
            gmsh.initialize()  # initialize gmsh
            logging.debug("gmsh initialized")
        except Exception as e:
            logging.warning(e)
        finally:
            Geometry._counter += 1
        super().__init__(tag, parent)
        logging.debug(f"create geometry instance {Geometry._counter}")
        # gmsh.option.setNumber("General.Terminal", 1)
        gmsh.option.setNumber("Mesh.SaveElementTagType", 2)
        # gmsh.option.setNumber("Mesh.SaveAll", 1)
        if filename is not None:
            self.open(filename)
        self.add(tag)
        self._tag = tag
        # logging.info(f"\n{self.gmsh_code}")

    def __del__(self):
        r"""Make sure to exit gmsh when the geometry is deleted."""
        logging.debug(f"delete geometry instance {Geometry._counter}")
        e_code = -1
        try:
            if Geometry._counter == 1:  # all other instances deleted
                gmsh.finalize()
                logging.debug("gmsh finalized")
            e_code = 0
        except ValueError:
            raise  # only message, exceptions are ignored in __del__
        finally:
            Geometry._counter -= 1
            return e_code

    @property
    def dim(self):
        r"""The spatial dimension of the geometry.

        :return: int -- The dimension.
        """
        return self.getDimension()

    def display(self):
        r"""Renders the geometry. See
        `ex <https://kitware.github.io/vtk-js/examples/PolyDataReader.html>`_
        """
        pass

    def generate_mesh(self, dim=3):
        r"""Generate a mesh of the current model, up to dimension
        ``dim`` (0, 1, 2 or 3), and save to the temp directory.

        :param dim: The maximum dimension.
        :type dim: int
        """
        self.mesh.generate(dim)
        gmsh.write(str(TEMP_DIR / f"{self._tag}.msh"))

    def geom_a(self, lc=0.1, eps=1e-6):
        r"""Generates a two-rectangles assembly from a unit square.
        The assembly consists of a bottom rectangle of length 1, and height
        0.5 with corner positioned at 0, 0, and a top rectangle of same
        dimensions but positioned at 0, 0.5 + eps. There is no imprints
        (identical mesh between the top of the lower rectangle and the
        bottom of the upper rectangle).

        .. figure:: ../images/geom_a.png
          :name: geom_a
          :width: 600px
          :align: center
          :alt: Geometry A
          :figclass: align-center

          : Geometry A.

        :param lc: The characteristic length for meshing, default 0.1.
        :param eps: The separation between the two assemblies, default 1e-6.
        """
        # create geometry from bottom-up
        p0 = self.geo.addPoint(0, 0, 0, lc / 4)
        p1 = self.geo.addPoint(1., 0, 0, lc)
        p2 = self.geo.addPoint(1., 0.5, 0, lc)
        p3 = self.geo.addPoint(0, 0.5, 0, lc / 4)
        p4 = self.geo.addPoint(0, 0.5 + eps, 0, lc)
        p5 = self.geo.addPoint(1., 0.5 + eps, 0, lc)
        p6 = self.geo.addPoint(1., 1.0 + eps, 0, lc)
        p7 = self.geo.addPoint(0, 1.0 + eps, 0, lc)
        points = [p0, p1, p2, p3, p4, p5, p6, p7]
        # lines
        l0 = self.geo.addLine(p0, p1)  # bottom lower
        l1 = self.geo.addLine(p1, p2)  # right lower
        l2 = self.geo.addLine(p2, p3)  # top lower
        l3 = self.geo.addLine(p3, p0)  # left lower
        l4 = self.geo.addLine(p4, p5)  # bottom upper
        l5 = self.geo.addLine(p5, p6)  # right upper
        l6 = self.geo.addLine(p6, p7)  # top upper
        l7 = self.geo.addLine(p7, p4)  # left upper
        # create surface  a = lower rectangle, b = upper rectangle
        cla = self.geo.addCurveLoop([l0, l1, l2, l3])
        clb = self.geo.addCurveLoop([l4, l5, l6, l7])
        psa = self.geo.addPlaneSurface([cla])
        psb = self.geo.addPlaneSurface([clb])
        # tag lines
        pla_l = self.addPhysicalGroup(1, [l0])  # bottom lower
        pla_p = self.addPhysicalGroup(1, [l1, l3])  # periodic_bottom
        plb_l = self.addPhysicalGroup(1, [l2])  # top bnd lower rectangle
        pla_u = self.addPhysicalGroup(1, [l4])  # bottom bnd upper rectangle
        plb_p = self.addPhysicalGroup(1, [l5, l7])  # periodic_top
        plb_u = self.addPhysicalGroup(1, [l6])  # top upper
        gmsh.model.setPhysicalName(1, pla_l, "bottom_lower")
        gmsh.model.setPhysicalName(1, pla_p, "bottom_periodic")
        gmsh.model.setPhysicalName(1, plb_l, "top_lower")
        gmsh.model.setPhysicalName(1, pla_u, "bottom_upper")
        gmsh.model.setPhysicalName(1, plb_p, "top_periodic")
        gmsh.model.setPhysicalName(1, plb_u, "top_upper")
        # tag surfaces
        psa = self.addPhysicalGroup(2, [psa])  # lower
        psb = self.addPhysicalGroup(2, [psb])  # upper
        gmsh.model.setPhysicalName(2, psa, "lower")
        gmsh.model.setPhysicalName(2, psb, "upper")
        # periodic condition
        self.geo.synchronize()
        # left to right
        translation = [1, 0, 0, 1.,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        gmsh.model.mesh.setPeriodic(1, [l1], [l3], translation)
        gmsh.model.mesh.setPeriodic(1, [l5], [l7], translation)
        gmsh.write(str(TEMP_DIR / f"{self._tag}.geo_unrolled"))

    def geom_b(self, lc=0.1, eps=1e-6):
        r"""Same as geometry a :func:`geom_a` but with a matching
        boundary between the top of the lower rectangle and the
        bottom of the upper rectangle.

        :param lc: The characteristic length for meshing, default 0.1.
        :param eps: The separation between the two assemblies, default 1e-6.
        """
        # create geometry from bottom-up
        p0 = self.geo.addPoint(0, 0, 0, lc / 4)
        p1 = self.geo.addPoint(1.0, 0, 0, lc/4)
        p2 = self.geo.addPoint(1.0, 0.5, 0, lc/4)
        p3 = self.geo.addPoint(0, 0.5, 0, lc / 4)
        p4 = self.geo.addPoint(0, 0.5 + eps, 0, lc)
        p5 = self.geo.addPoint(1.0, 0.5 + eps, 0, lc)
        p6 = self.geo.addPoint(1.0, 1.0 + eps, 0, lc)
        p7 = self.geo.addPoint(0, 1.0 + eps, 0, lc)
        # lines
        l0 = self.geo.addLine(p0, p1)  # bottom lower
        l1 = self.geo.addLine(p1, p2)  # right lower
        l2 = self.geo.addLine(p2, p3)  # top lower
        l3 = self.geo.addLine(p3, p0)  # left lower
        l4 = self.geo.addLine(p4, p5)  # bottom upper
        l5 = self.geo.addLine(p5, p6)  # right upper
        l6 = self.geo.addLine(p6, p7)  # top upper
        l7 = self.geo.addLine(p7, p4)  # left upper
        # create surface  a = lower, b = upper
        cla = self.geo.addCurveLoop([l0, l1, l2, l3])
        clb = self.geo.addCurveLoop([l4, l5, l6, l7])
        psa = self.geo.addPlaneSurface([cla])
        psb = self.geo.addPlaneSurface([clb])
        # Tag line
        pla_l = self.addPhysicalGroup(1, [l0])  # bottom lower
        pla_p = self.addPhysicalGroup(1, [l1, l3])  # periodic_bottom
        pl_pair = self.addPhysicalGroup(1, [l2, l4])  # pair
        plb_p = self.addPhysicalGroup(1, [l5, l7])  # periodic_top
        plb_u = self.addPhysicalGroup(1, [l6])  # top upper
        gmsh.model.setPhysicalName(1, pla_l, "bottom_lower")
        gmsh.model.setPhysicalName(1, pla_p, "bottom_periodic")
        gmsh.model.setPhysicalName(1, pl_pair, "pair")
        gmsh.model.setPhysicalName(1, plb_p, "top_periodic")
        gmsh.model.setPhysicalName(1, plb_u, "top_upper")
        # Tag surface
        psa = self.addPhysicalGroup(2, [psa])  # lower
        psb = self.addPhysicalGroup(2, [psb])  # upper
        gmsh.model.setPhysicalName(2, psa, "lower")
        gmsh.model.setPhysicalName(2, psb, "upper")
        # periodic condition
        self.geo.synchronize()
        # left to right
        translation = [1, 0, 0, 1,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        gmsh.model.mesh.setPeriodic(1, [l1], [l3], translation)
        gmsh.model.mesh.setPeriodic(1, [l5], [l7], translation)
        # bottom top
        translation = [1, 0, 0, 0,
                       0, 1, 0, eps,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        gmsh.model.mesh.setPeriodic(1, [l4], [l2], translation)
        gmsh.write(str(TEMP_DIR / f"{self._tag}.geo_unrolled"))

    def geom_c(self, lc=0.1, *args, **kwargs):
        r"""A simple rectangle with periodic mesh on left/right side

        :param lc: The characteristic length for meshing, default 0.1.
        :type lc: float
        """
        w = kwargs.pop("w", 1.0)
        h = kwargs.pop("h", 0.5)
        # create geometry from bottom-up
        p0 = self.geo.addPoint(0, 0, 0, lc / 4)
        p1 = self.geo.addPoint(w, 0, 0, lc)
        p2 = self.geo.addPoint(w, h, 0, lc)
        p3 = self.geo.addPoint(0, h, 0, lc / 4)
        # lines
        l0 = self.geo.addLine(p0, p1)  # bottom lower
        l1 = self.geo.addLine(p1, p2)  # right lower
        l2 = self.geo.addLine(p2, p3)  # top lower
        l3 = self.geo.addLine(p3, p0)  # left lower
        # create surface  a = lower, b = upper
        cla = self.geo.addCurveLoop([l0, l1, l2, l3])
        psa = self.geo.addPlaneSurface([cla])
        # Tag line
        pla_l = self.addPhysicalGroup(1, [l0])  # bottom lower
        pla_p = self.addPhysicalGroup(1, [l1, l3])  # periodic_bottom
        pla_u = self.addPhysicalGroup(1, [l2])  # top lower
        gmsh.model.setPhysicalName(1, pla_l, "bottom_lower")
        gmsh.model.setPhysicalName(1, pla_p, "periodic_lower")
        gmsh.model.setPhysicalName(1, pla_u, "top_lower")
        # Tag surface
        psa = self.addPhysicalGroup(2, [psa])  # lower
        gmsh.model.setPhysicalName(2, psa, "lower")
        # periodic condition
        self.geo.synchronize()
        # left to right
        translation = [1, 0, 0, w,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        gmsh.model.mesh.setPeriodic(1, [l1], [l3], translation)
        gmsh.write(str(TEMP_DIR / f"{self._tag}.geo_unrolled"))

    def open(self, filename):
        r"""Use :mod:`gmsh`

        :param filename:
        :type filename: str.
        :returns:  int -- the return code.
        :rtype: list of strings
        :raises: ValueError, KeyError
        """
        gmsh.clear()  # start fresh
        m = f"Can't open the file \"{Path(filename).name}\""
        try:
            gmsh.open(filename)
        except ValueError:
            logging.error(m)
        if self.getDimension() < 0:
            raise ValueError(m)
        gmsh.write(str(TEMP_DIR / f"{self._tag}.geo_unrolled"))

    def to_vtk(self):
        r"""Generates vtk file for display."""
        pass

    def save(self, file_format='geo_unrolled'):
        r"""Gmsh never translates geometry data into a common representation:
        all the operations on a geometrical entity are performed natively with
        the associated geometry kernel. Consequently, one cannot export a
        geometry constructed with the built-in kernel as an OpenCASCADE BRep
        file; or export an OpenCASCADE model as an Unrolled GEO file.

        :param file_format:
        :return:
        """
        try:
            gmsh.write(str(TEMP_DIR / f"{self._tag}.{file_format}"))
        except Exception as e:
            logging.error(e)
