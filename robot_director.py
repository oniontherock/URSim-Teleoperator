import threading
import landmark_saver
import time
from rtde_control import RTDEControlInterface

position_lock = threading.Lock()
robot_stop_flag = threading.Event()

robot_ready = threading.Event()
control_error = None

target = [0, 0.2, 0.6, 0.0, 3.14159, 0.0]
ts_grab = 0
ts_grab_last = 0
t0 = 0

# this is always running asynchronously at the update speed of the robot arm
def update_arm(robot_ip, stop_event:threading.Event):

    global control_error
    global ts_grab_last

    try:
        rtde = RTDEControlInterface(robot_ip, frequency=125)
    except Exception as e:
        control_error = e
        robot_ready.set()
        return
    
    robot_ready.set()

    try:
        while not stop_event.is_set():

            start_time = rtde.initPeriod()

            with (position_lock):
                tcp_pose = list(target)
                tsg = ts_grab
            

            if (tsg != 0) and (tsg != ts_grab_last):
                landmark_saver.data_point_publish_time_set(tsg, (time.perf_counter_ns() // 1000000) - t0)
                ts_grab_last = tsg

            rtde.servoL(tcp_pose, 0.5, 0.5, 1.0/125, 0.03, 500)


            rtde.waitPeriod(start_time)

    finally:
        for cleanup in (rtde.servoStop, rtde.stopScript, rtde.disconnect):
            try:
                cleanup()
            except Exception as e:
                print("Robot disconnection/cleanup failed: ", e)

    return
# this is called to update the target used in update_arm
def update_target(target_new, ts_grab_new):
    global target
    global ts_grab
    with (position_lock):
        target = list(target_new)
        ts_grab = ts_grab_new

control_ip = "localhost"
control_thread = threading.Thread()

# starts the control thread
def start():
    global control_thread, control_error

    if (control_thread.is_alive()):
        return

    robot_stop_flag.clear()
    robot_ready.clear()
    control_error = None
    
    control_thread = threading.Thread(target=update_arm, args=(control_ip, robot_stop_flag))

    control_thread.start()

    if not robot_ready.wait(timeout=10.0):
        robot_stop_flag.set()
        print("Robot Control Failed: connection timed out")
    elif control_error is not None:
        print("Robot Control Failed: ", control_error)
    
#ends the control thread safely
def end():
    robot_stop_flag.set()
    if control_thread.is_alive():
        control_thread.join()