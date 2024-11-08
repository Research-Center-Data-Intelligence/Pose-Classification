import joblib
import numpy as np

label_map = {
    "ARM_RAISE": 0,
    "CHAIR_RAISE_AND_STEP": 1,
    "HEAD_LIFT": 2,
    "LEG_RAISE": 3,
    "PICK_UP": 4,
    "SIT_ALL_FOURS_RISE": 5,
    "SIT_UP": 6,
    "SUPINE_TO_PRONE": 7,
}


def load_sequence(seq_path):
    seq = joblib.load(seq_path)
    return seq[0]["keypoints"]


def normalize_keypoints(keypoints):
    normalized_keypoints = []

    for frame_index in range(len(keypoints)):
        keypoints_frame = keypoints[frame_index][:, :2]  # Extract x, y

        hip_x = keypoints_frame[11, 0]  # x-coordinate of the left hip
        hip_y = keypoints_frame[11, 1]  # y-coordinate of the left hip

        # Normalize the keypoints based on the hip position
        keypoints_frame[:, 0] = (
            keypoints_frame[:, 0] - hip_x
        )  # Center x-coordinates around the hip
        keypoints_frame[:, 1] = (
            keypoints_frame[:, 1] - hip_y
        )  # Center y-coordinates around the hip

        normalized_keypoints.append(keypoints_frame)

    return np.array(normalized_keypoints)
