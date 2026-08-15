import time
import math
import landmark_gatherer
import opencv_handler
import landmark_processor
import landmark_mapper
import robot_director
import landmark_saver
import cv2

try:
    with landmark_gatherer.vision.PoseLandmarker.create_from_options(landmark_gatherer.options) as landmarker:

        robot_director.start()

        t0 = time.perf_counter_ns() // 1000000
        robot_director.t0 = t0

        while (opencv_handler.frameCapOk):

            opencv_handler.frame_pushed.wait()
            opencv_handler.frame_pushed.clear()

            with (opencv_handler.frame_lock):

                if not opencv_handler.frameCapOk:
                    break
                
                frame = opencv_handler.frame

            cv2.imshow("Teleoperator", frame)

            programOk = opencv_handler.finish_frame()
            if (not programOk):
                break

            landmark_gatherer.landmark_async_process_from_frame(landmarker, frame, (time.perf_counter_ns() // 1000000) - t0)

            if (landmark_gatherer.landmark_written.is_set()):
                landmarks, timestamp = landmark_gatherer.landmarks_get_with_timestamp()

                if not landmarks:
                    continue


                wrist_position = landmark_gatherer.wrist_position_get(landmarks)
                if wrist_position is not None:

                    landmark_saver.data_point_add(wrist_position[0], wrist_position[1], wrist_position[2], timestamp)

                    landmark_saver.data_point_infer_time_set(timestamp, (time.perf_counter_ns() // 1000000) - t0)

                    wrist_position = landmark_processor.filter_wrist_position(wrist_position, time.perf_counter_ns() // 1000000)
                    
                    position_mapped = landmark_mapper.wrist_map_to_robot(wrist_position)

                    robot_director.update_target(position_mapped, timestamp)
                
finally:

    robot_director.end()

    opencv_handler.end()

landmark_saver.data_save()

# kill rtde script-to-robot interation
# print that the program is finished
print("Program End")
