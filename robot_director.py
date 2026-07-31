import threading
from rtde_control import RTDEControlInterface

position_lock = threading.Lock()
robot_stop_flag = threading.Event()

robot_ready = threading.Event()
control_error = None

target = [0, 0.5, 0.5, 0.0, 3.14159, 0.0]

# this is always running asynchronously at the update speed of the robot arm
def update_arm(robot_ip, stop_event:threading.Event):

    global control_error
    try:
        rtde = RTDEControlInterface(robot_ip)
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
def update_target(target_new):
    global target
    with (position_lock):
        target = list(target_new)

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