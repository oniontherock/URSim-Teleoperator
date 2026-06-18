import cv2
import time
import threading
import numpy
import mediapipe
import mediapipe
from mediapipe.tasks.python import vision, BaseOptions
from rtde_control import RTDEControlInterface
from pathlib import Path


MODEL_PATH = Path(__file__).parent / "pose_landmarker.task"

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

neutral = None          # set by pressing 'c' with hand at rest
smoothed = None         # EMA + step-limit state (full 6-vector)

ALPHA    = 0.2          # EMA: lower = smoother but laggier
MAX_STEP = 0.008        # max meters per axis per loop iteration (glitch guard)
GAIN     = 1.0
BOX      = [0.70, 0.7, 0.7]
WORKSPACE_CENTER = [-0.15, -0.45, 0.30]   # a reachable base-frame point

def wrist_delta(world_landmarks):
    w = world_landmarks[0][WRIST_ID]
    if w.visibility < VIS_THRESHOLD:
        return None
    return (w.x, w.z, -w.y)              # same convention you printed

def map_to_robot(d):
    rx = clamp(WORKSPACE_CENTER[0] + GAIN*(d[0]-neutral[0]), WORKSPACE_CENTER[0]-BOX[0], WORKSPACE_CENTER[0]+BOX[0])
    ry = clamp(WORKSPACE_CENTER[1] + GAIN*(d[1]-neutral[1]), WORKSPACE_CENTER[1]-BOX[1], WORKSPACE_CENTER[1]+BOX[1])
    rz = clamp(WORKSPACE_CENTER[2] + GAIN*(d[2]-neutral[2]), WORKSPACE_CENTER[2]-BOX[2], WORKSPACE_CENTER[2]+BOX[2])
    return [rx, ry, rz, *FIXED_ORIENT]

def smooth_and_limit(target, prev):
    if prev is None:
        return list(target)
    out = []
    for t, p in zip(target, prev):
        s = ALPHA*t + (1-ALPHA)*p                 # EMA smoothing
        out.append(clamp(s, p-MAX_STEP, p+MAX_STEP))  # reject jumps
    return out




with vision.PoseLandmarker.create_from_options(options) as landmarker:

    t_elapsed = 0

    t0 = time.time()
    t_last = t0
    set_base = False

    while (frameCapOk):

        if (t_elapsed > 6):
            set_base = True
        if (set_base):
            t_elapsed = 0

        t_elapsed += time.time() - t_last;
        t_last = time.time()

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
            d = wrist_delta(lm)
            if d is not None:
                if neutral is None or t_elapsed > 5:
                    neutral = d                  # press 'c' (hand at rest) to (re)calibrate
                elif neutral is not None:
                    target   = map_to_robot(d)
                    smoothed = smooth_and_limit(target, smoothed)
                    rtde.servoL(smoothed, 0.5, 0.5, 1.0/125, 0.1, 300)

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
