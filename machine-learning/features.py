import cv2
import mediapipe as mp
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.models import Model
from sklearn.impute import SimpleImputer


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Load the pre-trained MobileNetV2 model
base_model = MobileNetV2(weights='imagenet', include_top=True)
model = Model(inputs=base_model.input, outputs=base_model.get_layer('global_average_pooling2d').output)

def extract_features(video_path, model):
    try:
        cap = cv2.VideoCapture(video_path)
    except:
        print(f"Could not open video file: {video_path}")
        return None

    features = []
    frame_counter = 0
    max_frames = 24 * 2  # Limit to approximately 30 seconds

    while cap.isOpened() and frame_counter < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to match the expected input shape of the model
        frame = cv2.resize(frame, (224, 224))

        # Check if pose landmarks are detected in the current frame
        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # If pose is detected, process the frame and extract features
        if results.pose_landmarks:
            # Preprocess the frame for the model
            preprocessed_frame = preprocess_input(frame)
            feature = model.predict(np.expand_dims(preprocessed_frame, axis=0))
            features.append(feature.squeeze())
            frame_counter += 1

        print(f"Processed frame {frame_counter} of {video_path}")

        # Skip some frames for faster processing
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + 10)

    cap.release()

    imputer = SimpleImputer(strategy='mean')
    imputed_features = imputer.fit_transform(features)

    # Check if any features were extracted
    if len(features) == 0:
        print(f"No pose detected in video: {video_path}")
        return None

    print(f"Extracted features from {video_path}")

    return np.mean(imputed_features, axis=0)

# Extract features from videos

def get_training_labels(video_paths, labels):
    features_list = [extract_features(video_path, model) for video_path in video_paths]
    X = np.vstack(features_list)
    y = np.array(labels, dtype=str)
    np.save("X_features.npy", X)
    np.save("y_labels.npy", y)
    return print("Training labels saved")

video_paths = ["train/ballet_1.mp4","train/kpop_0.mp4","train/jazz_0.mp4"]
labels = ['ballet','kpop','jazz']
get_training_labels(video_paths, labels)

def get_eval_labels(video_paths, labels):
    features_list = [extract_features(video_path, model) for video_path in video_paths]
    X = np.vstack(features_list)
    y = np.array(labels, dtype=str)
    np.save("X_eval_features.npy", X)
    np.save("y_eval_labels.npy", y)
    return print("Training labels saved")

eval_video_paths = ["eval/ballet_0.mp4"]
eval_labels = ['ballet']
get_eval_labels(eval_video_paths, eval_labels)