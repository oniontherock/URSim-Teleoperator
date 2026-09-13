import data_loader

skip_count = 1000

data = data_loader.load_data("PUT_FILE_NAME_HERE", skip_count)

ts1 = data[3]

fps = []
diff = []

size = len(ts1)

for i in range(size-1):
    fps.append(1.0/((ts1[i+1]-ts1[i])*1e-3))
    diff.append(ts1[i+1]-ts1[i])

avg = 0
for i in range(size-1):
    avg += diff[i]

avg /= (size - 1)

final_fps = 1000/avg

print(
    "Data points: ", size, "\n",
    "Average FPS: ", final_fps, "\n",
    "Min Diff: ", min(diff), " ", diff.index(min(diff))+skip_count, "\n",
    "Max Diff: ", max(diff), " ", diff.index(max(diff))+skip_count, "\n"
    )