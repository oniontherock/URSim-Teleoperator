import cv2
import time
import threading
import numpy
import mediapipe
import mediapipe
from mediapipe.tasks.python import vision, BaseOptions
from rtde_control import RTDEControlInterface
from pathlib import Path
import math

MODEL_PATH = Path(__file__).parent / "pose_landmarker.task"

pose = {"landmarks": None, "timestamp": 0}
lock = threading.Lock()
position_lock = threading.Lock()

is_robot_running = True

def on_result(result, output_image, timestamp_ms):
    with lock:
        pose["landmarks"] = result.pose_world_landmarks
        pose["timestamp"] = timestamp_ms 

base_options = mediapipe.tasks.BaseOptions(model_asset_path = str(MODEL_PATH))
options = vision.PoseLandmarkerOptions(base_options=base_options, running_mode = vision.RunningMode.LIVE_STREAM, result_callback = on_result)

def calculate_alpha(hz):
    pass

class Filter:
    def __init__(self, alpha):
        self.val_filtered_prev = (None, None, None)
        self.alpha = alpha
        self.first_run = True

    # does no filtering in basic filter type
    def filter_value(self, val:tuple) -> tuple:
        self.first_run = False
        return val

class LowPass(Filter):
    def filter_value(self, val:tuple) -> tuple:

        # we need to set a value for val_filtered_prev if we've never run before, so we assign it to val on the first run.
        # this basically makes our first run's filtered value just be the unfilitered value, but just for the first run
        if (self.first_run):
            self.first_run = False
            self.val_filtered_prev = val

        val_filtered = (
            (val[0] * self.alpha) + (self.val_filtered_prev[0] * (1.0 - self.alpha)),
            (val[1] * self.alpha) + (self.val_filtered_prev[1] * (1.0 - self.alpha)),
            (val[2] * self.alpha) + (self.val_filtered_prev[2] * (1.0 - self.alpha))
            )
        self.val_filtered_prev = val_filtered

        return val_filtered

# create window
cv2.namedWindow("MyWindow")
# declare and initialize video capture from default webcame, allows you to read webcam data on demand
videoCapture = cv2.VideoCapture(0)

frameCapOk, frame = videoCapture.isOpened(), None

# wrist ID in mediapipe is 16
WRIST_ID = 16

FIXED_ORIENT = [0.0, 3.14159, 0.0]  # tool pointing down (axis-angle, rad) — verify for your tool
VIS_THRESHOLD = 0.5

def clamp(v, lo, hi): return max(lo, min(hi, v))

def wrist_position_get(world_landmarks):
    wrist = world_landmarks[0][WRIST_ID]
    if wrist.visibility < VIS_THRESHOLD:
        return None
    return [wrist.x, wrist.y, wrist.z]

def filter_wrist_position(wrist_position, filter:Filter):
    return filter.filter_value(wrist_position)


# this comes in after filter
def map_to_robot(d):
    rx = d[0]*1.2
    ry = d[1]*1.2
    rz = d[2]*1.2

    min_dist = 0.1
    max_dist = 0.8

    dist_from_base = math.sqrt((rx*rx)+(ry*ry)+(rz*rz))
    if (dist_from_base >max_dist):
        rx = (rx / dist_from_base) * max_dist
        ry = (ry / dist_from_base) * max_dist
        rz = (rz / dist_from_base) * max_dist
    elif (dist_from_base < min_dist):
        rx = (rx / dist_from_base) * min_dist
        ry = (ry / dist_from_base) * min_dist
        rz = (rz / dist_from_base) * min_dist

    return [-rz, rx, -ry, *FIXED_ORIENT]

target = [0, 0.5, 0.5, 0.0, 3.14159, 0.0]

def update_arm(robot_ip):

    target_joints = None

    rtde = RTDEControlInterface(robot_ip)


    
    while (is_robot_running):
        start_time = rtde.initPeriod()

        with (position_lock):
            target_joints = target

        rtde.servoL(target_joints, 0.5, 0.5, 1.0/125, 0.03, 500)

        rtde.waitPeriod(start_time)

    rtde.servoStop()
    rtde.stopScript()
    rtde.disconnect()

    return

control_ip = "localhost"
control_thread = threading.Thread(target=update_arm, args=(control_ip,))

# we need to record the previous timestamp, and only fire the tracker when the timestamp changes.
# basically, if we just fire whenever, we can get the same position sent bunch of times every frame,
# because if our control loop is running faster than our mediapipe loop can receive new data, then we will run the control loop with the same stale data.
# so we only allow the control loop to run the single moment that the mediapipe loop runs/receives new data.
previous_timestamp = -1

low_pass = LowPass(0.02)
try:
    with vision.PoseLandmarker.create_from_options(options) as landmarker:


        control_thread.start()

        start_time = time.perf_counter_ns()
        while (frameCapOk):


            # get next frame from webcam
            frameCapOk, frame = videoCapture.read()

            if not frameCapOk:
                break

            # updates the window with the current frame, only ever runs if frameCapOk is true
            cv2.imshow("MyWindow", frame) # type: ignore

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # type: ignore
            mediapipe_image = mediapipe.Image(image_format = mediapipe.ImageFormat.SRGB, data = frame_rgb)
            landmarker.detect_async(mediapipe_image, (time.perf_counter_ns() - start_time) // 1000000)

            with lock:
                lm = pose["landmarks"]
                ts = pose["timestamp"]
            if (lm) and (previous_timestamp != ts):
                previous_timestamp = ts
                wrist_position = wrist_position_get(lm)
                if wrist_position is not None:

                    wrist_position = filter_wrist_position(wrist_position, low_pass)
                    
                    position_mapped = map_to_robot(wrist_position)

                    with (position_lock):
                        target = position_mapped
                

            # check if esc was pressed, if it was, break the loop
            keyPress = cv2.waitKey(1)
            if (keyPress == 27):
                break
finally:
    is_robot_running = False
    if control_thread.is_alive():
        control_thread.join()

    # close window and release webcam VideoCapture device
    cv2.destroyWindow("MyWindow")
    videoCapture.release()

# kill rtde script-to-robot interation
# print that the program is finished
print("Program End")
