import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import joblib
from scipy.linalg import null_space

print(__file__)
base_dir = os.path.dirname(os.path.abspath(__file__))
CURRENT_FILE = os.path.join(base_dir, "dataset/3D/kps_mirrored/ARM_RAISE/1.pkl")
# PREVIEW_TRIMMED_MODE = True

# if PREVIEW_TRIMMED_MODE:
#     CURRENT_FILE = f"dataset/trimmed_keypoints/{CURRENT_FILE}"
# else:
#     CURRENT_FILE = f"dataset/keypoints/{CURRENT_FILE}"

data = joblib.load(CURRENT_FILE)
kp3d = data["kp3d"] # if PREVIEW_TRIMMED_MODE else data[0]["kp3d"]  # Shape: (FRAMES, SKELETON (31), XYZ)
kp3d = kp3d[:, :17, :]  # Extract necessary keypoints only

# A = kp3d
# B = data[1]["kp3d"]
# kp3d = np.concatenate((A, B), axis=0)

skeleton_connections = [
    (0, 1), (0, 2), (1, 3), (2, 4),       # Nose to eyes and ears
    (5, 6), (5, 11), (6, 12),              # Shoulders and torso
    (5, 7), (7, 9),                        # Left arm
    (6, 8), (8, 10),                       # Right arm
    (11, 13), (13, 15),                    # Left leg
    (12, 14), (14, 16),                    # Right leg
    (11, 12)                               # Connect hips
]

def normalize_keypoints(keypoints):
    normalized_keypoints = []

    for frame_index in range(len(keypoints)):
        keypoints_frame = keypoints[frame_index][:, :3]
        
        
        hip_x, hip_y, hip_z = keypoints_frame[11]  #  left hip

        # Normalize
        keypoints_frame[:, 0] -= hip_x  
        keypoints_frame[:, 1] -= hip_y  
        keypoints_frame[:, 2] -= hip_z

        normalized_keypoints.append(keypoints_frame)
    return np.array(normalized_keypoints)

def transform_keypoints(keypoints):
    transformed_keypoints = []

    for frame_index in range(len(keypoints)):
        keypoints_frame = keypoints[frame_index][:, :3]

        neck_index = 0
        lefthip_index = 11
        righthip_index = 12

        hipline = keypoints_frame[righthip_index] - keypoints_frame[lefthip_index]
        hipline /= np.linalg.norm(hipline)

        hipmid = (keypoints_frame[righthip_index] + keypoints_frame[lefthip_index]) / 2

        spine = hipmid - keypoints_frame[neck_index]
        spine /= np.linalg.norm(spine)
        A = np.stack((hipline, spine), axis=0)

        hnnorm = null_space(A).squeeze()
        rotation_matrix = np.column_stack((hipline, spine, hnnorm))

        keypoints_frame -= hipmid

        transformed_frame = keypoints_frame @ rotation_matrix
        transformed_keypoints.append(transformed_frame)

    return np.array(transformed_keypoints)

hip_center = (kp3d[:, 11, :] + kp3d[:, 12, :]) / 2
kp3d_normalized = normalize_keypoints(kp3d)
kp3d_normalized = transform_keypoints(kp3d_normalized)

def plot_keypoints_3d(ax, keypoints, connections):
    ax.cla()
    ax.scatter(keypoints[:, 0], keypoints[:, 1], keypoints[:, 2], c='r', marker='o')
    
    for connection in connections:
        pt1, pt2 = connection
        ax.plot([keypoints[pt1, 0], keypoints[pt2, 0]],
                [keypoints[pt1, 1], keypoints[pt2, 1]],
                [keypoints[pt1, 2], keypoints[pt2, 2]], 'b')
    
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    plt.draw()

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

initial_frame = 0
plot_keypoints_3d(ax, kp3d_normalized[initial_frame], skeleton_connections)

slider_ax_start = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_ax_end = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')

start_slider = Slider(slider_ax_start, 'Start Frame', 0, len(kp3d_normalized)-1, valinit=0, valstep=1)
end_slider = Slider(slider_ax_end, 'End Frame', 0, len(kp3d_normalized)-1, valinit=len(kp3d_normalized)-1, valstep=1)

def update(val):
    frame = int(val)
    plot_keypoints_3d(ax, kp3d_normalized[frame], skeleton_connections)

start_slider.on_changed(update)
end_slider.on_changed(update)

trim_button_ax = plt.axes([0.8, 0.9, 0.1, 0.05])
trim_button = Button(trim_button_ax, 'Trim', color='lightblue', hovercolor='lightgreen')

def trim_data(event):
    start_frame = int(start_slider.val)
    end_frame = int(end_slider.val)
    trimmed_kp3d = kp3d[start_frame:end_frame+1]
    
    print(f"Trimming data from frame {start_frame} to {end_frame}")
    print(f"Original number of frames: {kp3d_normalized.shape[0]}")
    print(f"Trimmed number of frames: {trimmed_kp3d.shape[0]}")
    
    file_dir, file_name = os.path.split(CURRENT_FILE)
    base_name, ext = os.path.splitext(file_name)
    rel_path_after_keypoints = os.path.relpath(file_dir, 'dataset/3d_keypoints')
    new_dir = os.path.join('dataset', 'trimmed_keypoints', rel_path_after_keypoints)
    os.makedirs(new_dir, exist_ok=True)
    new_file_path = os.path.join(new_dir, f"{base_name}{ext}")
    joblib.dump({'kp3d': trimmed_kp3d}, new_file_path)
    print(f"Trimmed data saved to {new_file_path}")

trim_button.on_clicked(trim_data)

plt.show()
