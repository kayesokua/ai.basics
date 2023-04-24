import cv2
import mediapipe as mp
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.models import Model
from sklearn.impute import SimpleImputer

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

base_model = MobileNetV2(weights='imagenet', include_top=True)
model = Model(inputs=base_model.input, outputs=base_model.get_layer('global_average_pooling2d').output)

def extract_features(video_path, model):
    """
    Extracts features from a video using the MobileNetV2 model.
    """

    try:
        cap = cv2.VideoCapture(video_path)
    except:
        print(f"Could not open video file: {video_path}")
        return None

    features = []
    frame_counter = 0
    max_frames = 24 * 16  # Limit to approximately 30 seconds

    while cap.isOpened() and frame_counter < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (224, 224))

        with mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Only processes frames with detected pose landmarks
        if results.pose_landmarks:
            preprocessed_frame = preprocess_input(frame)
            feature = model.predict(np.expand_dims(preprocessed_frame, axis=0))
            features.append(feature.squeeze())
            frame_counter += 1
        print(f"Processed frame {frame_counter} of {video_path}")

        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + 10)

    cap.release()

    imputer = SimpleImputer(strategy='mean')
    imputed_features = imputer.fit_transform(features)

    if len(features) == 0:
        print(f"No pose detected in video: {video_path}")
        return None

    print(f"Extracted features from {video_path}")

    return np.mean(imputed_features, axis=0)

def get_model_labels(video_paths, labels, X_filename, y_filename):
    features_list = [extract_features(video_path, model) for video_path in video_paths]
    X = np.vstack(features_list)
    y = np.array(labels, dtype=str)
    np.save(f"{X_filename}", X)
    np.save(f"{y_filename}", y)
    return print("Training labels saved")

train_videos = [
    "train/ballet_0.mp4", "train/ballet_1.mp4", "train/ballet_2.mp4", "train/ballet_3.mp4", "train/ballet_4.mp4",
    "train/contemporary_0.mp4", "train/contemporary_1.mp4", "train/contemporary_2.mp4", "train/contemporary_3.mp4", "train/contemporary_4.mp4",
    "train/jazz_0.mp4", "train/jazz_1.mp4", "train/jazz_2.mp4", "train/jazz_3.mp4", "train/jazz_4.mp4",
    "train/kpop_0.mp4", "train/kpop_1.mp4", "train/kpop_2.mp4", "train/kpop_3.mp4", "train/kpop_4.mp4"]
train_labels = ['ballet', 'ballet', 'ballet', 'ballet', 'ballet',
          'contemporary', 'contemporary', 'contemporary', 'contemporary', 'contemporary',
          'jazz', 'jazz', 'jazz', 'jazz', 'jazz',
          'kpop', 'kpop', 'kpop', 'kpop', 'kpop']

get_model_labels(train_videos, train_labels, "X_train.npy", "y_train.npy")

eval_videos = ["eval/ballet_0.mp4","eval/ballet_1.mp4","eval/contemporary_0.mp4","eval/contemporary_1.mp4","eval/kpop_0.mp4"]
eval_labels = ['ballet', 'ballet', 'contemporary', 'contemporary', 'kpop']

get_model_labels(eval_videos, eval_labels, "X_eval.npy", "y_eval.npy")
