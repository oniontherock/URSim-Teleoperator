import threading
import time
import data_format
import data_tracker
import random
from rtde_receive import RTDEReceiveInterface

t0 = 0

class TCP_Sampler:
    def __init__(self, receive_ip, name):
        self.receive_ip = receive_ip
        self.receive_interface = RTDEReceiveInterface(receive_ip)
        self.name = name

    def update_random(self):

        random_period = random.uniform(1, 10)*1e6  # Random period between 1e6ns and 10e6ns
        BUFFER_LEN:int = 2e6 # 2ms buffer, in nanoseconds

        t_ns_start = time.perf_counter_ns()
        frameCount = 1

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
                random_period = random.uniform(1, 10)*1e6  # Random period between 1e6ns and 100e6ns

            if self.receive_interface:

                tcp_pos = self.receive_interface.getActualTCPPose()
                data_tracker.data_quick_write(self.name, ['x', 'y', 'z', 't_write'], [tcp_pos[0], tcp_pos[1], tcp_pos[2], (time.perf_counter_ns() // 1000000) - t0])

receive_ip = "localhost"

kill_event = threading.Event()

tcp_sampler = TCP_Sampler(receive_ip, "tcp_sampler")
tcp_sampler_thread = threading.Thread(target=tcp_sampler.update_random)



def start_all_threads():
    kill_event.clear()
    tcp_sampler_thread.start()

def kill_all_threads():
    kill_event.set()
    tcp_sampler_thread.join()

