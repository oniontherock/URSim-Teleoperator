import math

FIXED_ORIENT = [0.0, 3.14159, 0.0]  # tool pointing down (axis-angle, rad) — verify for your tool

# this comes in after filter
def wrist_map_to_robot(d):
    rx = d[0]*1.2
    ry = d[1]*1.2
    rz = d[2]*1.2

    min_dist = 0.1
    max_dist = 0.8

    dist_from_base = math.sqrt((rx*rx)+(ry*ry)+(rz*rz))
    if (dist_from_base >max_dist):
        rx = (rx / dist_from_base) * max_dist
        ry = (ry / dist_from_base) * max_dist
        rz = (rz / dist_from_base) * max_dist
    elif (dist_from_base < min_dist):
        rx = (rx / dist_from_base) * min_dist
        ry = (ry / dist_from_base) * min_dist
        rz = (rz / dist_from_base) * min_dist

    return [-rz, rx, -ry, *FIXED_ORIENT]