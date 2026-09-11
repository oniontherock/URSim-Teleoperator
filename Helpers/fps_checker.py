import data_loader

# NOTE, we exclude videos 6-11 in this because they use a video that is producing very odd results due to lack of visiblity on hand, and just generally bad recording procedures.

for j in range(1, 15):

    if (j in range(6,11)):
        continue

    name = f"timestamps{j}"

    data = data_loader.load_data(name, 31)

    ts1 = data[3]

    # NOTE, Timestamps1-5 are TestVideo. Timestamps 6-10 are TestVideo2. Timestamps 11-15 are hand_held

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
        f"Data points in {name} : ", size, "\n",
        "Average FPS: ", final_fps, "\n",
        "Min Diff: ", min(diff), " ", diff.index(min(diff)), "\n",
        "Max Diff: ", max(diff), " ", diff.index(max(diff)), "\n"
        )