import threading
import time
import data_format
import data_tracker
import random
from rtde_receive import RTDEReceiveInterface

t0 = 0

class TCP_Sampler:
    def __init__(self, receive_ip, frequency, name):
        self.receive_ip = receive_ip
        self.receive_interface = RTDEReceiveInterface(receive_ip)
        self.frequency = frequency
        self.name = name

    def update(self):

        PERIOD:int = (1e9/self.frequency)
        BUFFER_LEN:int = 2e6 # 2ms buffer, in nanoseconds

        t_ns_start = time.perf_counter_ns()
        frameCount = 1

        # fps_timer = 0
        # second_timer_milli = 0
        # t_ns_prev = 0

        while (self.receive_interface.isConnected()):

            if kill_event.is_set():
                break

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

            if self.receive_interface:

                tcp_pos = self.receive_interface.getActualTCPPose()
                data_tracker.data_quick_write(self.name, ['x', 'y', 'z', 't_write'], [tcp_pos[0], tcp_pos[1], tcp_pos[2], (time.perf_counter_ns() // 1000000) - t0])
    def update_random(self):

        random_period = random.uniform(1, 100)*1e6  # Random period between 1e6ns and 100e6ns
        BUFFER_LEN:int = 2e6 # 2ms buffer, in nanoseconds

        t_ns_start = time.perf_counter_ns()
        frameCount = 1

        # fps_timer = 0
        # second_timer_milli = 0
        # t_ns_prev = 0

        while (self.receive_interface.isConnected()):

            if kill_event.is_set():
                break

            t_ns_now = time.perf_counter_ns()

            t_ns_deadline = t_ns_start + (frameCount * random_period)


            if (t_ns_now >= t_ns_deadline):
                pass
            elif (t_ns_now > (t_ns_deadline - BUFFER_LEN)): # if we are within the buffer, busy wait and then continue the next iteration
                continue
            else:
                t_ns_diff  = (t_ns_deadline - t_ns_now) - BUFFER_LEN

                if (t_ns_diff > 0):
                    time.sleep(float(t_ns_diff) / 1e9)

                continue

            while (t_ns_now >= (t_ns_start + (frameCount * random_period))):
                frameCount += 1
                random_period = random.uniform(1, 100)*1e6  # Random period between 1e6ns and 100e6ns

            if self.receive_interface:

                tcp_pos = self.receive_interface.getActualTCPPose()
                data_tracker.data_quick_write(self.name, ['x', 'y', 'z', 't_write'], [tcp_pos[0], tcp_pos[1], tcp_pos[2], (time.perf_counter_ns() // 1000000) - t0])

receive_ip = "localhost"

kill_event = threading.Event()

sampler_1 = TCP_Sampler(receive_ip, 1, "sampler1")
thread_1 = threading.Thread(target=sampler_1.update)

sampler_2 = TCP_Sampler(receive_ip, 30, "sampler2")
thread_2 = threading.Thread(target=sampler_2.update)

sampler_3 = TCP_Sampler(receive_ip, 125, "sampler3")
thread_3 = threading.Thread(target=sampler_3.update)

sampler_4 = TCP_Sampler(receive_ip, 500, "sampler4")
thread_4 = threading.Thread(target=sampler_4.update)

sampler_5 = TCP_Sampler(receive_ip, 2, "sampler5")
thread_5 = threading.Thread(target=sampler_5.update)

sampler_6 = TCP_Sampler(receive_ip, 1, "sampler6")
thread_6 = threading.Thread(target=sampler_6.update_random)



def start_all_threads():
    kill_event.clear()

    thread_1.start()
    thread_2.start()
    thread_3.start()
    thread_4.start()
    thread_5.start()
    thread_6.start()

def kill_all_threads():
    kill_event.set()
    thread_1.join()
    thread_2.join()
    thread_3.join()
    thread_4.join()
    thread_5.join()
    thread_6.join()

