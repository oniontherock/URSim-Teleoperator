import filtering

low_pass = filtering.LowPass(1)

def filter_wrist_position(wrist_position, timestamp):
    return low_pass.filter_value(wrist_position, timestamp)