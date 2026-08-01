import cv2
import numpy as np
import threading

# create window
cv2.namedWindow("MyWindow")
# declare and initialize video capture from default webcame, allows you to read webcam data on demand
videoCapture = cv2.VideoCapture(0)

cv2.VideoCapture(0, cv2.CAP_DSHOW)

videoCapture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

frameCapOk, frame, frame_index = videoCapture.isOpened(), None, 0
cap_good = frameCapOk
frame_lock = threading.Lock()

def process_frame():

    global frameCapOk
    global frame
    global frame_index
    global cap_good

    frameCapOkThreaded, frameThreaded = videoCapture.read()

    while (frameCapOkThreaded):

        # get next frame from webcam but do it outside the with statement to avoid blocking while waiting for the read
        frameCapOkThreaded, frameThreaded = videoCapture.read()

        if not frameCapOkThreaded:
            continue

        with frame_lock:
            frameCapOk, frame = frameCapOkThreaded, frameThreaded
            frame_index += 1

frame_thread = threading.Thread(target=process_frame)

frame_thread.start()

# this ends a frame and returns whether the program should continue running, if it's False, the program should end
def finish_frame():
    # check if esc was pressed, if it was, return false which ends the program
    keyPress = cv2.waitKey(1)
    return not (keyPress == 27)

def end():
    # close window and release webcam VideoCapture device
    cv2.destroyWindow("MyWindow")
    videoCapture.release()
    frame_thread.join()