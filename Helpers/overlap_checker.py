import data_loader

skip_count = 31

def process_overlaps(filename, preexisting_overlap_dict):

    data = data_loader.load_data(filename, skip_count, False)

    size = len(data)

    for data_cur_ind in range(size-1):

        data_cur = data[data_cur_ind]
        data_next = data[data_cur_ind+1]

        overlap = round(data_cur[3] - data_next[0])

        if overlap in preexisting_overlap_dict:
            preexisting_overlap_dict[overlap] += 1
        else:
            preexisting_overlap_dict[overlap] = 1





overlaps:dict = {0:0}

for i in range(1, 15):
    process_overlaps(f"timestamps{i}", overlaps)

sorted_overlaps = dict(sorted(overlaps.items()))

print(
    *(f"overlap count for {key}: {sorted_overlaps[key]}\n" for key in sorted_overlaps)
    )