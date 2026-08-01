import numpy as np
from numpy.typing import NDArray

dtype = [('x', 'f8'), ('y', 'f8'), ('z', 'f8'), ('ts_grab', 'i8'), ('ts_infer', 'i8'), ('ts_publish', 'i8')]


data_list: dict[int, tuple[float, float, float, int, int]] = {}

def data_point_add(x, y, z, ts_grab):
    data_list[ts_grab] = (-z, x, -y, 0, 0)
def data_point_infer_time_set(ts_grab, ts_infer):
    data_list[ts_grab] = (
        data_list[ts_grab][0],
        data_list[ts_grab][1],
        data_list[ts_grab][2],
        ts_infer, 
        data_list[ts_grab][4]
    )
def data_point_publish_time_set(ts_grab, ts_publish):
    data_list[ts_grab] = (
        data_list[ts_grab][0],
        data_list[ts_grab][1],
        data_list[ts_grab][2],
        data_list[ts_grab][3],
        ts_publish
    )

def data_save():
    formatted_data = [(v[0], v[1], v[2], ts_grab, v[3], v[4]) for ts_grab, v in data_list.items()]
    
    final_array: NDArray[np.void] = np.array(formatted_data, dtype=dtype)
    
    np.savetxt(
        "data.txt", 
        final_array, 
        fmt=['%.16f', '%.16f', '%.16f', '%d', '%d', '%d'], 
        delimiter=', ', 
        header='x, y, z, ts_grab, ts_infer, ts_publish', 
        comments=''
    )