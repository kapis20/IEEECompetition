import cv2

import mediapipe as mp
import pandas as pd

VIDEO_FILE_PATH = "video_files/squat.mp4"
COLOURS = {"mint": (137, 180, 62),
           "cyan": (255, 255, 0),
           "red": (33, 33, 217),
           "orange": (0, 102, 255),
           "white": (255, 255, 255),
           "teal": (200, 90, 56)}

COLUMN_HEADERS = ["frame", "time_stamp"]


def process_mp4(video_file_path: str, display: bool = False) -> pd.DataFrame:
    """
    Function to Load video media and post-process using mediapipe landmark tracking
    :param video_file_path:
    :param display:
    :return:
    """

    """ Create data frame for landmark data storage """
    df = pd.DataFrame(columns=COLUMN_HEADERS)

    """ Configure Video Capture """
    cap = cv2.VideoCapture(video_file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    """ Configure mediapipe landmarks for processing """
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_count = 0
        while cap.isOpened():
            """ Config frame """
            ret, frame = cap.read()
            time_stamp = frame_count * fps

            """ mediapipe pose processing """
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True

            """ Prepare image for visualising """
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            width = int(cap.get(3) / 2)
            height = int(cap.get(4) / 2)
            image = cv2.resize(image, (width, height))

            """ Draw landmarks on image frame """
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=COLOURS["teal"], thickness=3, circle_radius=3),
                                      mp_drawing.DrawingSpec(color=COLOURS["white"], thickness=1,
                                                             circle_radius=2))

            cv2.imshow("MediaPipe Feed", image)

            frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    return df


def main():
    data = process_mp4(video_file_path=VIDEO_FILE_PATH, display=True)
    print(data)


if __name__ == "__main__":
    main()
