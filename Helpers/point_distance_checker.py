

def dist_get(x1,y1,z1,x2,y2,z2):

    axis_x = x2-x1
    axis_y = y2-y1
    axis_z = z2-z1

    dist = (axis_x**2 + axis_y**2 + axis_z**2)**0.5
    
    return dist

def dist_get_pos(pos1,pos2):
    return dist_get(pos1[0],pos1[1],pos1[2],pos2[0],pos2[1],pos2[2])