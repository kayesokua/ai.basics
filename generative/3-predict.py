import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("user1_dance_preferences.h5")
new_input_sequence = np.random.random((1, 80))
new_input_sequence = new_input_sequence.reshape((1, new_input_sequence.shape[1], 1))
predictions = model.predict(new_input_sequence)
predicted_dance_moves = predictions.reshape((predictions.shape[1],))
print(predicted_dance_moves)