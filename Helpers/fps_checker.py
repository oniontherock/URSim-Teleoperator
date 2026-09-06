import data_loader

data = data_loader.load_data("sampler6__2026_09_02__12h12m01s", 1)

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
    "Min Diff: ", min(diff), " ", diff.index(min(diff)), "\n",
    "Max Diff: ", max(diff), " ", diff.index(max(diff)), "\n"
    )