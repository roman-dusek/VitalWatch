import argparse
import cv2
import numpy as np
import logging
import os


def generate_frame(video_path: str, save_path: str, threshold: int = 700, time_window: int = 20):

    if not os.path.exists(video_path):
        logging.error("Video in %s doenest exists!", video_path)
        raise ValueError(f"Video in {video_path} doesnt exists!")

    capture = cv2.VideoCapture(video_path)

    if not capture.isOpened():
        logging.error("Error during opening video!")
        raise RuntimeError("Error during opening video!")

    IS_START = False
    counter = 0
    dimension = 0.0
    previous_frame = None
    previous_error = 0.0
    previous_derivation = 0.0
    dim = (0, 0)

    file_name, _ = video_path.split(".")

    # Read and process frames in a loop
    image_counter = 0
    while True:
        ret, frame = capture.read()
        counter += 1

        # Break the loop if there are no more frames
        if not ret:
            break

        if counter % time_window == 0:
            if not IS_START:
                width = int(frame.shape[1])
                height = int(frame.shape[0])
                dim = (width, height)
                previous_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_LANCZOS4)
                previous_frame = cv2.GaussianBlur(previous_frame, (5, 5), 0)
                dimension = float(width * height)
                previous_error = 0

                IS_START = True
                continue

            err = np.sum((frame.astype("float") - previous_frame.astype("float")) ** 2)
            err /= dimension
            derivation = abs(previous_error - err)  # derivation
            logging.info("%s iteration is %s %s", counter, err, derivation)

            if abs(derivation - previous_derivation) >= threshold:
                cv2.imwrite(f"{save_path}/{file_name}-{image_counter}.jpg", frame)
                image_counter += 1
                cv2.imshow("Frame", frame)
            previous_frame = frame
            previous_error = err
            previous_derivation = derivation

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all frames
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='video interest frame selector',
        description='Program generate interesting frame between sequence in jpeg',
    )
    parser.add_argument('-f', '--file-name', help='Set the file path to video file', required=True)
    parser.add_argument('-w', '--time-window', default=20,
                        help='Set the time window, where algorithm will search interesting key frame', type=int, required=False)
    parser.add_argument('-t', '--threshold', default=700,
                        help='Set the threshold how many pixels can be detect as interesting frame', required=False, type=int
    )
    parser.add_argument('-s', '--save-path', help='Set the saving path', required=False, default="myfiles/images")

    args = parser.parse_args()
    generate_frame(
        video_path=args.file_name,
        save_path=args.save_path,
        threshold=args.threshold,
        time_window=args.time_window
    )
