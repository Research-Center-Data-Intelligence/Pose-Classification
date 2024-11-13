import matplotlib.pyplot as plt
import joblib
import matplotlib.animation as animation
import numpy as np

class KeypointVisualizer:
    def __init__(self, tracking_results_path):
        self.tracking_results = self.load_tracking_results(tracking_results_path)
        self.keypoints = self.tracking_results[0]["keypoints"]
        self.bbox = self.tracking_results[0]["bbox"]

        # 17-keypoint COCO format
        self.limb_connections = [
            (0, 1),
            (0, 2),  # Nose to Eyes
            (1, 3),
            (2, 4),  # Eyes to Ears
            (5, 6),  # Shoulders
            (5, 7),
            (7, 9),  # Left arm (Shoulder -> Elbow -> Wrist)
            (6, 8),
            (8, 10),  # Right arm (Shoulder -> Elbow -> Wrist)
            (11, 12),  # Hips
            (5, 11),
            (6, 12),  # Torso (Shoulders to Hips)
            (11, 13),
            (13, 15),  # Left leg (Hip -> Knee -> Ankle)
            (12, 14),
            (14, 16),  # Right leg (Hip -> Knee -> Ankle)
        ]

        self.fig, self.ax = plt.subplots()

    def load_tracking_results(self, tracking_results_path):
        tracking_results = joblib.load(tracking_results_path)
        print(f"Type of loaded data: {type(tracking_results)}")
        return tracking_results

    def normalize_keypoints(self, keypoints, bbox):
        bbox_center_x, bbox_center_y, bbox_scale = bbox
        normalized_keypoints = np.copy(keypoints)
        normalized_keypoints[:, 0] = (keypoints[:, 0] - bbox_center_x) / bbox_scale
        normalized_keypoints[:, 1] = (keypoints[:, 1] - bbox_center_y) / bbox_scale
        return normalized_keypoints

    def init_plot(self):
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(100, -100)  
        return self.ax.scatter([], [], c="r")

    def update_plot(self, frame_index):
        self.ax.cla()

        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(100, -100)

        keypoints = self.keypoints[frame_index][:, :2]
        bbox = self.bbox[frame_index] 

        normalized_keypoints = self.normalize_keypoints(keypoints, bbox)

        scatter = self.ax.scatter(
            normalized_keypoints[:, 0], normalized_keypoints[:, 1], c="r"
        )

        for connection in self.limb_connections:
            start, end = connection
            self.ax.plot(
                [normalized_keypoints[start, 0], normalized_keypoints[end, 0]],
                [normalized_keypoints[start, 1], normalized_keypoints[end, 1]],
                "b-",
            )

        midpoint_x = (normalized_keypoints[5, 0] + normalized_keypoints[6, 0]) / 2
        midpoint_y = (normalized_keypoints[5, 1] + normalized_keypoints[6, 1]) / 2
        self.ax.plot(
            [normalized_keypoints[0, 0], midpoint_x],
            [normalized_keypoints[0, 1], midpoint_y],
            "b-",
        )  # Neck line

        return (scatter,)

    def create_animation(self, interval=10):
        ani = animation.FuncAnimation(
            self.fig,
            self.update_plot,
            frames=len(self.keypoints),
            init_func=self.init_plot,
            interval=interval,
        )
        plt.show()


def main():
    seq_path = "dataset/2D/kps_unseen/STP.pth"
    visualizer = KeypointVisualizer(seq_path)
    visualizer.create_animation()


main()
