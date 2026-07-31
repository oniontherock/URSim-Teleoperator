import time
import math
import landmark_gatherer
import opencv_handler
import landmark_processor
import landmark_mapper
import robot_director

# we need to record the previous timestamp, and only fire the tracker when the timestamp changes.
# basically, if we just fire whenever, we can get the same position sent bunch of times every frame,
# because if our control loop is running faster than our mediapipe loop can receive new data, then we will run the control loop with the same stale data.
# so we only allow the control loop to run the single moment that the mediapipe loop runs/receives new data.
previous_timestamp = -1

try:
    with landmark_gatherer.vision.PoseLandmarker.create_from_options(landmark_gatherer.options) as landmarker:

        robot_director.start()

        t0 = time.perf_counter_ns() // 1000000
        while (opencv_handler.frameCapOk):

            frame = opencv_handler.process_frame()
            if not frame[0]:
                break

            landmark_gatherer.landmark_async_process_from_frame(landmarker, frame[1], (time.perf_counter_ns() // 1000000) - t0)

            landmarks, timestamp = landmark_gatherer.landmarks_get_with_timestamp()

            if (landmarks) and (previous_timestamp != timestamp):
                previous_timestamp = timestamp
                wrist_position = landmark_gatherer.wrist_position_get(landmarks)
                if wrist_position is not None:

                    wrist_position = landmark_processor.filter_wrist_position(wrist_position, timestamp)
                    
                    position_mapped = landmark_mapper.wrist_map_to_robot(wrist_position)

                    robot_director.update_target(position_mapped)
                

            programOk = opencv_handler.finish_frame()
            if (not programOk):
                break
finally:

    robot_director.end()

    opencv_handler.end()


# kill rtde script-to-robot interation
# print that the program is finished
print("Program End")
