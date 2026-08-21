import time
import math
import landmark_gatherer
import opencv_handler
import landmark_processor
import landmark_mapper
import robot_director
import data_structures
import data_tracker
import data_saver
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

                    data_ind = data_tracker.data_dict_init("pos_ts")

                    data_tracker.data_element_add_group("pos_ts", data_ind, ['x', 'y', 'z', "ts_grab"], [wrist_position[0], wrist_position[1], wrist_position[2], timestamp])

                    data_tracker.data_element_add("pos_ts", data_ind, "ts_infer", (time.perf_counter_ns() // 1000000) - t0)



                    wrist_position = landmark_processor.filter_wrist_position(wrist_position, time.perf_counter_ns() // 1000000)
                    
                    position_mapped = landmark_mapper.wrist_map_to_robot(wrist_position)

                    robot_director.update_target(position_mapped, data_ind)
            data_tracker.data_log_next() # here we process a single data_report. We technically could wait until the program is fully finished running. But we do it here so we don't have a massive queue at the end of the program (especially for large files). If performance is absolutely critical this line can be removed (unlikely to change performance in a significant way though)
finally:

    robot_director.end()

    opencv_handler.end()

data_tracker.data_log_force_process_all()

data = data_tracker.data_format("pos_ts")

data_saver.data_save_singular("pos_ts", data["data"], data["format"], data["header"])

# kill rtde script-to-robot interation
# print that the program is finished
print("Program End")
