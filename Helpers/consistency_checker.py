import data_loader

data = data_loader.load_data(
    "timestamps__2026_08_31__09h27m09s",
        1
    )

# print(data)

timestamps = data[3]
frames = data[4]
data_offset = -745 # an offset for every data point, added to each point before printing
frame_offset = -30 # an offset for every frame, added to each frame before printing


data_size = len(timestamps)

for i in range(data_size):
    print(int(timestamps[i]) + data_offset, int(frames[i]) + frame_offset)







