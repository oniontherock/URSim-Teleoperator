import time
import threading
import numpy as np
import math

class IKPoint:
    def __init__(self, position, orientation=None):
        self.position = np.asarray(position, dtype=float)
        self.orientation = None if orientation is None else np.asarray(orientation, dtype=float)


# returns the axis from point_a to point_b
def position_axis_get(pa, pb):
    return [pb[0] - pa[0], pb[1] - pa[1], pb[2] - pa[2]]

# get distance between two points
def position_distance_get(pa, pb):

    axis = position_axis_get(pa, pb)

    return math.sqrt((axis[0] * axis[0]) + (axis[1] * axis[1]) + (axis[2] * axis[2]))


