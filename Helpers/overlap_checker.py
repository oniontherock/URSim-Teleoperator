import data_loader

skip_count = 31

data = data_loader.load_data("timestamps__2026_09_08__10h29m40s", skip_count, False)

size = len(data)


overlaps = [0,0,0,0,0,0,0,0,0,0]
avg_overlap = 0

for data_cur_ind in range(size-1):

    data_cur = data[data_cur_ind]
    data_next = data[data_cur_ind+1]

    overlap = round(data_cur[3] - data_next[0])

    avg_overlap += overlap

    overlaps[overlap] += 1


avg_overlap /= size-1

print(
    "Data points: ", size, "\n",
    "Average overlap: ", avg_overlap, "\n",
    *(f"overlap count for {i}: {overlaps[i]}\n" for i in range(len(overlaps)))
    )