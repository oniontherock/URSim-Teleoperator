import math

class Filter:
    def __init__(self):
        self.val_filtered_prev = (None, None, None)
        self.first_run = True
        self.timestamp_last = 0 # an absolute value in time, not a difference, just the last time that the filter was called

    # does no filtering in basic filter type
    def filter_value(self, val:tuple, timestamp) -> tuple:
        self.first_run = False
        self.timestamp_last = timestamp
        return val


class LowPass(Filter):

    def __init__(self, cutoff):
        self.val_filtered_prev = (0, 0, 0)
        self.first_run = True
        self.timestamp_last = 0 # an absolute value in time, not a difference, just the last time that the filter was called
        self.cutoff = cutoff
        self.RC_milli = 1000 / (2 * math.pi * self.cutoff) # the RC time constant that would produce the given cutoff frequency, in milliseconds

    def calculate_alpha(self, dt) -> float:
        return dt / (self.RC_milli + dt)

    def filter_value(self, val:tuple, timestamp) -> tuple:

        dt = timestamp - self.timestamp_last
        self.timestamp_last = timestamp
        alpha = self.calculate_alpha(dt)

        # we need to set a value for val_filtered_prev if we've never run before, so we assign it to val on the first run.
        # this basically makes our first run's filtered value just be the unfilitered value, but just for the first run
        if (self.first_run):
            self.first_run = False
            self.val_filtered_prev = val

        val_filtered = (
            (val[0] * alpha) + (self.val_filtered_prev[0] * (1.0 - alpha)),
            (val[1] * alpha) + (self.val_filtered_prev[1] * (1.0 - alpha)),
            (val[2] * alpha) + (self.val_filtered_prev[2] * (1.0 - alpha))
            )
        self.val_filtered_prev = val_filtered

        return val_filtered