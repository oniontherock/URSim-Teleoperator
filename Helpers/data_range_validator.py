import data_loader
import numpy as np
import bisect

def bumpy(name_1,name_2):

    data_1 = data_loader.data_load_as_dict(name_1, 1)
    data_2 = data_loader.data_load_as_dict(name_2, 1)

    bad_timestamps = 0

    sorted_data_2 = sorted(data_2.keys())

    for i in data_1:

        ind_i = bisect.bisect_left(sorted_data_2, i)

        closest_lower_i = sorted_data_2[ind_i-1] if ind_i >  0 else 0
        closest_higher_i = sorted_data_2[ind_i] if ind_i < len(sorted_data_2) else 0

        if closest_lower_i <= 0 or closest_higher_i <= 0:
            continue

        neighbors_like_me = 0

        if data_2[closest_lower_i] == data_1[i]:
            neighbors_like_me += 1
        if data_2[closest_higher_i] == data_1[i]:
            neighbors_like_me += 1

        if neighbors_like_me <= 0:
            bad_timestamps += 1

    print(f"Bad timestamps = {bad_timestamps}")

bumpy("sampler2__2026_09_07__10h05m25s", "sampler1__2026_09_07__10h05m25s")
