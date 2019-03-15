import numpy as np
import math

def vector_norm(data, axis=None, out=None):
    """Return length, i.e. Euclidean norm, of ndarray along axis."""


    data = np.array(data, dtype=np.float64, copy=True)
    if out is None:
        if data.ndim == 1:
            return math.sqrt(np.dot(data, data))
        data *= data
        out = np.atleast_1d(np.sum(data, axis=axis))
        np.sqrt(out, out)
        return out
    else:
        data *= data
        np.sum(data, axis=axis, out=out)
        np.sqrt(out, out)


def decompose_matrix(matrix):
    """Return sequence of transformations from transformation matrix.

    matrix : array_like
        Non-degenerative homogeneous transformation matrix

    Return tuple of:
        scale : vector of 3 scaling factors
        shear : list of shear factors for x-y, x-z, y-z axes
        angles : list of Euler angles about static x, y, z axes
        translate : translation vector along x, y, z axes
        perspective : perspective partition of matrix

    Raise ValueError if matrix is of wrong type or degenerative."""

    eps = np.finfo(float).eps

    M = np.array(matrix, dtype=np.float64, copy=True).T
    row = np.array([0, 0, 0])
    column = np.array([[0], [0], [0], [1]])
    M = np.vstack((M, row))
    M = np.hstack((M, column))
    if abs(M[3, 3]) < eps:
        raise ValueError('M[3, 3] is zero')
    M /= M[3, 3]
    P = M.copy()
    P[:, 3] = 0.0, 0.0, 0.0, 1.0
    if not np.linalg.det(P):
        raise ValueError('matrix is singular')

    scale = np.zeros((3,))
    shear = [0.0, 0.0, 0.0]
    angles = [0.0, 0.0, 0.0]

    if any(abs(M[:3, 3]) > eps):
        perspective = np.dot(M[:, 3], np.linalg.inv(P.T))
        M[:, 3] = 0.0, 0.0, 0.0, 1.0
    else:
        perspective = np.array([0.0, 0.0, 0.0, 1.0])

    translate = M[3, :3].copy()
    M[3, :3] = 0.0

    row = M[:3, :3].copy()
    scale[0] = vector_norm(row[0])
    row[0] /= scale[0]
    shear[0] = np.dot(row[0], row[1])
    row[1] -= row[0] * shear[0]
    scale[1] = vector_norm(row[1])
    row[1] /= scale[1]
    shear[0] /= scale[1]
    shear[1] = np.dot(row[0], row[2])
    row[2] -= row[0] * shear[1]
    shear[2] = np.dot(row[1], row[2])
    row[2] -= row[1] * shear[2]
    scale[2] = vector_norm(row[2])
    row[2] /= scale[2]
    shear[1:] /= scale[2]

    if np.dot(row[0], np.cross(row[1], row[2])) < 0:
        np.negative(scale, scale)
        np.negative(row, row)

    angles[1] = math.asin(-row[0, 2])
    if math.cos(angles[1]):
        angles[0] = np.degrees(math.atan2(row[1, 2], row[2, 2]))
        angles[2] = np.degrees(math.atan2(row[0, 1], row[0, 0]))
    else:
        # angles[0] = math.atan2(row[1, 0], row[1, 1])
        angles[0] = np.degrees(math.atan2(-row[2, 1], row[1, 1]))
        angles[2] = 0.0

    angles[1] = np.degrees(angles[1])

    return scale, shear, angles, translate, perspective