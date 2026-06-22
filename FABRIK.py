# import time
# import threading
# import numpy
# import math

# # returns the axis from point_a to point_b
# def point_axis_get(point_a, point_b):
#     return (point_b - point_a)

# def point_distance_get(point_a, point_b):

#     axis = point_axis_get(point_a, point_b)

#     return math.sqrt((axis.x*axis.x) + (axis.y*axis.y) + (axis.z*axis.z))

# # this application of FABRIK uses 3D joint positions and rotational constraints. Intended for use in a Universal Robots robotic arm

# def forward_pass(joint_list, end_effector):
#     pass

# def backward_pass(joint_list, base):
#     pass

# # joint_list is the list of joints for FABRIK to be applied on. The base is the base position for the backwards pass. The end_effector is the target for the forward pass.
# def apply_FABRIK(joint_list, base, end_effector, distance_threshold):
#     while (point_distance_get(joint_list[-1], end_effector) > distance_threshold):
#         joint_list = backward_pass()forward_pass(joint_list, end_effector))

    


