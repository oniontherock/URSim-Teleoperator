import time
import landmark_gatherer
import opencv_handler
import landmark_processor
import landmark_mapper
import robot_director
import data_format
import data_tracker
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

                    frame_counter = 0
                    with opencv_handler.frame_counter_lock:
                        frame_counter = opencv_handler.frame_counter

                    data_ind = data_tracker.data_dict_init("timestamps")
                    data_tracker.data_element_add_group("timestamps", data_ind, ['t_obtained', 't_used', 'frame_used'], [timestamp, (time.perf_counter_ns() // 1000000) - t0, frame_counter])
                    data_tracker.data_quick_write("pre_filter_position", ['x', 'y', 'z', 't_write'], [wrist_position[0], wrist_position[1], wrist_position[2], timestamp])

                    wrist_position = landmark_processor.filter_wrist_position(wrist_position, (time.perf_counter_ns() // 1000000) - t0)
                    data_tracker.data_quick_write("post_filter_position", ['x', 'y', 'z', 't_write'], [wrist_position[0], wrist_position[1], wrist_position[2], timestamp])
                    position_mapped = landmark_mapper.wrist_map_to_robot(wrist_position)

                    data_tracker.data_element_add("timestamps", data_ind, "t_processed", (time.perf_counter_ns() // 1000000) - t0)

                    robot_director.update_target(position_mapped, data_ind)

            while True:
                data_tracker.data_log_next() # here we process a single data_report. We technically could wait until the program is fully finished running. But we do it here so we don't have a massive queue at the end of the program (especially for large files). If performance is absolutely critical this line can be removed (unlikely to change performance in a significant way though)

                if data_tracker.data_log_queue.qsize() <= 6:
                    break

finally:

    robot_director.end()

    opencv_handler.end()

# this code only runs on successful execution of the program. If an error occurs these remaining lines won't run. If something MUST run put in in the "finally" above

data_format.data_finalize()

print("Program End")
