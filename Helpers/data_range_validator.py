import data_loader
import point_distance_checker


def bumpy(name_1,name_2):

    data_1 = data_loader.data_load_as_dict(name_1, -1)
    data_2 = data_loader.data_load_as_dict(name_2, -1)

    all_dists = []

    for timestamp in data_1:

        if not timestamp in data_2:
            continue

        def get_from_data(ts1, ts2):
            return point_distance_checker.dist_get(
                data_1[ts1][0][0],
                data_1[ts1][0][1],
                data_1[ts1][0][2],
                data_2[ts2][0][0],
                data_2[ts2][0][1],
                data_2[ts2][0][2]
                )

        if (timestamp-1) in data_2:
            all_dists.append(get_from_data(timestamp, timestamp-1))
        if (timestamp+1) in data_2:
            all_dists.append(get_from_data(timestamp, timestamp+1))
        if (timestamp) in data_2:
            all_dists.append(get_from_data(timestamp, timestamp))
        

    print(
        f"Data count = {len(all_dists)}\n",
        f"Max dist = {max(all_dists)}\n",
        f"Min dist = {min(all_dists)}\n"
        )
    return(
        len(all_dists),
        max(all_dists),
        min(all_dists)
          )

data_len_full = 0
dist_max_full = -99999999
dist_min_full = 999999999

for i in range(1, 13):
    data_len, dist_max, dist_min, = bumpy(f"tcp_sampler_{i}", f"robot_tcp_position_{i}")
    data_len_full += data_len

    if (dist_max > dist_max_full):
        dist_max_full = dist_max
    if (dist_min < dist_min_full):
        dist_min_full = dist_min
        
print(
    f"Final data count = {data_len_full}\n",
    f"final max dist = {dist_max_full}\n",
    f"Final min dist = {dist_min_full}\n"
    )