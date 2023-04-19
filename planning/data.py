import random

landmarks = ['nose_x', 'nose_y', 'nose_z', 'left_eye_inner_x', 'left_eye_inner_y',
       'left_eye_inner_z', 'left_eye_x', 'left_eye_y', 'left_eye_z',
       'left_eye_outer_x', 'left_eye_outer_y', 'left_eye_outer_z',
       'right_eye_inner_x', 'right_eye_inner_y', 'right_eye_inner_z',
       'right_eye_x', 'right_eye_y', 'right_eye_z', 'right_eye_outer_x',
       'right_eye_outer_y', 'right_eye_outer_z', 'left_ear_x', 'left_ear_y',
       'left_ear_z', 'right_ear_x', 'right_ear_y', 'right_ear_z',
       'mouth_left_x', 'mouth_left_y', 'mouth_left_z', 'mouth_right_x',
       'mouth_right_y', 'mouth_right_z', 'left_shoulder_x', 'left_shoulder_y',
       'left_shoulder_z', 'right_shoulder_x', 'right_shoulder_y',
       'right_shoulder_z', 'left_elbow_x', 'left_elbow_y', 'left_elbow_z',
       'right_elbow_x', 'right_elbow_y', 'right_elbow_z', 'left_wrist_x',
       'left_wrist_y', 'left_wrist_z', 'right_wrist_x', 'right_wrist_y',
       'right_wrist_z', 'left_pinky_x', 'left_pinky_y', 'left_pinky_z',
       'right_pinky_x', 'right_pinky_y', 'right_pinky_z', 'left_index_x',
       'left_index_y', 'left_index_z', 'right_index_x', 'right_index_y',
       'right_index_z', 'left_thumb_x', 'left_thumb_y', 'left_thumb_z',
       'right_thumb_x', 'right_thumb_y', 'right_thumb_z', 'left_hip_x',
       'left_hip_y', 'left_hip_z', 'right_hip_x', 'right_hip_y', 'right_hip_z',
       'left_knee_x', 'left_knee_y', 'left_knee_z', 'right_knee_x',
       'right_knee_y', 'right_knee_z', 'left_ankle_x', 'left_ankle_y',
       'left_ankle_z', 'right_ankle_x', 'right_ankle_y', 'right_ankle_z',
       'left_heel_x', 'left_heel_y', 'left_heel_z', 'right_heel_x',
       'right_heel_y', 'right_heel_z', 'left_foot_index_x',
       'left_foot_index_y', 'left_foot_index_z', 'right_foot_index_x',
       'right_foot_index_y', 'right_foot_index_z']

def generate_position():
    """Generate random position for each landmark"""
    position = {}
    for pose in landmarks:
        if pose.endswith('_x'):
            position[pose] = random.uniform(0, 640)
        elif pose.endswith('_y'):
            position[pose] = random.uniform(0, 360)
        elif pose.endswith('_z'):
            position[pose] = random.uniform(-1, 1)
    return position

def generate_sequence(duration, fps=24):
    """Generate a sequence of random positions"""
    num_frames = int(duration * fps)
    sequence = [generate_position() for _ in range(num_frames)]
    return sequence

movement_vocabulary = [
    {"name": "Contraction", "position": generate_sequence(duration=random.uniform(0, 3)), "level": random.randint(0, 3)},
    {"name": "Release", "position": generate_sequence(duration=random.uniform(0, 3)), "level": random.randint(0, 3)},
    {"name": "Spiral", "position": generate_sequence(duration=random.uniform(0, 3)), "level": random.randint(0, 3)},
    {"name": "Deep plié", "position": generate_sequence(duration=random.uniform(0, 3)), "level": random.randint(0, 3)},
    {"name": "Cupped Hands", "position": generate_sequence(duration=random.uniform(0, 3)), "level": random.randint(0, 3)},
]

print(movement_vocabulary)