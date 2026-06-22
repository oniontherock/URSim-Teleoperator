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


MODEL_PATH = Path(__file__).parent / "pose_landmarker_heavy.task"

pose = {"landmarks": None, "image": None}
lock = threading.Lock()

def on_result(result, output_image, timestamp_ms):
    with lock:
        pose["landmarks"] = result.pose_world_landmarks 
        pose["image"] = output_image

base_options = mediapipe.tasks.BaseOptions(model_asset_path = str(MODEL_PATH))
options = vision.PoseLandmarkerOptions(base_options=base_options, running_mode = vision.RunningMode.LIVE_STREAM, result_callback = on_result)

rtde = RTDEControlInterface("localhost")

# create window
cv2.namedWindow("MyWindow")
# declare and initialize video capture from default webcame, allows you to read webcam data on demand
videoCapture = cv2.VideoCapture(0)

# Get first frame and register if it works
if videoCapture.isOpened():
    # get whether the frame was captured successfully, and the actual frame if it did work
    frameCapOk, frame = videoCapture.read()
else:
    frameCapOk = False

# wrist ID in mediapipe is 16
WRIST_ID = 16

# define minimum coordinates
X_MIN = -0.35
Y_MIN = -0.35
Z_MIN = -0.35
# define maximum coordinates
X_MAX = 0.35
Y_MAX = 0.35
Z_MAX = 0.35

FIXED_ORIENT = [0.0, 3.14159, 0.0]  # tool pointing down (axis-angle, rad) — verify for your tool
VIS_THRESHOLD = 0.5

def lerp(t, lo, hi):  return lo + t * (hi - lo)
def clamp(v, lo, hi): return max(lo, min(hi, v))

def wrist_position_get(world_landmarks):
    wrist = world_landmarks[0][WRIST_ID]
    if wrist.visibility < VIS_THRESHOLD:
        return None
    return (wrist.x, wrist.y, wrist.z)              # same convention you printed


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


with vision.PoseLandmarker.create_from_options(options) as landmarker:

    t0 = time.time()
    while (frameCapOk):

        # updates the window with the current frame, only ever runs if frameCapOk is true
        cv2.imshow("MyWindow", frame) # type: ignore

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # type: ignore
        mediapipe_image = mediapipe.Image(image_format = mediapipe.ImageFormat.SRGB, data = frame_rgb)
        landmarker.detect_async(mediapipe_image, int((time.time() - t0) * 1000))

        # get next frame from webcam
        frameCapOk, frame = videoCapture.read()

        with lock:
            lm = pose["landmarks"]
        if lm:
            wrist_position = wrist_position_get(lm)
            if wrist_position is not None:
                target = map_to_robot(wrist_position)
                print(target[0])
                print(" ")
                print(target[1])
                print(" ")
                print(target[2])
                print("\n")
                rtde.servoL(target, 0.5, 0.5, 1.0/125, 0.1, 300)

        # check if esc was pressed, if it was, break the loop
        keyPress = cv2.waitKey(20)
        if (keyPress == 27):
            break



# close window and release webcam VideoCapture device
cv2.destroyWindow("MyWindow")
videoCapture.release()
# kill rtde script-to-robot interation
rtde.servoStop()
rtde.stopScript()
# print that the program is finished
print("Program End")
