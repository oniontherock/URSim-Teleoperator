import data_loader

# filters out two data arrays so that only data with timestamps within a certain threshold are kept. threshold is time in milliseconds
def filter_for_timestamps(data_1, data_2, t_threshold, timestamp_index=-1):

    data_filtered_1 = []
    data_filtered_2 = []

    data_size_min = min(len(data_1), len(data_2))

    for data_ind_cur in range(data_size_min):
        t1 = data_1[data_ind_cur][timestamp_index]
        t2 = data_2[data_ind_cur][timestamp_index]

        if (abs(t1 - t2) <= t_threshold):
            data_filtered_1.append(data_1[data_ind_cur])
            data_filtered_2.append(data_2[data_ind_cur])

    return data_filtered_1, data_filtered_2

def data_filtered_get(file_name_1, file_name_2, t_threshold, timestamp_index=-1):
    pos_data_1 = data_loader.load_data(file_name_1, 1, False)
    pos_data_2 = data_loader.load_data(file_name_2, 1, False)

    data_filtered_1, data_filtered_2 = filter_for_timestamps(pos_data_1, pos_data_2, t_threshold, timestamp_index)

    return data_filtered_1, data_filtered_2
