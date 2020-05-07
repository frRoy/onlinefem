
import dolfinx
import ufl
from mpi4py import MPI
import numpy as np
from dolfinx import (RectangleMesh)
from dolfinx.cpp.mesh import CellType

import requests as req
import logging



from flask import Flask, jsonify, request
app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    r"""Use simple flas application to serve dolfinX."""
    v = [np.array([0, 0, 0]), np.array([1, 1, 0])]

    mesh = RectangleMesh(
        MPI.COMM_WORLD,
        [np.array([0, 0, 0]), np.array([1, 1, 0])], [32, 32],
        CellType.triangle, dolfinx.cpp.mesh.GhostMode.none)


    d = {"numbers": list(range(10)), 'method': request.method}
    if request.method == 'POST':
        data = request.form
        name = data['name']
        d = None
        if name == "numbers":
            d = {"numbers": list(range(10)), 'method': request.method}
    return jsonify(d)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555)