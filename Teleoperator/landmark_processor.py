import filtering

our_filter = filtering.MovingAverage(10)

def filter_wrist_position(wrist_position, timestamp):
    return our_filter.filter_value(wrist_position, timestamp)