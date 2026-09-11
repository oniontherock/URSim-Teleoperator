import data_loader

skip_count = 66
full_avg = 0
tally_count = 0


def process_overlaps(filename, preexisting_overlap_dict):

    global tally_count
    global full_avg

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

        tally_count += 1
        full_avg += overlap





overlaps:dict = {0:0}

for i in range(1, 15):

    # we exclude videos 6-11 in this because they use a video that is producing very odd results due to lack of visiblity on hand, and just generally bad recording procedures.
    if (i in range(6,11)):
        continue

    process_overlaps(f"timestamps{i}", overlaps)

sorted_overlaps = dict(sorted(overlaps.items()))

final_avg = full_avg / tally_count

print(
    *(f"overlap count for {key}: {sorted_overlaps[key]}\n" for key in sorted_overlaps)
    )
print(f"average overlap: {final_avg}")