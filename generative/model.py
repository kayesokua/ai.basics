import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.utils import pad_sequences

from database.dance.terms import all_moves

# Load training and validation data
X_train = np.load("X_train.npy", allow_pickle=True)
y_train = np.load("y_train.npy", allow_pickle=True)

# Convert arrays of lists to arrays of arrays
X_train = np.array([np.array(x) for x in X_train])
y_train = np.array([np.array(y) for y in y_train])

for i, seq in enumerate(X_train):
    print(f"Sequence {i+1} shape: {seq.shape}")

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Pad sequences in X_train and X_val
max_sequence_length = max([len(x) for x in X_train])
print(f"Max sequence length: {max_sequence_length}")

X_train = pad_sequences(X_train, maxlen=max_sequence_length)
X_val = pad_sequences(X_val, maxlen=max_sequence_length)
y_train = pad_sequences(y_train, maxlen=max_sequence_length)
y_val = pad_sequences(y_val, maxlen=max_sequence_length)

# Reshape X_train and X_val
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], -1))
X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], -1))

# Build the model
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True),
    tf.keras.layers.Dense(len(all_moves), activation='softmax')
])

# Compile and fit the model
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X_train, y_train, epochs=1, validation_data=(X_val, y_val))

# Save the model
model.save("user1_dance_preferences.h5")