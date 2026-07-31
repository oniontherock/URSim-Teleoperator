import cv2
import numpy as np

# create window
cv2.namedWindow("MyWindow")
# declare and initialize video capture from default webcame, allows you to read webcam data on demand
videoCapture = cv2.VideoCapture(0)

frameCapOk, frame = videoCapture.isOpened(), None


def process_frame() -> tuple[bool, cv2.typing.MatLike]:
    # get next frame from webcam
    frameCapOk, frame = videoCapture.read()

    if not frameCapOk:
        return (False, np.zeros((1, 1, 1), dtype="uint8"))

    # updates the window with the current frame, only ever runs if frameCapOk is true
    cv2.imshow("MyWindow", frame) # type: ignore

    return (True, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) # type: ignore

# this ends a frame and returns whether the program should continue running, if it's False, the program should end
def finish_frame():
    # check if esc was pressed, if it was, return false which ends the program
    keyPress = cv2.waitKey(1)
    return not (keyPress == 27)

def end():
    # close window and release webcam VideoCapture device
    cv2.destroyWindow("MyWindow")
    videoCapture.release()