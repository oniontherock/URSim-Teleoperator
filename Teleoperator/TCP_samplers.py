import threading
import time
import data_tracker

t0 = 0

class TCP_Sampler:
    def __init__(self, frequency, name, write_throttle):
        self.frequency = frequency
        self.name = name
        self.write_throttle = write_throttle

    def update(self):

        PERIOD:int = (1e9/self.frequency)
        BUFFER_LEN:int = 250e3 # 250us buffer, in nanoseconds

        t_ns_start = time.perf_counter_ns()
        frameCount = 1

        iterations_since_write = 0

        while not kill_event.is_set():

            t_ns_now = time.perf_counter_ns()

            t_ns_deadline = t_ns_start + (frameCount * PERIOD)


            if (t_ns_now >= t_ns_deadline):
                pass
            elif (t_ns_now > (t_ns_deadline - BUFFER_LEN)): # if we are within the buffer, busy wait and then continue the next iteration
                continue
            else:
                t_ns_diff  = (t_ns_deadline - t_ns_now) - BUFFER_LEN

                if (t_ns_diff > 0):
                    time.sleep(float(t_ns_diff) / 1e9)

                continue

            while (t_ns_now >= (t_ns_start + (frameCount * PERIOD))):
                frameCount += 1

            if (self.write_throttle):
                iterations_since_write += 1
                if (iterations_since_write >= 30):
                    iterations_since_write = 0
                    with int_lock:
                        data_tracker.data_quick_write(self.name, ['int', 't_write'], [test_int, time.perf_counter_ns()])
            else:
                # pass
                with int_lock:
                    data_tracker.data_quick_write(self.name, ['int', 't_write'], [test_int, time.perf_counter_ns()])

kill_event = threading.Event()

sampler_1 = TCP_Sampler(2500, "sampler1", False)
thread_1 = threading.Thread(target=sampler_1.update)

sampler_2 = TCP_Sampler(2500, "sampler2", True)
thread_2 = threading.Thread(target=sampler_2.update)

test_int = 0
int_lock = threading.Lock()

def start_all_threads():
    kill_event.clear()

    thread_1.start()
    thread_2.start()


def kill_all_threads():
    kill_event.set()
    thread_1.join()

    thread_2.join()


